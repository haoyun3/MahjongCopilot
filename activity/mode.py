import json


def mode1(p_dora: list, p_hand: list, p_mo: list, p_left: list):
    need_raw = ["1m", "9m", "1p", "9p", "1s", "9s",
                "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
    need = {}
    for pai in need_raw:
        if pai not in need:
            need[pai] = 1
        else:
            need[pai] += 1
    for k in range(len(p_mo)):
        if p_mo[k] in need:
            need[p_mo[k]] -= 1
            if need[p_mo[k]] == 0:
                del need[p_mo[k]]
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
            for _ in range(5):
                change = []
                hand_tmp = hand.copy()
                for pai in hand_tmp:
                    if pai_in_which(pai, need):
                        if pai_in_which(pai, future):
                            change.append(pai)
                            hand.remove(pai)
                            future[pai] -= 1
                            if future[pai] == 0:
                                del future[pai]
                        else:
                            tmp = pai_count(pai, hand)
                            if tmp > need[pai]:
                                if pai_in_which(pai, backup):
                                    tmp2 = min(tmp - need[pai], pai_count(pai, backup))
                                    if not pai_in_which(pai, future_raw):
                                        future_raw[pai] = tmp2
                                    else:
                                        future_raw[pai] += tmp2
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
                change_history.append(change)
                flag_break = False
                while len(hand) < 13:
                    hand.append(p_left[cnt])
                    cnt += 1
                    if cnt >= len(p_left):
                        cnt -= len(p_left)
                        flag_break = True
                        break
                if flag_break:
                    hand = []
                    break
                hand = li_pai(hand)
        flag = True
        for pai in need:
            if pai_count(pai, hand) < need[pai]:
                flag = False
                break
        if flag:
            print(f"将在第{k + 1}巡自摸 {p_mo[k]} 凑齐国士无双, 以下为开局换牌序列")
            for output in change_history:
                print(output)
            print("以下为换完后手牌")
            print(hand)
            print('牌山对照: ')
            print(p_mo[:9])
            print(p_mo[9: 18])
            print(p_mo[18: 27])
            print(p_mo[27:])
            break


def mode2(p_dora: list, p_hand: list, p_mo: list):
    def get_rating(pi: str, k: int) -> int:
        ans = pai_search_next(pi, k)
        if ans == 36:
            return 100
        ans += 64
        if 's' in pi and (mode == 1 or mode == 2):
            ans -= 36
            left = p_mo[k:].copy()
            cnt2 = left.count("5s") + left.count("0s") if '0' in pi or '5' in pi else left.count(pi)
            ans -= 10 * (cnt2 - 1)
        if mode == 3:
            left = p_mo[k:].copy()
            cnt2 = left.count(f"5{pi[1]}") + left.count(f"0{pi[1]}") if '0' in pi or '5' in pi else left.count(pi)
            ans -= 20 * (cnt2 - 1)
        return ans

    def pai_search_next(pi: str, k: int) -> int:
        left = p_mo[k:].copy()
        if '0' in pi or '5' in pi:
            ans1 = left.index(f'5{pi[1]}') + k if f'5{pi[1]}' in left else 36
            ans2 = left.index(f'0{pi[1]}') + k if f'0{pi[1]}' in left else 36
            ans = min(ans1, ans2)
        else:
            ans = left.index(pi) + k if pi in left else 36
        return ans

    mode = int(input("请选择额外功能:\n"
                     "0, 无额外功能，以最快速度和牌结束\n"
                     "1, 摸索子模式，以尽量多和索子次数结束\n"
                     "2, 索子七对模式，以尽量多的索子对子结束\n"
                     "3, 多和牌模式，以尽量多的和牌结束\n"
                     "请选择 : "))
    lock = int(input("被锁的牌数为 : "))
    if lock > 0:
        p_mo = p_mo[:-lock]
    print('牌山对照: ')
    print(p_mo[:9])
    print(p_mo[9: 18])
    print(p_mo[18: 27])
    print(p_mo[27:])
    print(f"起始手牌: {p_hand}")

    action_list = []
    p_finish = []
    for pai in p_hand:
        if pai_count(pai, p_hand) == 2 and not pai_in_which(pai, p_finish):
            p_finish.append(pai)
    for cnt in range(len(p_mo)):
        new_pai = p_mo[cnt]
        # p_hand = li_pai(p_hand)
        # print(new_pai, p_finish, p_hand)
        if pai_in_which(new_pai, p_finish):
            if '0' in new_pai:
                action_list.append(f"手切5{new_pai[1]}")
            else:
                action_list.append(f"摸切{new_pai}")
            # print(action_list[-1])
            continue
        else:
            p_hand.append(new_pai)
            if pai_count(new_pai, p_hand) == 2:
                p_finish.append(new_pai)
        flag = False
        p_judge = []
        for pai in p_hand:
            if pai_count(pai, p_hand) > 2:
                out = pai if '0' not in pai else f'5{pai[1]}'
                outputMsg = '摸切' if out == new_pai else '手切'
                action_list.append(f"{outputMsg}{out}")
                p_hand.remove(out)
                # print(action_list[-1])
                if pai_count(pai, p_hand) == 2:
                    p_finish.append(pai)
                flag = True
                break
            elif not pai_in_which(pai, p_finish):
                p_judge.append(pai)
        if flag:
            continue
        if not p_judge:
            action_list.append(f"自摸!!!{new_pai}")
            more = p_mo[cnt:]
            print(f'和牌次数: {more.count(new_pai)}')
            break
        max_num = -1
        out = ""
        for pai in p_judge:
            tmp = get_rating(pai, cnt + 1)
            if tmp > max_num:
                max_num = tmp
                out = pai
        if max_num < 100 and 's' in out and mode == 2:
            for pai in p_finish:
                if 's' not in pai:
                    out = pai
                    p_finish.remove(pai)
                    break
        outputMsg = '摸切' if out == new_pai else '手切'
        action_list.append(f"{outputMsg}{out}")
        # print(action_list[-1], p_judge)
        p_hand.remove(out)
    while len(action_list) > 9:
        print(action_list[:9])
        action_list = action_list[9:]
    print(action_list)
    print(li_pai(p_hand))


def mode3(p_dora: list, p_hand: list, p_mo: list):
    def get_rating(pi: str, k: int) -> int:
        ans = pai_search_next(pi, k)
        if ans == 36:
            return 100
        ans += 64
        return ans

    def pai_search_next(pi: str, k: int) -> int:
        left = p_mo[k:].copy()
        if '0' in pi or '5' in pi:
            ans1 = left.index(f'5{pi[1]}') + k if f'5{pi[1]}' in left else 36
            ans2 = left.index(f'0{pi[1]}') + k if f'0{pi[1]}' in left else 36
            ans = min(ans1, ans2)
        else:
            ans = left.index(pi) + k if pi in left else 36
        return ans

    print('牌山对照: ')
    print(p_mo[:9])
    print(p_mo[9: 18])
    print(p_mo[18: 27])
    print(p_mo[27:])
    p_hand = li_pai(p_hand)
    print(f"起始手牌: {p_hand}")

    action_list = []
    p_finish = []
    for pai in p_hand:
        if pai_count(pai, p_hand) == 2 and not pai_in_which(pai, p_finish):
            p_finish.append(pai)
    for cnt in range(len(p_mo)):
        new_pai = p_mo[cnt]
        if len(p_finish) == 6:
            action_list.append(f"自摸!!!{new_pai}")
            win = 0
            left = p_mo[cnt:]
            for pai in left:
                if not pai_in_which(pai, p_hand):
                    win += 1
            print(f'和牌次数: {win}')
            break
        # p_hand = li_pai(p_hand)
        # print(new_pai, p_finish, p_hand)
        if pai_in_which(new_pai, p_finish):
            if '0' in new_pai:
                action_list.append(f"手切5{new_pai[1]}")
            else:
                action_list.append(f"摸切{new_pai}")
            # print(action_list[-1])
            continue
        else:
            p_hand.append(new_pai)
            if pai_count(new_pai, p_hand) == 2:
                p_finish.append(new_pai)
        flag = False
        p_judge = []
        for pai in p_hand:
            if pai_count(pai, p_hand) > 2:
                out = pai if '0' not in pai else f'5{pai[1]}'
                outputMsg = '摸切' if out == new_pai else '手切'
                action_list.append(f"{outputMsg}{out}")
                p_hand.remove(out)
                # print(action_list[-1])
                if pai_count(pai, p_hand) == 2:
                    p_finish.append(pai)
                flag = True
                break
            elif not pai_in_which(pai, p_finish):
                p_judge.append(pai)
        if flag:
            continue
        max_num = -1
        out = ""
        for pai in p_judge:
            tmp = get_rating(pai, cnt + 1)
            if tmp > max_num:
                max_num = tmp
                out = pai
        outputMsg = '摸切' if out == new_pai else '手切'
        action_list.append(f"{outputMsg}{out}")
        # print(action_list[-1], p_judge)
        try:
            p_hand.remove(out)
        except:
            print('failed to remove: ', out)
    while len(action_list) > 9:
        print(action_list[:9])
        action_list = action_list[9:]
    print(action_list)
    print(li_pai(p_hand))


def mode_qing(p_dora: list, p_hand: list, p_mo: list, p_left: list, sp: str):
    op = int(input("请选择额外规则:\n"
                   "0, 无额外规则\n"
                   "1, 换牌次数不超过3次\n"
                   "2, 换牌每次最多选3张\n"
                   "3, 不换牌\n"
                   "请选择 : "))
    c_times = 5
    c_times = c_times if op != 1 else 3
    c_times = c_times if op != 3 else 0
    with open("D:/Data/majong_qing.txt", "r", encoding='utf-8') as f:
        data = json.loads(f.read())["data"]
    win_list = []
    for target in data:
        if len(win_list) > 1000:
            break
        need_raw = []
        for pai in target["hand"]:
            need_raw.append(f"{pai}{sp}")
        need_backup = {}
        for pai in need_raw:
            pai_get_num(pai, need_backup, 1)
        left = 0
        right = len(p_mo) - 2
        ans = -1
        ans_data = {}
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
                    hand_tmp = hand.copy()
                    for pai in hand_tmp:
                        if pai_in_which(pai, need):
                            if pai_in_which(pai, future):
                                change.append(pai)
                                hand.remove(pai)
                                pai_get_num(pai, future, -1)
                                if pai_get_num(pai, future) == 0:
                                    pai_del_which(pai, future)
                                if len(change) >= 3 and op == 2:
                                    break
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
                                        if len(change) >= 3 and op == 2:
                                            break
                        else:
                            change.append(pai)
                            hand.remove(pai)
                            if len(change) >= 3 and op == 2:
                                break
                    if flag:
                        break
                    backup = hand.copy()
                    change_history.append(li_pai(change))
                    flag_break = False
                    while len(hand) < 13:
                        hand.append(p_left[cnt])
                        cnt += 1
                        if cnt >= len(p_left):
                            cnt -= len(p_left)
                            flag_break = True
                            break
                    if flag_break:
                        hand = []
                        break
                    hand = li_pai(hand)
            flag = True
            for pai in need:
                if pai_count(pai, hand) < pai_get_num(pai, need):
                    flag = False
                    break
            if flag:
                ans = k
                right = k - 1
                outputStr = "以下为开局换牌序列"
                change_cnt = 0
                for output in change_history:
                    change_flag = False
                    outputStr += '\n'
                    for pai in output:
                        if sp in pai:
                            outputStr += f"{pai} "
                            change_flag = True
                    outputStr += f"+ 非{sp}" if change_flag else f"非{sp}"
                    change_cnt += len(output)
                outputStr += f'\n以下为换完后手牌\n{hand}'
                outputStr += f'\n以下为听牌时牌型\n{need_raw}'
                outputStr += f'\n牌山对照: \n{p_mo[:9]}\n{p_mo[9: 18]}\n{p_mo[18: 27]}\n{p_mo[27:]}'
                outputStr += f"\n将在第{k + 1}巡自摸 {p_mo[k]} 凑齐清一色听牌,"
                mo_list = []
                for pai in target['ting']:
                    mo_list.append(f"{pai}{sp}")
                first = -1
                tot = 0
                for k2 in range(k + 1, len(p_mo)):
                    if pai_in_which(p_mo[k2], mo_list):
                        if first < 0:
                            first = k2 + 1
                            outputStr += f'\n将第在{k2 + 1}巡第一次自摸'
                            tot = 1
                        else:
                            tot += 1
                outputStr += f'\n听牌列表{mo_list}\n总共自摸{tot}次'
                ans_data = (tot, -change_cnt, -first, outputStr)
            else:
                left = k + 1
        if ans > -1:
            win_list.append(ans_data)
    win_list.sort(reverse=True)
    idx = 0
    con = 'y'
    while con == 'y':
        print(win_list[idx][-1])
        idx += 1
        con = input('next? y/n : ')


def mode_god(p_dora: list, p_hand: list, p_mo: list, p_left: list):
    data = []
    p_god = pai_get_dora(p_dora)

    def god_dfs(dfs_id: int, ting: str, select: list):
        if len(select) == 6:
            tmp_hand = select.copy() + select.copy()
            tmp_hand.append(ting)
            data.append({'hand': tmp_hand})
            return
        if dfs_id >= len(p_god):
            return
        tmp_pai = p_god[dfs_id]
        if tmp_pai != ting:
            select.append(tmp_pai)
            god_dfs(dfs_id + 1, ting, select)
            select.remove(tmp_pai)
        god_dfs(dfs_id + 1, ting, select)

    for pai in p_god:
        if 's' in pai:
            god_dfs(0, pai, [])

    op = int(input("请选择额外规则:\n"
                   "0, 无额外规则\n"
                   "1, 换牌次数不超过3次\n"
                   "2, 换牌每次最多选3张\n"
                   "3, 不换牌\n"
                   "请选择 : "))
    c_times = 5
    c_times = c_times if op != 1 else 3
    c_times = c_times if op != 3 else 0

    win_list = []
    for target in data:
        need_raw = target["hand"]
        need_backup = {}
        for pai in need_raw:
            pai_get_num(pai, need_backup, 1)
        left = 0
        right = len(p_mo) - 2
        ans = -1
        ans_data = {}
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
                    hand_tmp = hand.copy()
                    for pai in hand_tmp:
                        if pai_in_which(pai, need):
                            if pai_in_which(pai, future):
                                change.append(pai)
                                hand.remove(pai)
                                pai_get_num(pai, future, -1)
                                if pai_get_num(pai, future) == 0:
                                    pai_del_which(pai, future)
                                if len(change) >= 3 and op == 2:
                                    break
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
                                        if len(change) >= 3 and op == 2:
                                            break
                        else:
                            change.append(pai)
                            hand.remove(pai)
                            if len(change) >= 3 and op == 2:
                                break
                    if flag:
                        break
                    backup = hand.copy()
                    change_history.append(li_pai(change))
                    flag_break = False
                    while len(hand) < 13:
                        hand.append(p_left[cnt])
                        cnt += 1
                        if cnt >= len(p_left):
                            cnt -= len(p_left)
                            flag_break = True
                            break
                    if flag_break:
                        hand = []
                        break
                    hand = li_pai(hand)
            flag = True
            for pai in need:
                if pai_count(pai, hand) < pai_get_num(pai, need):
                    flag = False
                    break
            if flag:
                ans = k
                right = k - 1
                outputStr = "以下为开局换牌序列"
                change_cnt = 0
                for output in change_history:
                    outputStr += '\n'
                    for pai in output:
                        outputStr += f"{pai} "
                    change_cnt += len(output)
                outputStr += f'\n以下为换完后手牌\n{hand}'
                outputStr += f'\n以下为听牌时牌型\n{need_raw}'
                outputStr += f'\n牌山对照: \n{p_mo[:9]}\n{p_mo[9: 18]}\n{p_mo[18: 27]}\n{p_mo[27:]}'
                outputStr += f"\n将在第{k + 1}巡自摸 {p_mo[k]} 凑齐神域听牌,"

                first = -1
                tot = 0
                for k2 in range(k + 1, len(p_mo)):
                    if pai_in_which(p_mo[k2], p_god):
                        if first < 0:
                            first = k2 + 1
                            outputStr += f'\n将第在{k2 + 1}巡第一次自摸'
                            tot = 1
                        else:
                            tot += 1
                outputStr += f'\n听牌列表{p_god}\n总共自摸{tot}次'
                ans_data = (tot, -change_cnt, -first, outputStr)
            else:
                left = k + 1
        if ans > -1:
            win_list.append(ans_data)
    if len(win_list) <= 0:
        print("很遗憾，无法和牌")
        return
    win_list.sort(reverse=True)
    idx = 0
    con = 'y'
    while con == 'y':
        print(win_list[idx][-1])
        idx += 1
        con = input('next? y/n : ')


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


def pai_count(pi: str, p_hand: list):
    if pi == '5s' or pi == '0s':
        return p_hand.count('5s') + p_hand.count('0s')
    if pi == '5p' or pi == '0p':
        return p_hand.count('5p') + p_hand.count('0p')
    else:
        return p_hand.count(pi)


def pai_in_which(pi: str, which) -> bool:
    if '0' in pi or '5' in pi:
        return f'5{pi[1]}' in which or f'0{pi[1]}' in which
    else:
        return pi in which


def pai_get_num(pi: str, which: dict, change: int = 0):
    if change == 0:
        if '0' in pi or '5' in pi:
            if f'5{pi[1]}' in which:
                return which[f'5{pi[1]}']
            else:
                return which[f'0{pi[1]}']
        else:
            return which[pi]
    else:
        if '0' in pi or '5' in pi:
            if f'5{pi[1]}' in which:
                which[f'5{pi[1]}'] += change
            elif f'0{pi[1]}' in which:
                which[f'0{pi[1]}'] += change
            else:
                which[f'5{pi[1]}'] = change
        else:
            if pi in which:
                which[pi] += change
            else:
                which[pi] = change


def pai_del_which(pi: str, which):
    if '0' in pi or '5' in pi:
        if f'5{pi[1]}' in which:
            del which[f'5{pi[1]}']
        else:
            del which[f'0{pi[1]}']
    else:
        del which[pi]


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
