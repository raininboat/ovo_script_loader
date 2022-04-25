"""
Script Loader Test Script
Copyright (C) 2022  Rainy Zhou

在平台聊天中使用 !test all 进行所有项目测试
"""
import time

def test_error(msg, api):
    "返回错误"
    api.log.debug("错误捕捉返回相关测试")
    assert 1 == 2
    api.log.fatal("本条消息不应该发送")
    return "本条消息不应该发送"

def sys_reload(msg, api):
    host_id = msg.host_id
    group_id = msg.group_id
    user_id = msg.user_id
    api.reply(f"{host_id}-{group_id}-{user_id}-触发重启")
    api.proc.set_restart()
    return "重启中"

def test_say_group(msg, api):
    host_id = msg.host_id
    group_id = msg.group_id
    user_id = msg.user_id
    rep = f"[{user_id}]在群聊[{group_id}]中说：“{msg.str[0]}”"
    api.send("group", group_id, rep, host_id)

def test_say_private(msg, api):
    host_id = msg.host_id
    group_id = msg.group_id
    user_id = msg.user_id
    rep = f"[{user_id}]在群聊[{group_id}]中说：“{msg.str[0]}”"
    api.send("private", user_id, rep, host_id)

def test_say_say(msg, api):
    host_id = msg.host_id
    group_id = msg.group_id
    user_id = msg.user_id
    target_id = msg.target_id
    msg_type = msg.msg_type
    rep = f"[{user_id}]在群聊[{group_id}]中说：“{msg.str[0]}”"
    api.send(msg_type, target_id, rep, host_id)

def test_api_all(msg, api):
    api.log.debug("进行全部 api 测试")
    api.log.debug("##################")
    test_send(msg, api)
    api.log.debug("##################")
    test_log(msg, api)
    api.log.debug("##################")
    test_version(msg, api)
    api.log.debug("##################")
    test_web(msg, api)
    api.log.note("完成基本测试，下方测试需要 OlivaDiceCore 模块支持")
    test_ovo_dice(msg, api)
    return "所有测试结束"

def test_log(msg, api):
    api.log.debug("开始进行 log 测试")

    api.log.trace("api.log.trace arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.debug("api.log.debug arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.note("api.log.note arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.info("api.log.info arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.error("api.log.error arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.warn("api.log.warn arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.fatal("api.log.fatal arg2:{2}, arg1:{1}, arg0:{0}, {kwarg1}, {kwarg2}",
        "arg0", "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    api.log.debug("当不包含额外参数时，原始消息不经过 fmt 直接 log - {1} {1,3 }{22+2k}")

    api.log(0,"直接使用 api.log(0, 'xxx') 跳过封装")

    api.log.debug("log 测试结束")
    return "log相关测试 内容详见终端"

def test_version(msg, api):
    version = api.version
    api.log.debug(f"the olivos svn is {version.olivos_svn}")
    api.log.debug(f"the olivos version is {version.olivos_version}")
    api.log.debug(f"the script loader svn is {api.version.script_loader_svn}")
    api.log.debug(f"the script loader version is {api.version.olivos_svn}")
    return "api.version api 测试，内容详见 终端log"

def test_send(msg, api):
    api.log.debug("开始进行 api.send 测试")
    host_id = msg.host_id
    group_id = msg.group_id
    user_id = msg.user_id
    target_id = msg.target_id
    msg_type = msg.msg_type
    reply = "本条为测试消息,通过 api.send({0},{1}, 'xxx' ,{2}) 发送"
    if group_id is None:
        api.log.warn("测试由私聊触发，忽略群组发送")
    else:
        api.send("group",group_id, reply.format("'group'", "group_id", "host_id"), host_id)
        time.sleep(0.5)
        api.send(1,group_id, reply.format('1', 'group_id', 'host_id'), host_id)
        time.sleep(0.5)
    api.send("private",user_id, reply.format("'private'", "user_id", None))
    time.sleep(0.5)
    api.send(0,user_id, reply.format('0', 'user_id', None))
    time.sleep(0.5)
    api.send(msg_type, target_id, reply.format('msg_type', 'target_id', 'host_id'), host_id)
    time.sleep(0.5)
    api.reply("本条测试消息，通过 api.reply('xxx') 发送")

    api.log.debug("send 测试结束")
    return "send相关测试结束，本条消息由直接 return 返回发送"


def test_web(msg, api):
    api.log.debug("进行网页获取测试")
    data_dir = api.data_dir()
    api.log.debug("通过 api.data_dir() 获取 ./plugin/data 的绝对路径为 <{0}>", data_dir)
    tmp_dir_path = data_dir + "/tmp"
    api.mkdir(tmp_dir_path)
    api.mkdir(tmp_dir_path)     # 测试重复创建是否会出错
    api.log.debug("创建文件夹目录: {dir_path} 成功", dir_path = tmp_dir_path)
    url = "https://www.baidu.com"
    api.log.debug("即将通过 api.web_download 下载网页 {url} 的内容", url=url)
    api.web_download(url, tmp_dir_path+"/tmp.html")
    with open(tmp_dir_path+"/tmp.html", mode="r", encoding="utf-8") as file:
        txt = file.read()
        api.log.debug("{tmp_dir_path}/tmp.html 文件内容为：\n{txt}", tmp_dir_path=tmp_dir_path, txt=txt)
        md5 = api.md5(txt)
        api.log.debug("文件md5 {0}", md5)
    return f"网页获取测试，具体详见终端，文件 md5:{md5}"

def test_ovo_dice(msg, api):
    if not api.flag_has_olivadice:
        api.log.fatal("OlivaDiceCore不存在，测试结束")
        return
    # platform = msg.platform
    user_id = msg.user_id

    api.log.note("测试 api.draw")
    card = api.draw("单张塔罗牌")
    api.log.debug(f"api.draw('单张塔罗牌') => {card}")
    card = api.draw("这是一个不存在的卡组名称123456abc")  # 测试不存在的卡组
    api.log.debug(f"api.draw('这是一个不存在的卡组名称123456abc') => {card}")
    api.log.debug("=================")
    api.log.note("测试 api.onedice")
    rd_para = api.onedice("3d6+5-b2")
    api.log.debug(rd_para.originData)
    api.log.debug("------------------")
    if rd_para.resError is not None:
        api.log.debug(rd_para.resError)
    else:
        api.log.debug(rd_para.resInt)
        api.log.debug(rd_para.resIntMax)
        api.log.debug(rd_para.resIntMin)
        api.log.debug(rd_para.resIntMaxType)
        api.log.debug(rd_para.resIntMinType)
        api.log.debug(rd_para.resDetail)
    api.log.debug("##")
    rd_para = api.onedice("wphoinjhd23wnedpoj")
    api.log.debug(rd_para.originData)
    api.log.debug("------------------")
    if rd_para.resError is not None:
        api.log.debug(rd_para.resError)
    else:
        api.log.debug(rd_para.resInt)
        api.log.debug(rd_para.resIntMax)
        api.log.debug(rd_para.resIntMin)
        api.log.debug(rd_para.resIntMaxType)
        api.log.debug(rd_para.resIntMinType)
        api.log.debug(rd_para.resDetail)

    api.log.debug("=================")
    api.log.note("测试 api.get_pc_hash")
    fake_hash = api.get_pc_hash("1111111", "fake")
    pc_hash = api.get_pc_hash(user_id)
    api.log.debug(f"fake_hash = {fake_hash}, pc_hash = {pc_hash}")

    api.log.debug("=================")
    api.log.debug("测试人物卡名称相关")
    api.log.note("初始化人物卡名称")
    data1 = api.set_card_name(card_name="default", uid=user_id)
    data2 = api.set_card_name(card_name="default", pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.get_card_name")
    data1 = api.get_card_name(uid=user_id)
    data2 = api.get_card_name(pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.set_card_name (data1设置成功 True； data2设置失败 False)")
    data1 = api.set_card_name(card_name="测试人物卡名称", uid=user_id)
    data2 = api.set_card_name(card_name="测试人物\n卡名称", pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.get_card_name")
    data1 = api.get_card_name(uid=user_id)
    data2 = api.get_card_name(pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("修改人物卡名称")
    data1 = api.set_card_name(card_name="default", uid=user_id)
    data2 = api.set_card_name(card_name="default", pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")

    api.log.debug("=================")
    api.log.note("测试 api.get_pc_card")
    data1 = api.get_card_data(uid=user_id)
    data2 = api.get_card_data(pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")

    api.log.debug("=================")
    api.log.debug("测试技能读取+设置")
    api.log.debug("------------------")
    api.log.note("初始化test数据")
    data1 = api.set_pc_skill(skillname="test", skillval=0, uid=user_id)
    data2 = api.set_pc_skill(skillname="san", skillval=0, pc_hash=fake_hash)
    # api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.get_pc_skill 获取当前test（应当为 0 ）")
    data1 = api.get_pc_skill(skillname="test", uid=user_id)
    data2 = api.get_pc_skill(skillname="test", pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.set_pc_skill")
    data1 = api.set_pc_skill(skillname="test", skillval=42, uid=user_id)
    data2 = api.set_pc_skill(skillname="test", skillval=42, pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.get_pc_skill 获取当前理智值（应当为 42 ）")
    data1 = api.get_pc_skill(skillname="test", uid=user_id)
    data2 = api.get_pc_skill(skillname="test", pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    api.log.debug("------------------")
    api.log.note("测试 api.get_pc_card")
    data1 = api.get_card_data(uid=user_id)
    data2 = api.get_card_data(pc_hash=fake_hash)
    api.log.debug(f"data1 = {data1}, data2 = {data2}")
    return "Oliva Dice Core 相关测试结束"



COMMAND = {
    r"!test oliva" : test_ovo_dice,
    r"!test version" : test_version,
    r"!test send" : test_send,
    r"!test log" : test_log,
    r"!test web" : test_web,
    r"!test error" : test_error,
    r"!test all" : test_api_all,
    # r"!(test) ([a-f]{3,}) (.*)" : test_api_all,
    r"!sys reload" : sys_reload,            # 不进行鉴权，收到后直接重启ovo完整托盘，仅用于开发测试阶段
    r"#group (.*)" : test_say_group,
    r"#private (.*)" : test_say_private,
    r"#say (.*) " : test_say_say,
}
