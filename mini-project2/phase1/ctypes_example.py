import ctypes

if __name__ == '__main__':
    libname = 'filterTerms.so'
    c_lib = ctypes.CDLL(libname)
