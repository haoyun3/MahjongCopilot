import json
from .qingyun_mode import (
    li_pai, get_ting_list, check_anke,
    pai_del_which, pai_equal, pai_count, pai_get_num, pai_in_which,
)
pool = []


def mode_qing(p_hand: list, p_mo: list, p_left: list, change_times: int = 5, op: int = 0):
    sp = 'p'
    c_times = change_times
    with open("D:/Data/majong_qing.txt", "r", encoding='utf-8') as f:
        data = json.loads(f.read())["data"]
    win_list = []
    for target in data:
        if len(win_list) > 500:
            break
        need_raw = []
        for pai in target["hand"]:
            need_raw.append(f"{pai}{sp}")
        if op == 2:
            flag = True
            for i in range(1, 10):
                if i not in target["hand"]:
                    flag = False
                    break
            if not flag:
                continue
        need_backup = {}
        for pai in need_raw:
            pai_get_num(pai, need_backup, 1)
        left = -1
        right = len(p_mo) - 2
        ans = -2
        ans_data = (-2, [[0], [0]])
        while left <= right:
            k = (left + right) // 2
            need = need_backup.copy()
            for j in range(k + 1):
                if pai_in_which(p_mo[j], need):
                    pai_get_num(p_mo[j], need, -1)
                    if pai_get_num(p_mo[j], need) == 0:
                        pai_del_which(p_mo[j], need)
            flag = True
            future_raw = {}
            change_history = []
            hand = []
            while flag:
                hand = p_hand.copy()
                future = future_raw.copy()
                flag = False
                change_history = []
                backup = []
                cnt = 0
                for _ in range(c_times):
                    change = []
                    hand_tmp = li_pai(hand.copy())
                    for pai in hand_tmp:
                        if pai_in_which(pai, need):
                            if pai_in_which(pai, future):
                                change.append(pai)
                                hand.remove(pai)
                                pai_get_num(pai, future, -1)
                                if pai_get_num(pai, future) == 0:
                                    pai_del_which(pai, future)
                            else:
                                tmp = pai_count(pai, hand)
                                if tmp > pai_get_num(pai, need):
                                    if pai_in_which(pai, backup):
                                        tmp2 = min(tmp - pai_get_num(pai, need), pai_count(pai, backup))
                                        pai_get_num(pai, future_raw, tmp2)
                                        flag = True
                                        break
                                    else:
                                        change.append(pai)
                                        hand.remove(pai)
                        else:
                            change.append(pai)
                            hand.remove(pai)
                    if flag:
                        break
                    backup = hand.copy()
                    change = li_pai(change)
                    c_his = []
                    for j in range(len(change)):
                        x = hand_tmp.index(change[j])
                        if j > 0:
                            if change[j] == change[j - 1]:
                                x = c_his[-1] + 1
                        c_his.append(x)
                    change_history.append(c_his)
                    flag_break = False
                    tmp_cnt = 0
                    while change:
                        tmp_cnt += 1
                        hand.append(p_left[cnt])
                        cnt += 1
                        if cnt >= len(p_left):
                            cnt -= len(p_left)
                            flag_break = True
                            break
                        del change[0]
                    if flag_break:
                        hand = []
                        break
                    hand = li_pai(hand)
            success = 0
            for pai in need:
                if pai_count(pai, hand) < pai_get_num(pai, need):
                    success += pai_get_num(pai, need) - pai_count(pai, hand)
            if success <= 13 - len(p_hand):
                ans = k
                right = k - 1
                mo_list = []
                for pai in target['ting']:
                    mo_list.append(f"{pai}{sp}")
                hand_ting = need_raw

                tot = 0
                roll_cnt = 0
                for k2 in range(k + 1, len(p_mo)):
                    if pai_in_which(p_mo[k2], mo_list):
                        if op == 3:
                            roll_cnt += check_anke(hand_ting, p_mo[k2])
                        tot += 1
                if op == 3:
                    ans_data = (roll_cnt, hand_ting.copy(), mo_list, change_history)
                else:
                    ans_data = (tot, hand_ting.copy(), mo_list, change_history)
            else:
                left = k + 1
        if ans > -2:
            win_list.append(ans_data)
    win_list.sort(reverse=True)
    return win_list[0][1], win_list[0][3], win_list[0][2]


def get_helper(data: dict):
    global pool
    pool = data['pool']
    hand = data['hands']
    change_times = data['remainChangeTileCount']
    effects = data['effectList']
    effect = 0
    for e in effects:
        if e['id'] == 1460:
            effect = 3
            break
        elif e['id'] == 1470:
            effect = 2
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
    target, changeList, hu_list = mode_qing(p_hand, p_mo, p_left, change_times, effect)
    return changeList, target, hu_list


def get_helper_dahai(data: dict, target: list, hu: list):
    global pool
    p_hand = []
    for pai in data['hands']:
        for a in pool:
            if a['id'] == pai:
                p_hand.append(a['tile'])
                break
    new = p_hand[-1]
    del p_hand[-1]
    p_hand = li_pai(p_hand)
    if pai_count(new, p_hand) < pai_count(new, target):
        # 需要new这张牌，从手里切牌
        for pai in p_hand:
            if pai_count(pai, p_hand) > pai_count(pai, target):
                return p_hand.index(pai)
    else:
        # 不需要new这张牌，看看是不是和牌
        flag = True  # 是否听牌
        gang = False  # 是否存在杠按钮
        for pai in p_hand:
            if pai_count(pai, p_hand) > pai_count(pai, target):
                flag = False
            if pai_count(pai, p_hand) >= 4 or pai_count(pai, p_hand) >= 3 and pai_equal(new, pai):
                gang = True
        if flag and pai_in_which(new, hu):
            if gang:
                return -2
            else:
                return -1
        else:
            return 14
