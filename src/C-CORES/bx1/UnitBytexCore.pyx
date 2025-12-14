from untvgdev.core.bx1.UnitBytexDevConfig import Debug


# ===========
# CYTHON CODE
# ===========

debug = Debug.core

cdef void debugprint(values):
    if debug:
        if isinstance(values, (list, tuple)):
            print(*values)
        else:
            print(values)


cdef class VM_C_realized:
    def __init__(self):
        self.tape = self.create(512_000)
        self.position = round(
            len(self.tape)/2.0
        )
    
    cdef dict[int, int] create(self, int length = 1000):
        tape = {}
        cdef int i
        for i in range(length):
            tape[i] = 0
        return tape
    
    cpdef void jump(self, int pos):
        self.position = pos
        debugprint(f'Jump to {pos}')
    
    cdef inline void fast_next(self):
        self.position += 1  
        debugprint(f'Moved to {self.position}')
    
    cdef inline void fast_prev(self):
        self.position -= 1  
        debugprint(f'Moved to {self.position}')
    
    cpdef void next(self):
        if self.position < len(self.tape) - 1:
            self.fast_next()
        else:
            raise MemoryError("End of tape")
    
    cpdef void prev(self):
        if self.position > 0:
            self.fast_prev()
        else:
            raise MemoryError("End of tape")
    
    cpdef void set(self, data):
        self.tape[
            self.position
        ] = data
        debugprint(f'Set {data} to {self.position}')
    
    def get(self):
        debugprint(f'Get data from {self.position}')
        return self.tape[
            self.position
        ]

    def recreate(self, int length):
        self.tape = self.create(length)
        self.position = round(
            len(self.tape)/2.0
        )




cdef list c_parser(code: str):
    return list(
    map(
        lambda command: str(command).strip().split(' '),
        str(code).split(';')
    )        
)














# ==========
# PYTHON API
# ==========


class UnknownSyntax(Exception):pass
class OutputError(Exception):pass
class PointError(Exception):pass
class MemorySystemError(Exception):pass
class InterpreteError(Exception):pass


class VirtualMachineBasics(VM_C_realized): pass
def Parser(code: str): return c_parser(code)