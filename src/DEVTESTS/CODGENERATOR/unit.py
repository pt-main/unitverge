from objects import _UnitObject, Variable, Function, Code

class Unit:
    def __init__(self):
        self._commands: list[_UnitObject] = []
    
    def func(self, name: str, type: str = 'void', args: dict[str] = {}):
        class func_class:
            def __init__(self):pass
            @staticmethod
            def __enter__():
                self.instruction(Function(name, type, args))
            @staticmethod
            def __exit__(*args, **kwargs):
                self.instruction(Code('return 0;')) \
                    if type == 'int' else None
                self.instruction(Code('}'))
        return func_class()
    
    def var(self, name: str, value: any, type: str):
        self.instruction(
            Variable(name, value, type)
        )
        return self
    
    def code(self, line: str):
        self.instruction(Code(line))
        return self
        
    def instruction(self, instruction: _UnitObject):
        self._commands.append(instruction)
        return self