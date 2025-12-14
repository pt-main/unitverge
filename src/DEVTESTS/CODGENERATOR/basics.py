class _UnitObject:
    '''
    Basic metaclass for unitverge [codegenerator] objects.
    '''
    def __init__(self):
        self._code: list[str] = []
        self._type = 'not stated'

    def get(self):
        # get compiled object code
        return '\n'.join(self._code)

    def id(self):
        # id for errors and notifications
        type = self._type.replace(' ', '_')
        id = hash(self)
        return f'UnitObject <type {type}> with hash [{id}] '