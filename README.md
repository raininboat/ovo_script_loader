# ovo_script_loader
为轻量级脚本插件设计的 OlivOS 脚本读取托盘

本仓库仿照 [[Oliva|2]喧闹测试](https://wiki.dice.center/Chaos_Manual.html) （以前 lua 脚本扩展文件）的脚本编写方案，为 OlivOS 提供一个更加易用、更加简洁的脚本开发环境，使得轻量级扩展插件无需过多关注和框架间的交互，将重点放在功能实现上

一个示例脚本文件：<br>
![EFQC0D3YPJUZB`CIJNBZ$DU](https://user-images.githubusercontent.com/74845844/163611782-1f58f683-8670-46d2-a921-7247364850b8.png)
 ======
如图所示，`COMMAND` 为所有映射到插件的功能函数，用正则形式匹配， `msg` 为所有关于本条消息的信息（类似 `喧闹测试` 中的 `Msg`）
`api` 为所有本项目提供的接口（框架的 `plugin_event` 和 `proc` 也在其中）
