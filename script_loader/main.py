
import script_loader

class Event(object):
    def init(plugin_event, Proc):
        script_loader.other_misc.set_logger(Proc.log)
        script_loader.loader.script_load()

    def private_message(plugin_event, Proc):
        script_loader.loader.msg_run(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        script_loader.loader.msg_run(plugin_event, Proc)
