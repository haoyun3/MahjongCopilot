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
    "20": {"name": "海底皎月", "rarity": 2},
    "30": {"name": "点石成金", "rarity": 1},
    "40": {"name": "金闪闪", "rarity": 1},
    "50": {"name": "羽化成仙", "rarity": 2},
    "70": {"name": "和牌代价", "rarity": 1},
    "90": {"name": "钦差关防", "rarity": 2},
    "100": {"name": "役满大师", "rarity": 3},
    "110": {"name": "护身礼包", "rarity": 3},
    "120": {"name": "绩效奖励", "rarity": 2},
    "130": {"name": "阶梯调价", "rarity": 1},
    "140": {"name": "连续冲刺", "rarity": 1},
    "150": {"name": "天之恩惠", "rarity": 3},
    "160": {"name": "小猪储钱罐", "rarity": 1},
    "190": {"name": "私密日记", "rarity": 1},
    "200": {"name": "地底探险", "rarity": 1},
    "210": {"name": "财源广进", "rarity": 1},
    "220": {"name": "资本积累", "rarity": 1},
    "240": {"name": "龙之加护", "rarity": 1},
    "250": {"name": "风之加护", "rarity": 1},
    "270": {"name": "赏金猎人", "rarity": 1},
    "280": {"name": "回收机器人", "rarity": 1},
    "290": {"name": "能者多劳", "rarity": 1},
    "300": {"name": "数牌数数", "rarity": 0},
    "310": {"name": "秘籍：抢跑", "rarity": 0},
    "320": {"name": "秘籍：冲刺", "rarity": 0},
    "330": {"name": "秘籍：先行", "rarity": 0},
    "340": {"name": "秘籍：后发", "rarity": 0},
    "360": {"name": "无料物料", "rarity": 0},
    "380": {"name": "断幺神器", "rarity": 0},
    "390": {"name": "四十已到", "rarity": 0},
    "420": {"name": "占星术", "rarity": 0},
    "430": {"name": "常看常新", "rarity": 0},
    "440": {"name": "荒野探险", "rarity": 0},
    "450": {"name": "赛博淘金", "rarity": 0},
    "470": {"name": "最低保障", "rarity": 0},
    "480": {"name": "私喷滥涂", "rarity": 0},
    "490": {"name": "机会卡", "rarity": 0},
    "500": {"name": "独唱高歌", "rarity": 0},
    "520": {"name": "一气通半", "rarity": 0},
    "550": {"name": "致幻蘑菇", "rarity": 2},
    "560": {"name": "再来一次", "rarity": 1},
    "570": {"name": "恭喜发财", "rarity": 0},
    "590": {"name": "风神印记", "rarity": 0},
    "600": {"name": "商店常客", "rarity": 0},
    "610": {"name": "节节高", "rarity": 0},
    "620": {"name": "汪多鱼", "rarity": 1},
    "630": {"name": "无字天书", "rarity": 0},
    "650": {"name": "四君子：梅", "rarity": 1},
    "660": {"name": "四君子：兰", "rarity": 1},
    "670": {"name": "四君子：竹", "rarity": 1},
    "680": {"name": "四君子：菊", "rarity": 1},
    "700": {"name": "岚星·影分身", "rarity": 3},
    "710": {"name": "一眼万年", "rarity": 1},
    "720": {"name": "再换一次", "rarity": 0},
    "730": {"name": "汪的财宝", "rarity": 1},
    "740": {"name": "加油助力", "rarity": 1},
    "750": {"name": "巅峰盲盒", "rarity": 1},
    "1010": {"name": "烟花小贩", "rarity": 0},
    "1020": {"name": "彩虹泉水", "rarity": 0},
    "1030": {"name": "节电令", "rarity": 0},
    "1040": {"name": "伐木场", "rarity": 0},
    "1050": {"name": "有失有得", "rarity": 0},
    "1060": {"name": "放大缩小灯", "rarity": 0},
    "1070": {"name": "黄金矿工", "rarity": 1},
    "1080": {"name": "坐地起价", "rarity": 0},
    "1100": {"name": "延迟满足", "rarity": 0},
    "1110": {"name": "直播带货", "rarity": 0},
    "1120": {"name": "捉五魁", "rarity": 0},
    "1130": {"name": "过期苹果", "rarity": 0},
    "1140": {"name": "猫咪养老院", "rarity": 0},
    "1160": {"name": "美好寄托", "rarity": 0},
    "1170": {"name": "文房四宝", "rarity": 0},
    "1180": {"name": "小猫钓鱼", "rarity": 0},
    "1190": {"name": "刮刮乐", "rarity": 0},
    "1200": {"name": "萌生情感", "rarity": 1},
    "1210": {"name": "蟠龙池", "rarity": 0},
    "1220": {"name": "美味佳肴", "rarity": 0},
    "1230": {"name": "一姬克星", "rarity": 1},
    "1240": {"name": "大蛇瞪眼", "rarity": 1},
    "1250": {"name": "违规燃放", "rarity": 1},
    "1260": {"name": "人山人海", "rarity": 1},
    "1270": {"name": "烟花加特林", "rarity": 1},
    "1280": {"name": "偷天换日", "rarity": 1},
    "1290": {"name": "全身防护", "rarity": 1},
    "1300": {"name": "已读不回", "rarity": 1},
    "1310": {"name": "护身符黄牛", "rarity": 1},
    "1320": {"name": "传国美玉", "rarity": 1},
    "1340": {"name": "魔豆", "rarity": 1},
    "1350": {"name": "荒野时代", "rarity": 1},
    "1360": {"name": "快速列车", "rarity": 1},
    "1370": {"name": "数位时代", "rarity": 1},
    "1380": {"name": "摸鱼临时工", "rarity": 1},
    "1390": {"name": "双学位", "rarity": 1},
    "1410": {"name": "开锁大师", "rarity": 2},
    "1430": {"name": "烟花上膛", "rarity": 1},
    "1440": {"name": "红包拿来", "rarity": 1},
    "1450": {"name": "摩天大楼", "rarity": 1},
    "1460": {"name": "车轮滚滚", "rarity": 1},
    "1470": {"name": "荧光带鱼", "rarity": 1},
    "1480": {"name": "公子买单", "rarity": 2},
    "1490": {"name": "幻影役满", "rarity": 2},
    "1500": {"name": "花火主场姬川响", "rarity": 2},
    "1510": {"name": "类魂游戏", "rarity": 2},
    "1520": {"name": "元宇宙", "rarity": 1},
    "1530": {"name": "万里挑一", "rarity": 2},
    "1540": {"name": "神社大舞台", "rarity": 2},
    "1550": {"name": "吞金幼龙琳琅", "rarity": 2},
    "1560": {"name": "百花缭乱", "rarity": 2},
    "1570": {"name": "负重前行", "rarity": 2},
    "1580": {"name": "王之召唤", "rarity": 2},
    "1590": {"name": "储备粮食", "rarity": 2},
    "1600": {"name": "无边黑洞", "rarity": 2},
    "1610": {"name": "小游戏高手", "rarity": 2},
    "1620": {"name": "神域", "rarity": 2},
    "1630": {"name": "晚会邀请函", "rarity": 2},
    "1640": {"name": "惊喜发明家未来", "rarity": 2},
    "1650": {"name": "耀眼明珠", "rarity": 2},
    "1660": {"name": "星探墨镜", "rarity": 2},
    "1670": {"name": "假面酒侍白夜", "rarity": 3},
    "1680": {"name": "魔法开锁匠柚", "rarity": 3},
    "1690": {"name": "万象天引", "rarity": 3},
    "1700": {"name": "模仿捣蛋鬼阳菜", "rarity": 2},
    "1720": {"name": "失败的发明", "rarity": 2},
}  # 差藤蔓，君子，乱步
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
            if effect['id'] == 1660 or effect['id'] == 1661:
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
            if k in name_list:
                r2 = name_list[k]["rarity"]
                data["packs"][rarity][r2] += 1
                flag = True
                only_glasses = r2 == 2
                for ex in msg['effect']:
                    if ex['id'] % 10 == 1:
                        k2 = str(ex['id'] - 1)
                        if k2 in name_list:
                            if name_list[k2]['rarity'] == r2:
                                flag = False
                                if k2 != '1660':
                                    only_glasses = False
                        else:
                            flag = False
                if flag:
                    if k in data['cards'][rarity_list[r2]]:
                        data['cards'][rarity_list[r2]][k] += 1
                    else:
                        data['cards'][rarity_list[r2]][k] = 1
                    data['cards'][rarity_list[r2]]['total'] += 1
                elif only_glasses:
                    if k in data['cards']['gold-glasses']:
                        data['cards']['gold-glasses'][k] += 1
                    else:
                        data['cards']['gold-glasses'][k] = 1
                    data['cards']['gold-glasses']['total'] += 1
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"new Effect: {effect}")
                print("!!!!!!!!!!!!!!!!!!!!!!!")

    with open("D:/data/qingyun_statistic.txt", "w", encoding='utf-8') as f_write:
        f_write.write(json.dumps(data, indent=4, sort_keys=True))
