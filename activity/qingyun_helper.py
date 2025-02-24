import re

left = []
hand = []
dora = []
cnt = 49
cnt2 = 36


def init():
    global left, hand, dora, cnt2
    print("神域青云之志遍历助手v1.0  ------   by 扫地机\n\n")
    print("输入格式均为类似 1919m114p514s1234z类似的格式\n"
          "顺序没要求，不识别区分0p请写5p")
    raw_dora = []
    str_input = input("请输入宝牌指示牌:\n")
    r = re.findall(r"\d*[mpsz]", str_input)
    for k in r:
        for i in range(len(k) - 1):
            raw_dora.append(f"{k[i]}{k[-1]}")
    if len(raw_dora) != 10:
        str_input = input("检测到宝牌指示牌不等于10张，请补充输入，如果确认无误请直接回车:\n")
        r = re.findall(r"\d*[mpsz]", str_input)
        for k in r:
            for i in range(len(k) - 1):
                raw_dora.append(f"{k[i]}{k[-1]}")
    dora = pai_get_dora(raw_dora)
    dora = li_pai(dora)
    for pai in dora:
        left.append(pai)
        left.append(pai)
        left.append(pai)
        left.append(pai)
    for pai in raw_dora:
        left.remove(pai)
    left = li_pai(left)
    print_dora()
    str_input = input("请输入牌河明牌:\n")
    r = re.findall(r"\d*[mpsz]", str_input)
    for k in r:
        for i in range(len(k) - 1):
            cnt2 -= 1
            pai = f"{k[i]}{k[-1]}"
            if pai in left:
                left.remove(pai)
    str_input = input(f"牌河目前还有{cnt2}暗牌，请补充输入牌河明牌，如果确认无误可直接回车:\n")
    r = re.findall(r"\d*[mpsz]", str_input)
    for k in r:
        for i in range(len(k) - 1):
            cnt2 -= 1
            pai = f"{k[i]}{k[-1]}"
            if pai in left:
                left.remove(pai)
    print_helper()
    str_input = input("请输入手牌(不影响牌统计，只是检测不合法，不用可直接回车):\n")
    r = re.findall(r"\d*[mpsz]", str_input)
    for k in r:
        for i in range(len(k) - 1):
            pai = f"{k[i]}{k[-1]}"
            hand.append(pai)
    hand = li_pai(hand)


def main():
    init()
    global left, hand, cnt, dora
    for _ in range(8):
        throw = []
        str_input = input("请输入要换掉的牌:\n")
        r = re.findall(r"\d*[mpsz]", str_input)
        for k in r:
            for i in range(len(k) - 1):
                pai = f"{k[i]}{k[-1]}"
                if pai in left:
                    left.remove(pai)
                throw.append(pai)
        cnt -= len(throw)
        backup = hand.copy()
        print_helper()
        hand = []
        str_input = input("请输入换完后手牌(不影响牌统计，只是检测不合法，不用可直接回车):\n")
        r = re.findall(r"\d*[mpsz]", str_input)
        for k in r:
            for i in range(len(k) - 1):
                pai = f"{k[i]}{k[-1]}"
                hand.append(pai)
        hand = li_pai(hand)


def li_pai(p_hand):
    m = []
    p = []
    s = []
    z = []
    for pai in p_hand:
        if "m" in pai:
            m.append(pai)
        elif "p" in pai:
            p.append(pai)
        elif "s" in pai:
            s.append(pai)
        elif "z" in pai:
            z.append(pai)
    m.sort()
    z.sort()
    if '0p' in p:
        p[p.index('0p')] = '5p'
        p.sort()
        p[p.index('5p')] = '0p'
    else:
        p.sort()
    if '0s' in s:
        s[s.index('0s')] = '5s'
        s.sort()
        s[s.index('5s')] = '0s'
    else:
        s.sort()
    return m + p + s + z


def pai_get_dora(p_dora: list):
    tmp = set()
    for pai in p_dora:
        if '0' in pai:
            tmp.add('5' + pai[1])
            tmp.add('6' + pai[1])
        else:
            tmp.add(pai)
            if '9' in pai:
                tmp.add('1' + pai[1])
            elif 'm' in pai:
                tmp.add('9m')
            elif 'z' in pai and pai in ['4z', '7z']:
                if pai == '4z':
                    tmp.add('1z')
                else:
                    tmp.add('5z')
            else:
                tmp.add(f"{int(pai[0]) + 1}{pai[1]}")
    return list(tmp)


def print_dora():
    outputStr_m = "万: "
    outputStr_p = "筒: "
    outputStr_s = "索: "
    outputStr_z = "字: "
    for pai in left:
        if 'm' in pai:
            outputStr_m += pai[0]
        elif 'p' in pai:
            outputStr_p += pai[0]
        elif 's' in pai:
            outputStr_s += pai[0]
        elif 'z' in pai:
            outputStr_z += pai[0]
    print(f"神域有效牌{len(dora)}种: {dora}")
    print(f"剩余可换出神域牌(手牌+可换牌+暗牌，已去掉牌河明牌)\n{outputStr_m}m\n{outputStr_p}p\n{outputStr_s}s\n{outputStr_z}z\n")


def print_helper():
    print_dora()
    global cnt, left, hand, cnt2

    helperStr1 = "七对子辅助:\n"
    p1 = []
    for pai in dora:
        if left.count(pai) >= 2:
            if left.count(pai) == 2:
                p1.append(f"{pai[0]}{pai}*")
            else:
                p1.append(f"{pai[0]}{pai}")
    while len(p1) > 7:
        helperStr1 += f"{p1[:7]}\n"
        p1 = p1[7:]
    helperStr1 += f"{p1}\n"

    helperStr2 = "面子手辅助:\n"
    p2 = []
    for pai in dora:
        if left.count(pai) >= 3:
            if left.count(pai) == 3:
                p2.append(f"{pai[0]}{pai[0]}{pai}*")
            else:
                p2.append(f"{pai[0]}{pai[0]}{pai}")
        pai2 = f"{int(pai[0]) + 1}{pai[1]}"
        pai3 = f"{int(pai[0]) + 2}{pai[1]}"
        if pai in left and pai2 in left and pai3 in left:
            if left.count(pai) >= 2 and left.count(pai2) >= 2 and left.count(pai3) >= 2:
                p2.append(f"{pai[0]}{pai2[0]}{pai3}")
            else:
                p2.append(f"{pai[0]}{pai2[0]}{pai3}*")
    while len(p2) > 5:
        helperStr2 += f"{p2[:5]}\n"
        p2 = p2[5:]
    helperStr2 += f"{p2}\n"

    outputStr = "注意，手牌中不符合的牌有:"
    for pai in hand:
        if pai not in dora:
            outputStr += ' ' + pai
    print(f"剩余{cnt}张待换牌, 及{cnt2}张牌河暗牌, 剩余有效牌包括手牌在内有{len(left)}张")
    print(helperStr1)
    print(helperStr2)
    print(f"有效神域牌:{dora}")
    print(outputStr)


if __name__ == '__main__':
    main()
