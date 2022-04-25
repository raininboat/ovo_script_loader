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
log_proc = None

class LogWrapper:
    def __init__(self, proc_log):
        self.log = proc_log

    def trace(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(-1, str(msg).format(*args,**kwargs))
        else:
            self.log(-1, str(msg))

    def debug(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(0, str(msg).format(*args,**kwargs))
        else:
            self.log(0, str(msg))

    def note(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(1, str(msg).format(*args,**kwargs))
        else:
            self.log(1, str(msg))

    def info(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(2, str(msg).format(*args,**kwargs))
        else:
            self.log(2, str(msg))

    def warn(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(3, str(msg).format(*args,**kwargs))
        else:
            self.log(3, str(msg))

    def error(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(4, str(msg).format(*args,**kwargs))
        else:
            self.log(4, str(msg))

    def fatal(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(5, str(msg).format(*args,**kwargs))
        else:
            self.log(5, str(msg))

    def __call__(self, *args, **kwds):
        self.log(*args, **kwds)

def set_logger(proc_log):
    global log_proc
    log_proc = LogWrapper(proc_log)
    return log_proc



class BasicScriptException(UserWarning):
    "这是所有本插件原生引发的异常的基类"

class OVODiceCoreNotFoundError(BasicScriptException):
    "OlivaDiceCore 未找到，且使用了依赖其的功能"

class ScriptRuntimeError(BasicScriptException):
    "脚本文件运行过程中发生异常"

