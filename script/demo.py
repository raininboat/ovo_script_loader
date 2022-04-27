
def duel(msg, api):
    if not api.flag_has_olivadice:
        return "本插件需要 OlivaDiceCore"
    nickname =  msg.sender["nickname"]
    player_rd = api.onedice("6d100")
    player_val = player_rd.resInt
    player_step = player_rd.resDetail
    bot_name = "Bot"
    bot_rd = api.onedice("6d100")
    bot_val = bot_rd.resInt
    bot_step = bot_rd.resDetail
    if bot_val > player_val:
        result = f"{bot_name}胜利！"
    elif bot_val < player_val:
        result = f"{nickname}胜利！"
    else:
        result = "平局。"
    rep = f"""
{nickname}:
6D100={player_step}=
{player_val}
{bot_name}:
6D100={bot_step}=
{bot_val}
{result}
"""
    return rep

COMMAND = {
    r"(。|\.)duel" : duel
}
