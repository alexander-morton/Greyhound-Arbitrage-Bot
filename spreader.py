
def spreader(dct):
    spread = 0
    for dog in dct:
        
        spread += 1/max(dct[dog])

    if spread< 1:
        return True, spread

    return False, spread

    

