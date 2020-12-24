
def spreader(dct):
    spread = 0
    for dog in dct:
        if dct[dog] == []:
            f = open("success.txt", "a")
            f.write("???????????")
            f.close()
            continue
        
        spread += 1/max(dct[dog])

    if spread< 1:
        return True, spread

    return False, spread

    

