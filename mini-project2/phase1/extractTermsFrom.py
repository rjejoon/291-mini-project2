 

def extractTermsFrom(postDoc: dict) -> list:
    '''
    Extracts terms from the title and body if those fields exist in the given post document, 
    and returns them in a list.
    '''
    title = []
    if 'Title' in postDoc:
        title = postDoc['Title'].split()
        title = map(termFilter, title)
        title = list(filter(lambda t: len(t)>=3, title))

    body = []
    if 'Body' in postDoc:
        body = postDoc['Body'].split()
        body = map(termFilter, body)
        body = list(filter(lambda t: len(t)>=3, body))

    return title + body

def termFilter(t: str) -> str:
    '''
    Filter out the whitespaces and punctuations from the string.
    '''

    t = t.strip()
    t = t.replace('<p>', '')
    t = t.replace('</p>', '')
    t = t.replace('<a href=\\', '')
    return ''.join([ch for ch in t if ch.isalnum()])