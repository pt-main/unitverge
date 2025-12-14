'''
# UnitBytex language

System assembler-like language for UnitVerge framework programms.

Executing in Vurtual machine.

By pt.

## Bytex 0.2
'''




from UnitVerge.core.UnitBytexCore import Parser
from .__executor import Executor
import sys

# for cycles
sys.setrecursionlimit(512_000)



class Interpreter:
    def __init__(self):
        self.exec = Executor()
        self.points_code = {}
        self.points = []
    
    def execute(self, code):
        code_spl = Parser(code) # splitted code
        for line in code_spl:
            self.exec.exec(line)
        return self




def execute(code: str) -> int | None:
    Interpreter().execute(code)
    return 0




if __name__ == '__main__':
    execute('''
point input; p:input jump 1234;
point basic; p:basic jump 0;
point temp; p:temp jump 8421;
point main;
    p:main goto temp;
    p:main copy 1235;
    p:main goto input;
    p:main op * >;
    p:main out .;
goto temp; print Введите число 1:~; in num; goto basic;
goto input; print Введите число 2:~; in num; goto basic;
goto main;
>;
    ''')