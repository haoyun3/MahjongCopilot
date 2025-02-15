import json

try:
    with open("D:/data/qingyun_statistic.txt", "r", encoding='utf-8') as f_open:
        data = json.loads(f_open.read())
except:
    data = {
        "refresh": {
            'normal': {
                'total': 0,
                'green': 0,
                'blue': 0,
                'gold': 0,
            },
            'super': {
                'total': 0,
                'green': 0,
                'blue': 0,
                'gold': 0,
            },
        },
        "packs": {
            'green': [0, 0, 0, 0],
            'blue': [0, 0, 0, 0],
            'blue+': [0, 0, 0, 0],
            "gold": [0, 0, 0, 0],
        },
        "invitation": {
            'total': 0,
        },
        "cards": {
            'green': {
                'total': 0,
            },
            'blue': {
                'total': 0,
            },
            "gold": {
                'total': 0,
            },
            "legend": {
                'total': 0,
            },
        },
    }


name_list = {
    "10": {"name": "岭上之花", "rarity": 2},
    "50": {"name": "羽化成仙", "rarity": 2},
    "150": {"name": "天之恩惠", "rarity": 3},
    "210": {"name": "财源广进", "rarity": 1},
    "480": {"name": "私喷滥涂", "rarity": 0},
    "570": {"name": "恭喜发财", "rarity": 0},
    "620": {"name": "汪多鱼", "rarity": 1},
    "1010": {"name": "烟花小贩", "rarity": 0},
    "1050": {"name": "有失有得", "rarity": 0},
    "1110": {"name": "直播带货", "rarity": 0},
    "1130": {"name": "过期苹果", "rarity": 0},
    "1210": {"name": "蟠龙池", "rarity": 0},
    "1220": {"name": "美味佳肴", "rarity": 0},
    "1290": {"name": "全身防护", "rarity": 1},
    "1460": {"name": "车轮滚滚", "rarity": 1},
    "1470": {"name": "荧光带鱼", "rarity": 1},
    "1640": {"name": "惊喜发明家未来", "rarity": 2},
    "1660": {"name": "星探墨镜", "rarity": 2},
}
rarity_list = ['green', 'blue', 'gold', 'legend']
buy_tmp = 0


def save_data(action: str, msg: dict):
    global buy_tmp
    if action == 'refresh':
        cnt = [0, 0, 0]
        for good in msg['goods']:
            cnt[good['goodsId'] - 101] += 1
        rtype = 'normal'
        for effect in msg['effect']:
            if effect['id'] == 1660:
                rtype = 'super'
        data[action][rtype]['total'] += 1
        data[action][rtype]['green'] += cnt[0]
        data[action][rtype]['blue'] += cnt[1]
        data[action][rtype]['gold'] += cnt[2]
    elif action == 'buy_pre':
        buy_tmp = msg['id']
        return
    elif action == 'buy':
        rarity = ""
        for good in msg['shop']['goods']:
            if good['id'] == buy_tmp:
                rarity = rarity_list[good['goodsId'] - 101]
                break
        if rarity == 'blue':
            for effect in msg['effect']:
                if effect['id'] == 1661:
                    rarity = 'blue+'
        for effect in msg['shop']['effectList']:
            k = str(effect) if effect % 10 == 0 else str(effect - 1)
            r2 = -1
            if k in name_list:
                r2 = name_list[k]["rarity"]
                flag = True
                for ex in msg['effect']:
                    if ex['id'] % 10 == 1:
                        k2 = str(ex['id'] - 1)
                        if k2 in name_list:
                            if name_list[k2]['rarity'] == r2:
                                flag = False
                        else:
                            flag = False
                if flag:
                    if k in data['cards'][rarity_list[r2]]:
                        data['cards'][rarity_list[r2]][k] += 1
                    else:
                        data['cards'][rarity_list[r2]][k] = 1
                    data['cards'][rarity_list[r2]]['total'] += 1
            if r2 >= 0:
                data["packs"][rarity][r2] += 1
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"new Effect: {effect}")
                print("!!!!!!!!!!!!!!!!!!!!!!!")

    with open("D:/data/qingyun_statistic.txt", "w", encoding='utf-8') as f_write:
        f_write.write(json.dumps(data, indent=4))
