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
import os
import sys
import importlib
import traceback
import re

# dictScriptLoadAll = {}      # 脚本文件名称 ： 脚本文件对应command dict
script_all = None

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

class Loader:        # 脚本载入运行模块，参考 OlivOS/pluginAPI.py
    def __init__(self):
        self.str_trans = {92:"\\", 123: r"{{", 125: r"}}"}
        dir_root = script_loader.data.data_root
        mkdir(dir_root)
        mkdir(dir_root+"/script")
        mkdir(dir_root+"/lib")
        self.script_data_all = {}   # 脚本文件名称 ： 脚本文件对应command dict
        self.script_message_command = {}    # 正则匹配表示 ： 具体函数
        self.log = script_loader.other_misc.log_proc
        self.loadDictAll()

    def loadDictAll(self):

        dir_root = script_loader.data.data_root
        sys.path.append(dir_root+"/lib")
        sys.path.append(dir_root)
        plugin_lst = os.listdir(dir_root+"/script")
        if "__pycache__" in plugin_lst:
            plugin_lst.remove("__pycache__")
        # DEBUG:
        self.log.debug("plugin all: {0}", plugin_lst)
        
        for file in plugin_lst:
            try:
                if file.startswith("_"):
                    self.log.info("Script load [{0}] skiped: start with '_'", file)
                    continue
                if not file.endswith(".py"):
                    self.log.info("Script load [{0}] skiped:unknown module file", file)
                module_name = file[:-3]
                tmp_path = script_loader.data.data_module + module_name
                self.log.debug(tmp_path)
                script_tmp = importlib.import_module(tmp_path, ".")
                if hasattr(script_tmp, "COMMAND"):
                    command_dict = script_tmp.COMMAND
                    self.script_data_all[file] = command_dict
                    cmd_dict_this = {}
                    for restr, cmd_func in script_tmp.COMMAND.items():
                        # recompile = re.compile(restr)
                        cmd_dict_this[restr] = cmd_func
                    a = [f"{i}: {str(j).translate(self.str_trans)}" for i, j in enumerate(command_dict.keys(), 1)]
                    self.log.info("Script load [{0}]:\n{1}".format(
                            file,
                            "\n".join(a)
                        ))
            except Exception as err:
                self.log.error(
                        "Script load [{0}] skiped:{1}\n{2}",
                        file,
                        str(err),
                        traceback.format_exc()
                    )
            else:
                self.script_message_command.update(cmd_dict_this)     #[restr] = cmd_func

    def run(self, plugin_event, proc):
        success = True
        try:
            for restr, cmd_func in self.script_message_command.items():
                msg = plugin_event.data.message
                reobj = re.fullmatch(restr, msg)
                if reobj is None:
                    continue
                self.log.debug("run command [{0}]", cmd_func)
                api = script_loader.script_api.PluginAPI(proc, plugin_event)
                msg = script_loader.script_api.MsgEvent(plugin_event, reobj)
                reply = cmd_func(msg, api)
                if reply is not None:
                    plugin_event.reply(reply)
                break
                # self.script_message_command[restr] = cmd_func
        except Exception as err:
            err_tcb = traceback.format_exc()
            success = False
            err_str = str(err)
            self.log.error(f"Script runtime error:{err_str}\n{err_tcb}")
        if not success:
            raise script_loader.other_misc.ScriptRuntimeError(
                err_str,
                err_tcb
            )

def script_load():
    global script_all
    script_all = Loader()

def msg_run(plugin_event, Proc):
    try:
        script_all.run(plugin_event, Proc)
    except script_loader.other_misc.BasicScriptException as err:
        err_str, tcb = err.args
        plugin_event.reply(f"script error occurred: {err_str}\n{tcb}")
