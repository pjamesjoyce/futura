import wrapt
from .proxy import WurstDatabase, WurstProcess

class FuturaSession:
    def __init__(self):
        self.session_info = []

    def clear(self):
        self.session_info = []

    def create_recipe(self):
        pass


def futura_action(session):
    @wrapt.decorator
    def inner(wrapped, instance, args, kwargs):
        signature = {
            'function': wrapped.__name__,
            'instance': instance.__repr__(),
            'args': args,
            'kwargs': kwargs
        }
        # for a, n in enumerate(args):
        #
        #     if isinstance(a, WurstDatabase):
        #         print('{} calls a WurstDatabase'.format(wrapped.__name__))
        #         print(a.__repr__())
        #         a[n] = a.__repr__()
        #     elif isinstance(a, WurstProcess):
        #         print('{} calls a WurstProcess'.format(wrapped.__name__))
        #         print(a.__repr__())
        #         a[n] = a.__repr__()

        session.session_info.append(signature)

        return wrapped(*args, **kwargs)
    return inner

