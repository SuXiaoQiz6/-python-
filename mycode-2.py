# -*- encoding= utf-8 -*-

def main():
    a = input("Input:")
    dic = {}
    result = []
    li = a.split(" ")
    mubiao_str = li[0]
    mubiao_int = int(li[1])
    for i in range(len(mubiao_str)):
        if mubiao_str[i] in dic and (i-dic[mubiao_str[i]]) <= mubiao_int:
            dic[mubiao_str[i]] = i
            result.append("-")
        else:
            dic[mubiao_str[i]] = i
            result.append(mubiao_str[i])
    print("Output:","".join(result))

if __name__ == "__main__":
    main()