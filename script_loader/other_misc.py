log_proc = None

class LogWrapper:
    def __init__(self, proc_log):
        self.log = proc_log

    def trace(self, msg: str, *args, **kwargs):
        self.log(-1, msg.format(*args,**kwargs))

    def debug(self, msg: str, *args, **kwargs):
        self.log(0, msg.format(*args,**kwargs))

    def note(self, msg: str, *args, **kwargs):
        self.log(1, msg.format(*args,**kwargs))

    def info(self, msg: str, *args, **kwargs):
        self.log(2, msg.format(*args,**kwargs))

    def warn(self, msg: str, *args, **kwargs):
        self.log(3, msg.format(*args,**kwargs))

    def error(self, msg: str, *args, **kwargs):
        self.log(4, msg.format(*args,**kwargs))

    def fatal(self, msg: str, *args, **kwargs):
        self.log(5, msg.format(*args,**kwargs))

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

