

def clear():
    '''
    Clears the shell.
    '''
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
