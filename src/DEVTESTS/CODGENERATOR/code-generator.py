from unit import Unit
from stdlib import std

class CodeGenerator:
    def __init__(self):
        self.code = [std]
    
    def parse_unit(self, unit: Unit):
        for comm in unit._commands:
            self.code.append(comm.get())
    
    def get(self):
        return '\n'.join(self.code)



cgn = CodeGenerator()
ctx = Unit()
with ctx.func('test', 'int') as f:
    ctx.code('int test = 10;')
cgn.parse_unit(ctx)
print(cgn.get())