import string


def extractTermsFrom(postDoc: dict) -> list:
    '''
    Extracts unique terms from the title and body if those fields exist in the given post document, 
    and returns them in a list.
    '''
    title = []
    if 'Title' in postDoc:
        title = filterTerms(postDoc['Title'])
        
    body = []
    if 'Body' in postDoc:
        body = filterTerms(postDoc['Body'])

    tag = []
    if 'Tags' in postDoc:
        tag = filterTerms(postDoc['Tags'])

    return title + body + tag


def filterTerms(s: str) -> list:
    '''
    Filters out alphanumeric terms that are at least 3 chars long from the given string and
    returns only the unique ones.
    '''
    if len(s) <= 0:
        return [] 

    terms = [] 
    start = 0
    for end in range(len(s.strip())):
        if s[end] in string.whitespace or s[end] in string.punctuation:
            if end - start >= 3:    # len of term must be larger than 3 
                terms.append(s[start:end].lower())
            start = end + 1

    if s[end].isalnum(): 
        if end+1 - start >= 3:
            terms.append(s[start:end+1].lower())

    return terms
