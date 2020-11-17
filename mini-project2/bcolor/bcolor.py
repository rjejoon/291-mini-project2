PINK = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def underline(s):
    return UNDERLINE + s + ENDC

def errmsg(s):
    return FAIL + s + ENDC

def cyan(s):
    return OKCYAN + s + ENDC

def blue(s):
    return OKBLUE + s + ENDC

def pink(s):
    return PINK + s + ENDC

def bold(s):
    return BOLD + s + ENDC

def warning(s):
    return WARNING + s + ENDC

def green(s):
    return OKGREEN + s + ENDC
