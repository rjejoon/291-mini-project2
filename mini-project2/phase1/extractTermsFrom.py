import string


def extractTermsFrom(postDoc: dict) -> list:
    '''
    Extracts unique terms from the title and body if those fields exist in the given post document, 
    and returns them in a list.
    '''
    title = set()
    if 'Title' in postDoc:
        title = filterTerms(postDoc['Title'])
        
    body = set()
    if 'Body' in postDoc:
        body = filterTerms(postDoc['Body'])

    return list(title.union(body))


def filterTerms(s: str) -> set:
    '''
    Filters out alphanumeric terms that are at least 3 chars long from the given string and
    returns only the unique ones.
    '''
    if len(s) <= 0:
        return set()

    terms = set()
    start = 0
    for end in range(len(s.strip())):
        if s[end] in string.whitespace or s[end] in string.punctuation:
            if end - start >= 3:    # len of term must be larger than 3 
                terms.add(s[start:end].lower())
            start = end + 1

    if s[end].isalnum(): 
        if end+1 - start >= 3:
            terms.add(s[start:end+1].lower())

    return terms
