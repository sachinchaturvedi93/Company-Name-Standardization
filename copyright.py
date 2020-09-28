import re
import pandas as pd
from ftfy import fix_text
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct

def CopyRight(data):

    def ngrams(string, n=3):
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
        string = string.replace('Corp', ' ')
        string = string.replace('Corporation', ' ')
        string = string.replace('Holding', ' ')
        string = string.replace('Holdings', ' ')
        string = string.replace('Ltd', ' ')
        string = string.replace('LTD', ' ')
        string = string.replace('LLC', ' ')
        string = string.replace('LLP', ' ')
        string = string.replace('Co', ' ')
        string = string.replace('Company', ' ')
        string = string.replace('US', ' ')
        string = string.replace('United States', ' ')
        ngrams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in ngrams]

    from sklearn.feature_extraction.text import TfidfVectorizer
    clean_org_names = pd.read_excel(
                'data.xlsx')
    cleanlist = list(clean_org_names.name)
    data = data[~data['name'].isin(cleanlist)]
    #clean_org_names = clean_org_names.iloc[:, 2:7]
    final = pd.concat([clean_org_names[['name']], data[['name']]],
                        ignore_index=True, axis=0)
    company_names = final['name'].unique().astype('U')
    #company_names = final['name'].astype('U')
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix = vectorizer.fit_transform(company_names)


    def awesome_cossim_top(A, B, ntop, lower_bound=0):
        # force A and B as a CSR matrix.
        # If they have already been CSR, there is no overhead
        A = A.tocsr()
        B = B.tocsr()
        M, _ = A.shape
        _, N = B.shape

        idx_dtype = np.int32

        nnz_max = M*ntop

        indptr = np.zeros(M+1, dtype=idx_dtype)
        indices = np.zeros(nnz_max, dtype=idx_dtype)
        data = np.zeros(nnz_max, dtype=A.dtype)

        ct.sparse_dot_topn(
            M, N, np.asarray(A.indptr, dtype=idx_dtype),
            np.asarray(A.indices, dtype=idx_dtype),
            A.data,
            np.asarray(B.indptr, dtype=idx_dtype),
            np.asarray(B.indices, dtype=idx_dtype),
            B.data,
            ntop,
            lower_bound,
            indptr, indices, data)

        return csr_matrix((data, indices, indptr), shape=(M, N))


    matches = awesome_cossim_top(
        tf_idf_matrix, tf_idf_matrix.transpose(), 10)


    def get_matches_df(sparse_matrix, name_vector, top=100):
        non_zeros = sparse_matrix.nonzero()

        sparserows = non_zeros[1]
        sparsecols = non_zeros[0]

        if top:
            nr_matches = top
        else:
            nr_matches = sparserows.size

        left_side = np.empty([nr_matches], dtype=object)
        right_side = np.empty([nr_matches], dtype=object)
        similarity = np.zeros(nr_matches)

        for index in range(0, nr_matches):
            left_side[index] = name_vector[sparserows[index]]
            right_side[index] = name_vector[sparsecols[index]]
            similarity[index] = sparse_matrix.data[index]

        return pd.DataFrame({'Name': left_side,
                            'Match': right_side,
                            'similarity': similarity})
    
    count = matches.nonzero()
    counter = count[1]
    
    matches_df = get_matches_df(matches, company_names, top = counter.size)

    matches_df = matches_df[matches_df['similarity']< 0.9999999999999]  # Remove all exact matches
    list_data = list(data.name)
    matches_df = matches_df[matches_df['Name'].isin(list_data)]
    matches_df = matches_df[~matches_df['Match'].isin(list_data)]
    idx = matches_df.groupby(['Name'])['similarity'].transform(max) == matches_df['similarity']
    matches_df = matches_df[idx]
    return matches_df.reset_index(drop = True)
