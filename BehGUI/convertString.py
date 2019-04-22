#https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float

from ast import literal_eval

def convertString(s):
    if isinstance(s, str):
        # It's a string.  Does it represnt a literal?
        #
        try:
            val = literal_eval(s)
        except:
            # s doesn't represnt any sort of literal so no conversion will be
            # done.
            #
            val = s
    else:
        # It's already something other than a string
        #
        val = s

    ##
    # Is the float actually an int? (i.e. is the float 1.0 ?)
    #
    if isinstance(val, float):
        if val.is_integer():
            return int(val)

        # It really is a float
        return val

    return val
