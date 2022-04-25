# API 详情
本页显示所有传入参数和内置 api
## 脚本原型
~~~python
COMMAND = {}

def temFunc(msg, api)
    Reply = ""
    return Reply

COMMAND[Regex] = Func
~~~
## 指令映射
对于所有托盘处理的指令，有如下映射:
~~~
COMMAND[Regex] = Func
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| COMMAND | dict | 所有暴露给托盘的指令映射 | 本项为必填项 |
| Regex | str | 所有指令响应的正则表达式 | 本项为必填项 |
| Func | callable | 指令对应的处理函数 | 本项为必填项 |

托盘接收到符合 `Regex` 正则表达式的消息事件后，运行 `Func` 函数
注：和 `[Oliva|2]喧闹测试` 不同，此处的 `Func` 函数并不是函数名称的字符串，而是直接设置为对应的函数

以下为正确的设置:
~~~python
def my_func(msg, api): ...
COMMAND["regex to run my_func"] = my_func       # 这里函数后面不用加括号，也不用加引号
~~~
## 传入参数
对于每个在 `COMMAND` 映射表中注册的函数，需要接收如下入参
~~~python
def my_func(msg, api): ...
~~~
### msg
`msg` 为消息数据对象，有如下属性：
| 名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| msg | str | 完整的消息信息 | "" |
| str | list | 消息中由正则表达式匹配到的信息列表 | [] |
| platform | str | 消息来源平台信息,例如 qq, telegram | None |
| msg_type | int | 消息类型 0 为 私聊消息，1 为群聊消息 | None |
| self_id | ID (int) | 机器人 id | None |
| self_hash | str | 机器人 account hash | None |
| user_id | ID (str) | 用户ID | None |
| group_id | ID (str) | 群聊ID | None |
| host_id | ID (str) | 频道ID（用于特定平台） | None |
| target_id | ID (str) | 群聊中则为 群聊ID，私聊则为 用户ID | None |
| user_info | int | 用户信息，0为私聊，1为群员，2为管理员，3为群主 | None |
| sender | dict | 发送者具体信息，详见 onebot 协议 和 OlivOS 框架 | {} |
| flag_is_master | bool | 框架如安装 OlivaDiceCore 插件，则返回当前用户是否为 OlivaDiceCore 管理员 | None |
| flag_has_olivadice | bool | 框架是否安装 OlivaDiceCore 插件 | None |



### api
`api` 为实现的功能

 =======

其中有如下成员：
#### flag_has_olivadice
一个常量，返回框架是否安装 OlivaDiceCore 插件
~~~python
a = api.flag_has_olivadice

>>> True
~~~
#### proc
OlivOS 框架 Proc
具体参数详见 OlivOS 官方文档
#### plugin_event
OlivOS 框架事件 plugin_event
具体参数详见 OlivOS 官方文档
#### version
一个结构体，内部含有本插件和 OlivOS 的版本信息
具体属性如下:
| 名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| olivos_svn | int | OlivOS 的 svn 版本号 | - |
| olivos_version | str | OlivOS 的版本字符串(如 '1.2.3') | - |
| script_loader_svn | int | Script Loader 的 svn 版本号 | - |
| script_loader_version | str | Script Loader 的版本字符串(如 '1.2.3') | - |

 =======

内含如下接口方法:
#### log
此为 OlivOS 框架 proc_log 的封装，添加 `trace` `debug` `info` `note` `warning` `error` `fatal` 方法，便于直接使用发送对应等级 log ，也可以直接调用，使用原版框架 log 函数
~~~python
api.log.info("这是一条示例信息{0},{1},{kwarg0},{kwarg1}", arg0, arg1,kwarg0=kwarg0,kwarg1=kwarg1)
~~~
具体如下:
- 通过 api.log.xxx() 发送时，第一个参数为 log 字符串，后面可以接任意不定参数，用于作为 log 字符串中 {x}  变量的值
- 如果仅有一个参数，则不会进行 format 操作(用于打印含有 {} 的信息)
- 直接 api.log() 发送时，等同于在框架中调用 Proc.log()

#### reply
原路返回一条消息
~~~python
api.reply("测试消息")
~~~
调用后直接在触发消息事件的 群聊 or 私聊 窗口中回复对应消息

| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| message | str | 具体发送消息内容 | 本项必填 |

#### send
对某个窗口发送消息 (详见框架接口)
~~~python
api.send(send_type, target_id, message, host_id)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| send_type | str 或 int | 用于指定发送目标的类型 | 本项必填 |
| target_id | str | 发送目标的ID | 本项必填 |
| message | str | 所需要发送的消息 | 本项必填 |
| host_id | str | 在含有多层群聊嵌套的平台中(如 dodo、qq频道 )为最外层群聊号，具体详见 OlivOS 框架文档 | None |
注：
- 当 send_type 为 字符串 时, 可用内容为 'private' 或 'group' （具体详见 OlivOS 框架）
- 当 send_type 为 数字 时， 0 代表 私聊， 1 代表 群聊 
- host_id 主要用于平台消息，具体而言 若 传入参数 msg 中 群聊信息 host_id 不为 None，则必填
~~~python
# 向 id 为 12345 的 用户 私聊发送一条内容为 测试消息 的消息
api.send("private", "12345", "测试消息") 
api.send(0, "12345", "测试消息")      # 这样写也可以
#
# 向 id 为 12345 的 群组 发送一条内容为 测试消息 的消息
api.send("group", "12345", "测试消息") 
api.send(1, "12345", "测试消息")      # 这样写也可以
~~~

#### md5
返回md5摘要
~~~python
rv = api.md5(data)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| data | Any | 需要计算md5的信息（自动转化为字符串后计算utf-8的md5） | 本项必填 |
返回内容为 data 对应的 md5 字符串

#### data_dir
显示框架资源文件夹，即 ./plugin/data/ 的绝对路径
~~~python
rv = api.data_dir()
~~~
*本函数无入参*
返回内容为 ./plugin/data/ 文件夹绝对路径

#### mkdir
创建新文件夹，如果存在则忽略
~~~python
api.mkdir(path)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| path | str | 创建的文件夹路径 | 本项必填 |

#### web_download
获取 url 内容，保存到指定目录中
~~~python
api.web_download(url, path)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| url | str | 访问网站的 url | 本项必填 |
| path | str | 保存路径 | 本项必填 |

 ======

下方所有的功能需要 OlivOS Dice Core 模块支持
#### draw
从牌堆中抽卡
~~~python
rv = api.draw(deck)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| deck | str | 牌堆名称 | 本项必填 |

返回值：
- 如果牌堆不存在则返回 None
- 如果牌堆存在则返回具体抽到的牌面 str

#### onedice
使用 onedice 标准进行运算
~~~python
rv = api.onedice(string)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| string | str | 具体运算表达式 | 本项必填 |

返回值为一个结构体，其中具体内容详见 OlivOS 官方 onedice 标准库：
下方仅为一个目前的示例
~~~python
rd_para = api.onedice("3d6+5")
print(rd_para.originData)
if rd_para.resError != None:
    print(rd_para.resError)         # 错误信息
else:
    print(rd_para.resInt)           # 具体投掷的结果
    print(rd_para.resIntMax)
    print(rd_para.resIntMin)
    print(rd_para.resIntMaxType)
    print(rd_para.resIntMinType)
    print(rd_para.resDetail)        # 详细投掷流程内容
~~~

#### get_pc_hash
返回 OlivaDiceCore 中用户对应的 pc_hash
~~~python
rv = api.get_pc_hash(uid, platform)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| uid | str | 用户uid | 本项必填 |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
注：
- 如果 platform 为空，则默认为当前消息事件来源平台

#### get_card_data
返回 OlivaDiceCore 中用户人物卡数据
~~~python
rv = api.get_card_data(uid, platform)
rv = api.get_card_data(pc_hash=pc_hash)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |
注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash **必须**以 关键字形式 入参
~~~python
# 获取 uid 为 12345， 平台为 qq 的用户人物卡
rv = api.get_card_data("12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.get_card_data(pc_hash=pc_hash)
~~~
返回值：
- 一个{技能名: 技能值} 形式的键值对，为 pc 当前选中人物卡

#### get_pc_skill
返回 OlivaDiceCore 中用户人物技能
~~~python
rv = api.get_card_data(skillname, uid, platform)
rv = api.get_card_data(skillname, pc_hash=pc_hash)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| skillname | str | 技能名称 | 本项必填 |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |
注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash **必须**以 关键字形式 入参
- 技能名称**不会**自动转义（如 san -> 理智）
~~~python
# 获取 uid 为 12345， 平台为 qq 的用户人物卡中 名为 test 的技能值
rv = api.get_pc_skill('test', "12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.get_pc_skill('test', pc_hash=pc_hash)
~~~
返回值：
- 技能数值，默认值为 0 

#### set_pc_skill
返回 OlivaDiceCore 中用户人物技能
~~~python
rv = api.set_pc_skill(skillname, skillval, uid, platform, card_name=card_name)
rv = api.set_pc_skill(skillname, skillval, pc_hash=pc_hash, card_name=card_name)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| skillname | str | 技能名称 | 本项必填 |
| skillcal | int | 技能数值 | 本项必填 |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |
| card_name | str | 如果存在，则为设置技能指定的人物卡名称 | None |

注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash，card_name **必须**以 关键字形式 入参
- 技能名称**不会**自动转义（如 san -> 理智）
- 如果 card_name 存在，则对特定的人物卡进行操作，如果不存在，则操作当前选中的人物卡
~~~python
# 设置 uid 为 12345， 平台为 qq 的用户人物卡中 名为 test 的技能值
rv = api.set_pc_skill('test', 1, "12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.set_pc_skill('test', 1, pc_hash=pc_hash)
~~~
返回值：
- 恒为True

#### get_card_name
返回 OlivaDiceCore 中用户人物卡名称
~~~python
rv = api.get_card_name(uid, platform)
rv = api.get_card_name(pc_hash=pc_hash)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |

注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash **必须**以 关键字形式 入参
~~~python
# 获取 uid 为 12345， 平台为 qq 的用户当前选中人物卡名称
rv = api.set_pc_skill("12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.set_pc_skill(pc_hash=pc_hash)
~~~
返回值：
- 对应人物卡名称 str

#### switch_card
切换 OlivaDiceCore 中用户人物卡
~~~python
rv = api.switch_card(card_name, uid, platform)
rv = api.switch_card(card_name, pc_hash=pc_hash)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| card_name | str | 目标人物卡名称 | 本项必填 |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |

注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash **必须**以 关键字形式 入参
~~~python
# 切换 uid 为 12345， 平台为 qq 的用户当前选中人物卡
rv = api.switch_card("人物卡1", "12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.switch_card("人物卡1", pc_hash=pc_hash)
~~~
返回值：
- 如果成功则为 True
- 如果失败则为 False

#### set_card_name
设置 OlivaDiceCore 中用户选中人物卡名称
~~~python
rv = api.set_card_name(card_name, uid, platform)
rv = api.set_card_name(card_name, pc_hash=pc_hash)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| card_name | str | 人物卡名称 | 本项必填 |
| uid | str | 用户uid | None |
| platform | str | 平台信息（如 'dodo', 'qq'） | None |
| pc_hash | str | 用户 pc_hash | None |

注：
- 本方法有两种入参形式，如果使用 uid + platform 则类似 get_pc_hash
- 如果 pc_hash 参数有入参，则忽略 uid、 platfoem， 直接使用对应 pc_hash
- pc_hash **必须**以 关键字形式 入参
~~~python
# 设置 uid 为 12345， 平台为 qq 的用户当前选中人物卡名称为 人物卡1
rv = api.set_card_name("人物卡1", "12345", 'qq')
# 也可以用如下方式操作
pc_hash = api.get_pc_hash("12345", 'qq')
rv = api.set_card_name("人物卡1", pc_hash=pc_hash)
~~~
返回值：
- 如果成功则为 True
- 如果失败则为 False

 ======

## 其他信息
脚本文件所需导入的lib可以摆放在 ./plugin/data/ScriptLoad/lib 文件夹中
■
