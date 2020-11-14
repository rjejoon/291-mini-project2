
def filterTerms(s: str) -> list:
    '''
    Extract alphanumeric terms that are at least 3 chars long from the given string.
    '''
    terms = []
    start = 0
    for end in range(len(s)):
        if not s[end].isalnum():
            if end - start >= 3:    # len of term must be larger than 3 
                terms.append(s[start:end])
            start = end + 1

    # the last term is not added if the last char is alphanumeric.
    if s[end].isalnum():    
        if end - start >= 3:
            terms.append(s[start:end+1])

    return terms
