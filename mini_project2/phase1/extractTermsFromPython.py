

def extractTermsFrom(postDoc: dict) -> list:
    '''
    Extracts unique terms from the title and body if those fields exist in the given post document, 
    and returns them in a list.
    '''
    terms = set()
    if 'Title' in postDoc:
        filterTerms(terms, postDoc['Title'])
        
    if 'Body' in postDoc:
        filterTerms(terms, postDoc['Body'])

    if 'Tags' in postDoc:
        filterTerms(terms, postDoc['Tags'])

    return list(terms)


def filterTerms(terms: set, s: str):
    '''
    Filters out alphanumeric terms that are at least 3 chars long from the given string and
    returns only the unique ones.
    '''
    if len(s) == 0:
        return 

    # does not handle for case-insensitive
    start = 0       
    i = 0
    for i in range(len(s.strip())):
        if not s[i].isalnum():
            if i - start >= 3:    # len of term must be larger than 3 
                terms.add(s[start:i])
            start = i + 1

    if s[i].isalnum(): 
        if (i - start) + 1 >= 3:
            terms.add(s[start:i+1])




    
