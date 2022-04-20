""" 
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
"""
import script_loader
import hashlib
import os
import urllib.parse
import requests

_SENDER_ROLE_MAP = ["private", "member", "admin", "owner"]

class MsgEvent:
    def __init__(self, plugin_event, re_result):
        self._plugin_event = plugin_event
        self._re_result = re_result
        self.msg = plugin_event.data.message
        self.hostId = plugin_event.data.host_id
        self.str = re_result.groups()
        self.msgType = None
        self.platform = plugin_event.platform['platform']
        if plugin_event.plugin_info["func_type"] == "group_message":
            self.msgType = 1
        elif plugin_event.plugin_info["func_type"] == "private_message":
            self.msgType = 0
        self.selfId = plugin_event.base_info["self_id"]
        self.fromUser = plugin_event.data.user_id
        if self.msgType == 1:
            self.fromGroup = plugin_event.data.group_id
            self.tergetId = self.fromGroup
        else:
            self.fromGroup = ""
            self.tergetId = self.fromUser
        self.flag_is_master = False
        self.fromUserInfo = 0
        if self.msgType == 1:
            if "role" in plugin_event.data.sender:
                self.fromUserInfo = _SENDER_ROLE_MAP.index(plugin_event.data.sender["role"])
            else:       # NOTE: 其他平台不能原生支持 role 发送者群聊权限字段，则默认为 1
                self.fromUserInfo = 1
        if script_loader.FLAG_HAS_OVODICE:  # 如果含有 ovodice， 则获取用户是否为 admin
            self.flag_is_master = script_loader.OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            script_loader.OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id, 'user',
                plugin_event.platform['platform']))

class PluginAPI:
    def __init__(self, proc, event):
        self.proc = proc
        self.plugin_event = event
        self.log = script_loader.other_misc.LogWrapper(proc.log)

    def send(self, send_type, target_id, message, host_id=None):
        self.plugin_event.send(send_type, target_id, message, host_id=host_id)

    def md5(self, data):
        hash_data =  hashlib.md5(str(data).encode("utf-8"))
        return hash_data.hexdigest()

    def dataDir(self):
        "显示框架资源文件夹，即 ./plugin/data/ 的绝对路径"
        ovo_root = os.path.abspath(".")
        return os.path.join(ovo_root,"plugin",'data')

    def mkDir(self, path):
        "创建新文件夹，如果存在则忽略"
        if not os.path.isdir(path):
            os.mkdir(path)

    def urlEncode(self, string):
        return urllib.parse.quote(string)

    def urlDecode(self, string):
        return urllib.parse.unquote(string)

    def fDownWebPage(self, url, path):
        "获取 url 内容，保存到指定目录中"
        r = requests.get(url=url)
        with open(path, mode="w", encoding=r.encoding) as file:
            file.write(r.text)

    # 以下功能需要 OlivOS Dice Core 模块支持
    def draw(self, string):
        "*需要 OlivaDiceCore* 抽取牌堆"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        bot_hash = self.plugin_event.bot_info.hash
        card = script_loader.OlivaDiceCore.drawCard.draw(string, bot_hash)
        return card

    def rd(self, string):
        "*需要 OlivaDiceCore* 以 onedice 标准投掷（返回 onedice RD）"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        rd = script_loader.OlivaDiceCore.onedice.RD(string)
        return rd

    def getPcSkill(self, uid, skillname, platform=None):
        "*需要 OlivaDiceCore*"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        if platform is None:
            platform = self.plugin_event.platform['platform']
        pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        r = script_loader.OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
            pchash, skillname
        )
        return r

    def setPcSkill(self, uid, skillname, skillval, cardname=None, platform=None):
        "*需要 OlivaDiceCore*"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        if platform is None:
            platform = self.plugin_event.platform['platform']
        pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        script_loader.OlivaDiceCore.pcCard.pcCardDataSetBySkillNameReplace(
            pchash, skillname, skillval, cardname
        )

    def getPcName(self, uid, platform=None):
        "*需要 OlivaDiceCore*"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        if platform is None:
            platform = self.plugin_event.platform['platform']
        pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        # pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid,
        #     self.plugin_event.platform['platform'])
        r = script_loader.OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
            pchash
        )
        return r

    def setPcName(self, uid, card_name, platform):
        "*需要 OlivaDiceCore*"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在，draw 功能不可用"
            )
        if platform is None:
            platform = self.plugin_event.platform['platform']
        pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        script_loader.OlivaDiceCore.pcCard.pcCardRebase(
            pchash, card_name
        )
