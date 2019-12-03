from pprint import pformat


class WurstDatabase(list):
    def __init__(self, *args, **kwargs):
        super(WurstDatabase, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "WurstDatabase with {} items".format(len(self))


class WurstProcess(dict):
    def __init__(self, *args, **kwargs):
        super(WurstProcess, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "WurstProcess: {} ({}) [{}]".format(self['name'], self['unit'], self['location'])


class WurstFilter:
    def __init__(self, func, x=None, signature=None):
        self.func, self.x = func, x
        self.description = None
        self.signature = signature

    def __call__(self, x):
        return self.func(x)

    def __repr__(self):
        if self.signature:
            detail = self.signature
        else:
            detail = str(self.func)

        return "WurstFilter: {}".format(detail)


class WurstFilterSet(list):
    def __init__(self, *args, **kwargs):
        super(WurstFilterSet, self).__init__(*args, **kwargs)
        self.description = None

    def __repr__(self):
        return "WurstFilterSet: {}".format(pformat([x for x in self]))
