# ovo_script_loader
为轻量级脚本插件设计的 OlivOS 脚本读取托盘

## 概述
本仓库仿照 [[Oliva|2]喧闹测试](https://wiki.dice.center/Chaos_Manual.html) （以前 lua 脚本扩展文件）的脚本编写方案，为 OlivOS 提供一个更加易用、更加简洁的脚本开发环境，使得轻量级扩展插件无需过多关注和框架间的交互，将重点放在功能实现上，实现过程中有参考 [OlivOS 源码](https://github.com/OlivOS-Team/OlivOS)

## 示例
一个示例脚本文件：

![EFQC0D3YPJUZB`CIJNBZ$DU](https://user-images.githubusercontent.com/74845844/163611782-1f58f683-8670-46d2-a921-7247364850b8.png)

 ======
如图所示，`COMMAND` 为所有映射到插件的功能函数，用正则形式匹配， `msg` 为所有关于本条消息的信息（类似 `喧闹测试` 中的 `Msg`）
`api` 为所有本项目提供的接口（框架的 `plugin_event` 和 `proc` 也在其中）

## 目录结构
~~~
* plugin/data   data 文件夹
+- * ScriptLoad   
   |
   * lib     所有脚本文件需载入的模块
   +-* xxx.py
   * script
   +-* xxx.py 所有的脚本文件

注： 脚本文件中以 _ 开头的项目自动跳过（方便在调试时临时关闭部分脚本文件）
~~~
## 相关依赖项
[OlivaDiceCore](https://github.com/OlivOS-Team/OlivaDiceCore) 非必须
如果不存在则其中部分功能将不可用

## 传入参数
### msg
`msg`中含有事件相关的各类信息
成员如下：
| 成员名称 | 数据类型 | 说明 |
| --- | --- | --- |
| msg | `str` | 消息全文 |
| str | `tuple` | 所有匹配的信息组合 |
| msgType | `int` | 消息类型 `0` 为 私聊消息，`1` 为群聊消息 |
| platform | `str` | 消息所属平台 |
| hostId | `str` or `None` | 消息所属频道号（类似 dodo 等平台适用，详见ovo手册） |
| selfId | `str` | 机器人id |
| fromUser | `str` | 消息发送用户id |
| fromGroup | `str` | 消息所在群聊id（私聊则为 ""） |
| targetId | `str` | 如果是群聊，则为群聊id；如果是私聊，则为用户id |
| fromUserInfo | `int` | 本条消息发送者的群内权限,`0`为私聊，`1`为群员，`2`为管理员，`3`为群主（如果在类似 dodo 等平台上，无法获取 群内权限 信息，则私聊为`0`群聊为`1`） |
| flag_is_master | `bool` | 是否为 `OlivaDice` 管理员（如果未安装该插件则默认为 `False`） |

### api
`api` 为实现的功能
成员如下：
#### proc
OlivOS 框架 Proc
#### plugin_event
OlivOS 框架事件 plugin_event
#### log
此为 OlivOS 框架 proc_log 的封装，添加诸如 `trace` `debug` `info` `note` `warning` `error` `fatal` 等方法，便于直接使用，也可以直接调用，使用原版框架 log 函数
~~~python
api.log.info("这是一条示例信息{0},{1},{kwarg0},{kwarg1}", arg0, arg1,kwarg0=kwarg0,kwarg1=kwarg1)
~~~
#### send
发送消息 (详见框架接口)
~~~python
api.send(send_type, target_id, message)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| send_type | `str` | 用于指定发送目标的类型 | |
| target_id | `str` | 发送目标的ID | |
| message | `str` | 所需要发送的消息 | |
| host_id | `str` | 发送目标的所属HOST ID | `None` |

#### md5
返回md5摘要
~~~python
rv = api.md5(data)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| data | Any | 需要计算md5的信息（自动转化为字符串后计算utf-8的md5） | |

#### dataDir
显示框架资源文件夹，即 ./plugin/data/ 的绝对路径
~~~python
rv = api.dataDir()
~~~
*本函数无入参*
| 返回值类型 | 说明 | 缺省 |
| --- | --- | --- |
| `str` | ./plugin/data/ 文件夹绝对路径 | |

#### mkDir
创建新文件夹，如果存在则忽略
~~~python
api.mkDir(path)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| path | `str` | 创建的文件夹路径 | |

#### fDownWebPage
获取 url 内容，保存到指定目录中
~~~python
api.fDownWebPage(path)
~~~
| 参数名称 | 数据类型 | 说明 | 缺省 |
| --- | --- | --- | --- |
| path | `str` | 创建的文件夹路径 | |

 ======

下方所有的功能需要 Oliva Dice Core 模块支持
#### draw
#### rd
#### getPcSkill
#### setPcSkill
#### getPcName
#### setPcName
