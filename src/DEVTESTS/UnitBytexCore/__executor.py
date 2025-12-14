from UnitVerge.core.UnitBytexCore import (
    OutputError, 
    MemorySystemError, 
    PointError, 
    UnknownSyntax,
    VirtualMachineBasics
)




















class VirtualMachine:
    def __init__(self):
        self.vm = VirtualMachineBasics()
    
    def compile_type(self, data):
        data = str(data).replace('~', ' ').replace('``', '~')
        if data.isdigit():
            return int(data)
        try:
            return float(data)
        except ValueError:
            return data

    def compile_int(self, integer):
        inp = float(str(integer)
                  .replace(
                      '?', str(self.vm.get())
                      )
                  .replace(
                      '<', str(self.vm.tape[max(0, self.vm.position-1)])
                      )
                  .replace(
                      '>', str(self.vm.tape[self.vm.position+1])
                    ))
        return inp
    
    def jump(self, pos):
        pos = int(pos)
        self.vm.jump(pos)
    
    def set(self, data):
        data = self.compile_type(data)
        self.vm.set(data)
    
    def next(self, iters: int = 1):
        iters = int(iters)
        for i in range(iters):
            self.vm.next()
    
    def prev(self, iters: int = 1):
        iters = int(iters)
        for i in range(iters):
            self.vm.prev()

    def out(self): # out 
        print(self.vm.get(), end='')
    
    def otn(self): # out next
        print('\n')
    
    def otc(self): # out char
        try: print(
            chr(int(self.vm.get())), 
            end=''
        )
        except TypeError:
            OutputError(f'Invalid data of section to out char: {self.vm.get()}.')
    
    def ott(self): # out type now
        print(type(self.vm.get()), end='')
        
    def otp(self): # out current position
        print(self.vm.position, end='')
    
    def print(self, data):
        print(
            self.compile_type(data), 
            end=''
        )
    
    def instr(self): # input string
        data = input()
        try: 
            data = str(data)
            self.vm.set(data)
        except TypeError:
            OutputError(f'Invalid for input: {data} - type must be str.')
    
    def inint(self): # input integer
        data = input()
        try: 
            data = int(data)
            self.vm.set(data)
        except TypeError:
            OutputError(f'Invalid for input: {data} - type must be int.')
        
    def innum(self): # input any numeric data
        data = input()
        try: 
            data = float(data)
            self.vm.set(data)
        except TypeError:
            OutputError(f'Invalid for input: {data} - type must be number.')
    
    def plus(self, x): # plus any data
        self.vm.tape[
                self.vm.position
        ] += self.compile_type(x)
    
    def plus_int(self, x):
        self.vm.tape[
                self.vm.position
        ] += self.compile_int(x)

    def sub(self, x):
        self.vm.tape[
                self.vm.position
        ] -= self.compile_int(x)
    
    def div(self, x):
        self.vm.tape[
                self.vm.position
        ] /= self.compile_int(x)
    
    def mul(self, x):
        self.vm.tape[
                self.vm.position
        ] *= self.compile_int(x)
    
    def pow(self, x):
        self.vm.tape[
                self.vm.position
        ] **= self.compile_int(x)

     


























class Machine(VirtualMachine):
    def __init__(self):
        super().__init__()
        self.variables = {}   
    
    def new_var(self, name, value, type: str = 'basic'):
        value = self.compile_type(value)
        self.variables[name] = {'val': value, 'typ': type}
        
    def get_from_var(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise MemorySystemError(
        f"Variable '{name}' is not found."
            )

    def set_var(self, name, value):
        value = self.compile_type(value)
        if name in self.variables:
            var = self.variables[name]
            if var['typ'] != 'const':
                self.variables[name]['val'] = value
            else:
                raise MemorySystemError(
        f"Variable '{name}' is not muttable."
            )
        else:
            raise MemorySystemError(
        f"Variable '{name}' is not found."
            )
    
    def swap(self, pos):
        pos = self.compile_type(pos)
        curr = self.vm.get()
        oth = self.vm.tape[pos]
        self.vm.set(oth)
        self.vm.tape[pos] = curr
    
    def copy(self, pos):
        pos = self.compile_type(pos)
        curr = self.vm.get()
        self.vm.tape[pos] = curr




























class Executor(Machine):
    def __init__(self):
        super().__init__()
        self.points_code = {}
        self.points = []
    
    
    
    def exec(self, command: list):
        cmd = command[0]
        args = command[1:]
        
        def err_syntax(other = ''):
                raise UnknownSyntax(f"Unknown syntax: {' '.join(command)}. " + str(other))
        def check_args_len(length):
            if len(args) != length:
                err_syntax(
                    f'\nBad arguments length ({len(args)} while must be {length}).'
            )
        
        if cmd.startswith('p:'):
            name = cmd[2:]
            if name in self.points:
                # add to point code from command
                self.points_code[name].append(args) 
            else:
                # if name of point is not found
                raise PointError(f'Unknown name to add code to point: {name}')
        else:
            match cmd:
                case 'jump':
                    check_args_len(1)
                    arg = args[0]
                    self.jump(arg)
                
                case 'set':
                    check_args_len(1)
                    arg = args[0]
                    self.set(arg)
                
                case '>':
                    self.next()
                
                case '<':
                    self.prev()
                
                case 'next':
                    check_args_len(1)
                    arg = args[0]
                    self.next(arg)
                
                case 'prev':
                    check_args_len(1)
                    arg = args[0]
                    self.prev(arg)
                
                case 'out':
                    check_args_len(1)
                    arg = args[0]
                    if arg in ('.', 'data', 'd'):
                        self.out()
                    elif arg in ('next', 'n'):
                        self.otn()
                    elif arg in ('char', 'c'):
                        self.otc()
                    elif arg in ('type', 't'):
                        self.ott()
                    elif arg in ('pos', 'p', '?'):
                        self.otp()
                    else:
                        err_syntax(f'Unknown out type: {arg}.')
                    
                case 'op': # operation
                    check_args_len(2)
                    arg = args[0]
                    x = args[1]
                    if arg in ('plus'):
                        self.plus(x)
                    elif arg in ('+'):
                        self.plus_int(x)
                    elif arg in ('-'):
                        self.sub(x)
                    elif arg in ('/'):
                        self.div(x)
                    elif arg in ('*'):
                        self.mul(x)
                    elif arg in ('^'):
                        self.pow(x)
                    else:
                        err_syntax(f'Unknown op type: {arg}.')
                
                case 'work':
                    arg = args[0]
                    if arg == 'ife':
                        self.work_ife(args[1], args[2:])
                    elif arg == 'ifl':
                        self.work_ifl(args[1], args[2:])
                    elif arg == 'ifm':
                        self.work_ifm(args[1], args[2:])
                    elif arg == 'ifme':
                        self.work_ifme(args[1], args[2:])
                    elif arg == 'ifle':
                        self.work_ifle(args[1], args[2:])
                    else:
                        err_syntax(f'Unknown work type: {arg}.')
                
                case 'in':
                    check_args_len(1)
                    arg = args[0]
                    if arg in ('str', 's'):
                        self.instr()
                    elif arg in ('int', 'i'):
                        self.inint()
                    elif arg in ('num', 'n'):
                        self.innum()
                    else:
                        err_syntax(f'Unknown input type: {arg}.')
                
                case 'print':
                    arg = ' '.join(args)
                    self.print(arg)
                
                case 'point': # declarate point
                    name = args[0]
                    self.points.append(name)
                    self.points_code[name] = [['#', 'start']]
                
                case 'goto': # use point
                    name = args[0]
                    if name in self.points_code.keys():
                        for linelocal in self.points_code[name]:
                            self.exec(linelocal)
                    else:
                        raise PointError(f'Unknown name for go to point: {name}')
                
                case 'copy':
                    check_args_len(1)
                    arg = args[0]
                    self.copy(arg)
                
                case 'swap':
                    check_args_len(1)
                    arg = args[0]
                    self.swap(arg)
                
                case 'mem':
                    arg = args[0]
                    if arg == 'var':
                        check_args_len(3)
                        self.new_var(args[1], args[2])
                    elif arg == 'const':
                        check_args_len(3)
                        self.new_var(args[1], args[2], 'const')
                    elif arg == 'edit':
                        check_args_len(3)
                        self.set_var(args[1], args[2])
                    elif arg == 'temp':
                        self.temp_use(args[1], args[2:])
                    else:
                        err_syntax(f'Unknown mem arg: {arg}.')
                case '#':
                    pass
                
                case _:
                    if str(cmd).strip() != '':
                        err_syntax()
        
    
    
    def work_ife(self, condition, command: list): # work if equal
        condition = self.compile_type(condition)
        if self.vm.get() == condition:
            self.exec(command)
        
    def work_ifm(self, condition, command: list): # work if more
        condition = self.compile_type(condition)
        if self.vm.get() > condition:
            self.exec(command)
    
    def work_ifl(self, condition, command: list): # work if less
        condition = self.compile_type(condition)
        if self.vm.get() < condition:
            self.exec(command)
        
    def work_ifme(self, condition, command: list): # work if more or equal
        condition = self.compile_type(condition)
        if self.vm.get() >= condition:
            self.exec(command)
        
    def work_ifle(self, condition, command: list): # work if less or equal
        condition = self.compile_type(condition)
        if self.vm.get() <= condition:
            self.exec(command)
        
    def temp_use(self, var, command: list):
        var_name = self.compile_type(var)
        pos = self.vm.position
        self.jump(0)
        self.set(self.get_from_var(var_name)['val'])
        self.exec(command)
        self.jump(pos)
        