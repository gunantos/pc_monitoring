
class _Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


TYPEDATA = _Enum(['INFO', 'GENERAL_INFO', 'CPU', 'DISK', 'NETWORK'])
