
def spreader(dct):
    spread = 0
    for dog in dct:

        spread += 1/dct[dog].max()

    if spread< 1:
        return True

    return False

    
