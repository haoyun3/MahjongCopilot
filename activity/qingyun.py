import json

from mode import li_pai, mode1, mode2, mode3, modeqing


def main():
    p_dora, p_hand, p_mo, p_left = pai_shan()
    print("宝牌指示牌:", p_dora)
    print("理牌手牌:", li_pai(p_hand))
    print("牌河待摸牌", p_mo)
    print("换牌待换牌", p_left)
    mode = int(input("请输入你想做的牌型\n"
                     "1, 换牌的国士无双十三面\n"
                     "2, 不换牌的七对子\n"
                     "3, 不换牌的万象六对子\n"
                     "4, 清一色筒子\n"
                     "5, 清一色索子\n"
                     "请输入序号 : "))
    if mode == 1:
        mode1(p_dora, p_hand, p_mo, p_left)
    elif mode == 2:
        mode2(p_dora, p_hand, p_mo)
    elif mode == 3:
        mode3(p_dora, p_hand, p_mo)
    elif mode == 4:
        modeqing(p_dora, p_hand, p_mo, p_left, 'p')
    elif mode == 5:
        modeqing(p_dora, p_hand, p_mo, p_left, 's')
    else:
        print("没做")


def pai_shan():
    with open("D:/Data/maj_input.txt", "r", encoding='utf-8') as f:
        data = json.loads(f.read())
    pool = data['pool']
    dora = data['dora']
    hand = data['hands']
    p_dora = []
    for pai in dora:
        for a in pool:
            if a['id'] == pai:
                p_dora.append(a['tile'])
                break
    p_hand = []
    for pai in hand:
        for a in pool:
            if a['id'] == pai:
                p_hand.append(a['tile'])
                break
    p_mo = []
    p_left = []
    pool = pool[10:]
    for pai in pool:
        if pai['id'] not in hand:
            if len(p_mo) < 36:
                p_mo.append(pai['tile'])
            else:
                p_left.append(pai['tile'])
    return p_dora, p_hand, p_mo, p_left


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
