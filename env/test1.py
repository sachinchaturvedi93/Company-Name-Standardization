"""

- creates nested lists of order 'n' where 'n' represents the nesting height. (Assume n=1 for the outermost list)
- the number of elements is 2n where the sequence is range(0, 2n)
- the last element of the list is the sublist

When n = 2, this is how the output would look:

[0, [0,1,2,3]]

When n = 3, the list would look like:

[0, [0, 1, 2, [0, 1, 2, 3, 4, 5]]]
"""
def nest_list(n):
    
