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

import hashlib
import os
import script_loader
# import urllib.parse
import requests
import OlivOS           # pylint: disable=import-error

_SENDER_ROLE_MAP = ["private", "member", "admin", "owner"]


class MsgEvent:
    "传入托盘中轻量级插件的消息数据类 msg"
    def __init__(self, plugin_event, re_result):
        self.msg = ""
        self.str = []
        self.platform = None
        self.msg_type = None
        self.self_id = None
        self.self_hash = None
        self.user_id = None
        self.group_id = None
        self.host_id = None
        self.target_id = None
        self.user_info = None
        self.sender = {}
        self.flag_is_master = None
        self.flag_has_olivadice = None
        self._plugin_event = plugin_event
        self._re_result = re_result

        self.__set_conf()

    def __set_conf(self):
        plugin_event = self._plugin_event
        self.msg = plugin_event.data.message
        self.str = self._re_result.groups()
        self.platform = plugin_event.platform['platform']
        if hasattr(plugin_event.data, "sender"):
            self.sender = plugin_event.data.sender
        if plugin_event.plugin_info["func_type"] == "group_message":
            self.msg_type = 1
        elif plugin_event.plugin_info["func_type"] == "private_message":
            self.msg_type = 0
        self.self_id = plugin_event.bot_info.id
        self.self_hash = plugin_event.bot_info.hash
        self.user_id = plugin_event.data.user_id
        if self.msg_type == 1:
            self.group_id = plugin_event.data.group_id
            self.target_id = self.group_id
            self.host_id = plugin_event.data.host_id
        else:
            self.terget_id = self.user_id
        if self.msg_type == 1:
            if "role" in plugin_event.data.sender:
                self.user_info = _SENDER_ROLE_MAP.index(
                    plugin_event.data.sender["role"])
            else:       # NOTE: 其他平台不能原生支持 role 发送者群聊权限字段，则默认为 1
                self.user_info = 1
        elif self.msg_type == 0:
            self.user_info = 0
        self.flag_has_olivadice = script_loader.FLAG_HAS_OVODICE
        if script_loader.FLAG_HAS_OVODICE:  # 如果含有 ovodice， 则获取用户是否为 master
            self.flag_is_master = script_loader.OlivaDiceCore.ordinaryInviteManager.isInMasterList(
                plugin_event.bot_info.hash,
                script_loader.OlivaDiceCore.userConfig.getUserHash(
                    plugin_event.data.user_id, 'user',
                    plugin_event.platform['platform']))
        else:
            self.flag_is_master = False

class PluginAPI:
    def __init__(self, proc, event):
        self.proc = proc
        self.plugin_event = event
        self.flag_has_olivadice = script_loader.FLAG_HAS_OVODICE
        self.log = script_loader.other_misc.LogWrapper(proc.log)

    @property
    def version(self):
        return self.__version_info_class()

    def reply(self, message):
        "直接按照原路径回复消息"
        self.log.trace(f"api.reply\n{message}")
        self.plugin_event.reply(message)

    def send(self, send_type, target_id, message, host_id=None):
        if isinstance(send_type, int) :
            # 将 int 形式的发送类型自动转换为具体的实现
            send_type = ["private", "group"][send_type]
        self.log.trace(f"api.send\n{send_type}, {target_id}, {message}, {host_id}")
        self.plugin_event.send(send_type, target_id, message, host_id=host_id)

    def md5(self, data):
        "返回对应 data 的 md5 值"
        hash_data = hashlib.md5(str(data).encode("utf-8"))
        ret = hash_data.hexdigest()
        self.log.trace(f"api.md5\n=> {ret}")
        return ret

    def data_dir(self):
        "显示框架资源文件夹，即 ./plugin/data/ 的绝对路径"
        ovo_root = os.path.abspath(".")
        ret = os.path.join(ovo_root, "plugin", 'data')
        self.log.trace(f"api.data_dir\n=>{ret}")
        return ret

    def mkdir(self, path):
        "创建新文件夹，如果存在则忽略"
        if not os.path.isdir(path):
            os.mkdir(path)
        self.log.trace(f"api.mkdir\n{path}")

    # Note: 对于url解析会有很多问题，而且 urllib 库外部也直接可以调用，故不提供 api
    # def urlEncode(self, string):
    #     "url 编码，目前没有做对域名部分的忽略"
    #     return urllib.parse.quote(string)

    # def urlDecode(self, string):
    #     return urllib.parse.unquote(string)

    def web_download(self, url, path, kwargs=None):
        "获取 url 内容，保存到指定目录中"
        if kwargs is None:
            kwargs = {}
        r = requests.get(url=url, **kwargs)
        with open(path, mode="wb") as file:
            file.write(r.content)
        self.log.trace(f"api.web_download\n{url} - {path}")
        return r.status_code

    # NOTE: 以下功能需要 OlivOS Dice Core 模块支持
    def draw(self, deck):
        "*需要 OlivaDiceCore* 抽取牌堆"
        self.__check_ovodice()
        bot_hash = self.plugin_event.bot_info.hash
        card = script_loader.OlivaDiceCore.drawCard.draw(deck, bot_hash)
        self.log.trace(f"api.draw {deck}\n=> {card}")
        return card

    def onedice(self, string):
        "*需要 OlivaDiceCore* 以 onedice 标准投掷（返回 onedice RD）"
        self.__check_ovodice()
        rd = script_loader.OlivaDiceCore.onedice.RD(string)
        rd.roll()
        self.log.trace(f"api.onedice string={string}\n=>{rd}")
        return rd

    def get_pc_hash(self, uid, platform=None):
        "*需要 OlivaDiceCore 组件* 返回其存储的user对应hash"
        self.__check_ovodice()
        if platform is None:
            platform = self.plugin_event.platform['platform']
        pchash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        self.log.trace(f"api.get_pc_hash uid={uid}, platform={platform}\n=>{pchash}")
        return pchash

    # def get_card_selection_key(self, uid=None, platform=None, pc_hash=None):
    #     "*需要 OlivaDiceCore* 获取用户的选择卡名称"
    #     self.__check_ovodice()
    #     pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
    #     card_key = script_loader.OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash)
    #     self.log.trace(f"api.get_pc_card_selection_key pc_hash={pc_hash}\n=>{card_key}")
    #     return card_key

    def get_card_data(self, uid=None, platform=None, pc_hash=None):
        "*需要 OlivaDiceCore* 获取用户的选择卡具体数据"
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        card_data = script_loader.OlivaDiceCore.pcCard.pcCardDataGetByPcName(pc_hash)
        self.log.trace(f"api.get_pc_card pc_hash={pc_hash}\n=>{card_data}")
        return card_data

    def get_pc_skill(self, skillname, uid=None, platform=None, pc_hash=None):
        "*需要 OlivaDiceCore*"
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        ret = script_loader.OlivaDiceCore.pcCard.pcCardDataGetBySkillName(pc_hash, skillname)
        self.log.trace(f"api.get_pc_skill pc_hash={pc_hash}\n=>{ret}")
        return ret

    def set_pc_skill(self, skillname, skillval, uid=None, platform=None, pc_hash=None, card_name=None):
        "*需要 OlivaDiceCore* 设置人物卡技能，注意技能名称不会自动重定向 "
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        if card_name is None:
            card_name = script_loader.OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash)
        script_loader.OlivaDiceCore.pcCard.pcCardDataSetBySkillNameReplace(
            pc_hash, skillname, skillval, card_name
        )
        self.log.trace(f"api.set_pc_skill pc_hash={pc_hash}")
        return True

    def get_card_name(self, uid=None, platform=None, pc_hash=None):
        "*需要 OlivaDiceCore*"
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        ret = script_loader.OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash)
        self.log.trace(f"api.get_pc_name pc_hash={pc_hash}\n=>{ret}")
        return ret

    def switch_card(self, card_name, uid=None, platform=None, pc_hash=None):
        "*需要 OlivaDiceCore*"
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        ret = script_loader.OlivaDiceCore.pcCard.pcCardDataSetSelectionKey(pc_hash, card_name)
        self.log.trace(f"api.switch_card pc_hash={pc_hash}\n=>{ret}")
        return ret

    def set_card_name(self, card_name, uid=None, platform=None, pc_hash=None):
        "*需要 OlivaDiceCore*"
        self.__check_ovodice()
        pc_hash = self.__get_pc_hash(uid, platform, pc_hash)
        flag_pcname_valid =  script_loader.OlivaDiceCore.pcCard.checkPcName(card_name)
        if not flag_pcname_valid:
            return False
        script_loader.OlivaDiceCore.pcCard.pcCardRebase(pc_hash, card_name)
        self.log.trace(f"api.change_card_name pc_hash={pc_hash}")
        return True

    # WARN: 以下内容为内部方法实现，不推荐外部调用. 如强行使用发生一切问题概不负责
    def __check_ovodice(self):
        "检查ovo模块是否存在"
        if not script_loader.FLAG_HAS_OVODICE:
            self.log.error("OlivaDiceCore 不存在，功能不可用")
            raise script_loader.other_misc.OVODiceCoreNotFoundError(
                "OlivaDiceCore 不存在, 功能不可用"
            )
        return True

    def __get_pc_hash(self, uid, platform, pc_hash):
        "获取对应 pc_hash，如果已填写 直接返回 pc_hash"
        if pc_hash is None:
            if platform is None:
                platform = self.plugin_event.platform['platform']
            if uid is None:
                raise ValueError("必须提供 uid 或 pc_hash")
            pc_hash = script_loader.OlivaDiceCore.pcCard.getPcHash(uid, platform)
        return pc_hash

    class __version_info_class:
        def __init__(self) -> None:
            self.olivos_svn = OlivOS.infoAPI.OlivOS_SVN
            self.olivos_version = OlivOS.infoAPI.OlivOS_Version
            self.script_loader_svn = script_loader.SCRIPT_LOADER_SVN
            self.script_loader_version = script_loader.SCRIPT_LOADER_VERSION

        def __str__(self) -> str:
            return f"<version info - olivos_svn: {self.olivos_svn}; olivos_version: {self.olivos_version}; script_loader_svn: {self.script_loader_svn}; script_loader_version: {self.script_loader_version}>"
