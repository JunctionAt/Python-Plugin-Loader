from org.bukkit.event import Listener


class NonExistentPriorityException(Exception):
    pass


class PythonListener(Listener, object):


    def register_event(self, func, event_class, priority='normal'):

        PRIORITIES = ["highest","high","normal","low","lowest","monitor"]
        if priority.lower() not in PRIORITIES:
            raise NonExistentPriorityException()

        if not hasattr(self, '_event_handlers'):
            self._event_handlers = list()

        self._event_handlers.append(dict(method=func, event=event_class, priority=priority.lower()))

__builtin__.PythonListener = PythonListener