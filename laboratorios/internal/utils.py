def is_integer(x):
    return x.isdigit() or x[0] == "-" and x[1:].isdigit()
