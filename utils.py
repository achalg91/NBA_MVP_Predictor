def cleanArrayAndConvertToFloat(arr) :
    arr.pop(0)
    arr[-1] = arr[-1].strip()
    arr = list(map(float, arr))
    return arr

