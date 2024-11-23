def longDivision(n1 = 1, n2 = 1, ranMore = False, decimalPlace = None, decimalDivision = None, rounds = 0) -> str:
    n3 = ""
    n1Str = str(n1)
    n2Str = str(n2)
    m = 0
    if "." in n1Str:
        move = len(n1Str) - n1Str.index(".") - 1
        if "." in n2Str:
            moved = n2Str.index(".")
            if len(n2Str) - moved > move:
                lessAmount = True
            while lessAmount:
                n2Str += "0"
                if len(n2Str) - moved > move:
                    lessAmount = False
                    n2Str = n2Str[:move] + n2Str[move + 1:]
        else:
            print(move)
            for i in range(move):
                n2Str += "0"
        decimalDivision = n1Str.index(".")
        print(n1Str, decimalDivision)
        n1Str = (n1Str[:decimalDivision] + n1Str[decimalDivision + 1:])
        print(n1Str)
    elif "." in n2Str:
        decimalDivision = n2Str.index(".")
        n2Str = n2Str[:move] + "" + n2Str[move + 1:]
    add = len(n1Str)
    for s in range(len(n1Str)):
        checking = True
        i = 0
        while checking:
            i += 1
            #print(str(n2Str[m:m + len(n1Str)]) * i > int(n1Str[m:m + len(n2Str)]), float(n2Str[m:m + len(n2Str)]) * i, float(n1Str[m:m + len(n2Str)]), "i:", i, n2Str[m:m + len(n2Str)], n3, m, ranMore, )
            if (n2Str[m:m + len(n1Str)] == '') or (int(n1Str[m:m + len(n2Str)]) == 0):
                if ranMore:
                    n3 = n3[:decimalPlace + 1] + "0" + n3[decimalPlace + 1:]
                else:
                    n3 += "0"
                checking = False
            elif int(n2Str[m:m + len(n2Str)]) * i > int(n1Str[m:m + len(n2Str)]):
                print("END")
                i -= 1
                if ranMore:
                    n3 = n3[:decimalPlace + 1] + str(i) + n3[decimalPlace + 1:]
                else:
                    n3 += str(i)
                checking = False
                if (m + len(n1Str) >= len(n1Str)
                    and int(n2Str[m:m + len(n1Str)]) * i < int(n1Str[m:m + len(n1Str)])):
                        n1Str += "0"
                        if ranMore:
                            print("RAN MORE")
                            rounds += 1
                            if rounds != 3:
                                n3 = str(longDivision(n1Str, n2Str, True, decimalPlace, decimalDivision, rounds))
                            else:
                                n3 += "..."
                        else:
                            print("RAN FIRST")
                            n3 = str(longDivision(n1Str, n2Str, True, m, decimalDivision, rounds))
                        break
                elif m + add >= len(n1Str) and ranMore:
                    print("ADDING DECIMAL")
                    n3 = n3[:decimalPlace] + '.' + n3[decimalPlace:]
        m += add
        if m >= len(n1Str):
            break
    if decimalDivision != None:
        n3 = n3[:decimalDivision + 1] + "." + n3[decimalDivision + 1:]
    #n3.lstrip("0")
    return n3
if __name__ == "__main__":
    print(longDivision(8, 12))