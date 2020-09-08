import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from ftfy import fix_text

def CopyRight(df):

    # Grab the column you'd like to group, filter out duplicate values
    clean_org_names = pd.read_csv(
        'C:/users/schaturvedi/Desktop/Python/Project Match/Forbes.csv', encoding='latin-1')
    clean_org_names = clean_org_names.iloc[:, 2:7]
    final = pd.concat([clean_org_names[['name']], df[['name']]],
                    ignore_index=True, axis=0)
    vals = final['name'].unique().astype('U')
    # and make sure the values are Unicode
    #vals = df['Company Name'].unique().astype('U')


    # Write a function for cleaning strings and returning an array of ngrams
    def ngrams_analyzer(string, n=3):
        string = fix_text(string)  # fix text encoding issues
        # remove non ascii chars
        string = string.encode("ascii", errors="ignore").decode()
        string = string.lower()  # make lower case
        chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'"]
        rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
        string = re.sub(rx, '', string)  # remove the list of chars defined above
        string = string.replace('&', 'and')
        string = string.replace(',', ' ')
        string = string.replace('-', ' ')
        string = string.title()  # normalise case - capital at start of each word
        # get rid of multiple spaces and replace with a single space
        string = re.sub(' +', ' ', string).strip()
        string = ' ' + string + ' '  # pad names for ngrams...
        string = re.sub(r'[,-./]|\sBD', r'', string)
        ngrams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in ngrams]


    # Construct your vectorizer for building the TF-IDF matrix
    vectorizer = TfidfVectorizer(analyzer=ngrams_analyzer)

    # Build the matrix!!!
    tfidf_matrix = vectorizer.fit_transform(vals)

    # Import IGN's awesome_cossim_topn module
    from sparse_dot_topn import awesome_cossim_topn

    # The arguments for awesome_cossim_topn are as follows:
    ### 1. Our TF-IDF matrix
    ### 2. Our TF-IDF matrix transposed (allowing us to build a pairwise cosine matrix)
    ### 3. A top_n filter, which allows us to filter the number of matches returned, which isn't useful for our purposes
    ### 4. This is our similarity threshold. Only values over 0.8 will be returned
    cosine_matrix = awesome_cossim_topn(
    tfidf_matrix,
    tfidf_matrix.transpose(),
    vals.size,
    0.55
    )


    # Build a coordinate matrix from a cosine matrix
    coo_matrix = cosine_matrix.tocoo()

    # Instaniate our lookup hash table
    group_lookup = {}


    def find_group(row, col):
        # If either the row or the col string have already been given
        # a group, return that group. Otherwise return none
        if row in group_lookup:
            return group_lookup[row]
        elif col in group_lookup:
            return group_lookup[col]
        else:
            return None


    def add_vals_to_lookup(group, row, col):
        # Once we know the group name, set it as the value
        # for both strings in the group_lookup
        group_lookup[row] = group
        group_lookup[col] = group


    def add_pair_to_lookup(row, col):
        # in this function we'll add both the row and the col to the lookup
        group = find_group(row, col)  # first, see if one has already been added
        if group is not None:
            # if we already know the group, make sure both row and col are in lookup
            add_vals_to_lookup(group, row, col)
        else:
            # if we get here, we need to add a new group.
            # The name is arbitrary, so just make it the row
            add_vals_to_lookup(row, row, col)


    # for each row and column in coo_matrix
    # if they're not the same string add them to the group lookup
    for row, col in zip(coo_matrix.row, coo_matrix.col):
        if row != col:
            # Note that what is passed to add_pair_to_lookup is the string at each index
            # (eg: the names in the legal_name column) not the indices themselves
            add_pair_to_lookup(vals[row], vals[col])


    df['Group'] = df['name'].map(group_lookup).fillna(df['name'])

    return df

