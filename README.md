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

## 许可证信息
~~~
    Script Loader - 轻量级插件托盘 for OlivOS
    Copyright (C) 2022  Rainy Zhou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
~~~

## 具体api信息：
详见 api 文档 doc/API.md
