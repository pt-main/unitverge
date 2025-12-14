from basics import _UnitObject
from type_system import Utils
from exceptions import *











class Types:
    # list of all allowed in c types
    ALLOWED_INPUTS = [int, str, float, list]
    
    # simple patterns to just paste name
    # '$' will be replaced to name of variable
    INT = 'int'
    STR = 'char*'
    FLOAT = 'double'
    CHAR = 'char'
    
    INT_LIST = 'int_list'
    STR_LIST = 'chr_list'
    FLOAT_LIST = 'dbl_list'



class _Utils:
    def is_valid(data):
        return Utils.check_c_available(
            data,
            Types.ALLOWED_INPUTS
        )








class Code(_UnitObject):
    def __init__(self, code):
        self._code = [code]
        self._type = 'code'





class Variable(_UnitObject):
    def __init__(self, 
                 name: str, 
                 value, 
                 type: str):
        value = repr(_Utils.is_valid(value))
        typed = type.replace('$', name)
        self._code = [f'{typed}{value}']
        self._type = f'variable {name} {value}'




class Function(_UnitObject):
    def __init__(self, 
                 name, 
                 type: str, 
                 args: dict[str, str] = {}):
        args = ', '.join([f'{args[arg]} {arg}' for arg in args.keys()])
        self._code = [f'{type} {name} ({args})' + '{']