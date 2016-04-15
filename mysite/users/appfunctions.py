def getLevel(totalexp):
    levelinfo = [
    {"name":"Game Scrub","exp_required":200},
    {"name":"Game Noob","exp_required":400},
    {"name":"Game Newbie","exp_required":800},
    {"name":"Game Trainee","exp_required":1600},
    {"name":"Game Novice","exp_required":3200},
    {"name":"Game Adept","exp_required":6400},
    {"name":"Game Veteran","exp_required":12800},
    {"name":"Game Expert","exp_required":25600},
    {"name":"Game Master","exp_required":51200},
    {"name":"Game God","exp_required":102400},
    ]

    for level in levelinfo:
        if totalexp < level.get("exp_required"):
            return level
            break
        else:
            continue
