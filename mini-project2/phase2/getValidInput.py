from bcolor.bcolor import errmsg


def getValidInput(prompt: str, validEntries: list) -> str:
    '''
    Prompts the user for an input. 
    The input is case-insensitive, so validEntries is assumed to contain 
    only the lowercased str elements.
    '''
    while True:
        entry = input(prompt).lower()
        if entry in validEntries:
            return entry
        print(errmsg("error: invalid entry"))
