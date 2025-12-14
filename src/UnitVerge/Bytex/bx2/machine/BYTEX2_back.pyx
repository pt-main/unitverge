class VMEXCEPTION(Exception): pass

cdef class _Memory:
    cdef int __std_params, __std_section_size, __std_registers
    cdef list _regs
    cdef dict _hands, params
    cdef str _hand
    cdef int _cursor_idx, _pointer_idx
    
    def __init__(self):
        self.__std_params = 256
        self.__std_section_size = 4096
        self.__std_registers = 1024
        
        self._regs = [[0] * self.__std_section_size 
                     for _ in range(self.__std_registers)]
        
        self._hands = {'main': [0, 0], 'temp': [0, 0]}
        self._hand = 'main'
        self.params = {i: 0 for i in range(self.__std_params)}
        
        self._update_cached_indices()
    
    cdef void _update_cached_indices(self):
        cdef list hand_data = self._hands[self._hand]
        self._cursor_idx = hand_data[0]
        self._pointer_idx = hand_data[1]
    
    @property
    def regs(self):
        return self._regs
    
    @property
    def hand(self):
        return self._hand
    
    @property
    def CURSOR(self):
        return self._cursor_idx
    
    @property
    def POINTER(self):
        return self._pointer_idx
    
    @POINTER.setter
    def POINTER(self, int value):
        self._hands[self._hand][1] = value
        self._pointer_idx = value
    
    @CURSOR.setter
    def CURSOR(self, int value):
        self._hands[self._hand][0] = value
        self._cursor_idx = value
    
    cpdef void set_hand(self, str name):
        if name not in self._hands:
            raise KeyError(name)
        self._hand = name
        self._update_cached_indices()
    
    cpdef void new_hand(self, str name):
        self._hands[name] = [0, 0]
    
    cdef inline bint _is_valid_index(self, int idx, int max_val):
        return 0 <= idx < max_val
    
    cdef void _check(self) except *:
        if not self._is_valid_index(self._cursor_idx, 1024):
            raise VMEXCEPTION(f"CURSOR {self._cursor_idx} out of range 0-1023")
        if not self._is_valid_index(self._pointer_idx, 512):
            raise VMEXCEPTION(f"POINTER {self._pointer_idx} out of range 0-511")
    
    cpdef check(self):
        self._check()
    
    cpdef list getreg(self, object reg=None):
        self._check()
        if reg is None:
            return self._regs[self._cursor_idx]
        return self._regs[reg]
    
    cpdef long getsum(self, object reg='curr'):
        cdef list reg_list
        cdef long total = 0
        cdef int i
        
        self._check()
        
        if reg == 'curr':
            reg_list = self._regs[self._cursor_idx]
        else:
            reg_list = self._regs[reg]
        
        cdef int length = len(reg_list)
        for i in range(length):
            total += reg_list[i]
        return total
    
    cpdef object getdata(self, object where=None):
        self._check()
        if where is None:
            return self._regs[self._cursor_idx][self._pointer_idx]
        return self._regs[self._cursor_idx][where]
    
    def _compile_section(self, string: str):
        cdef int pointer = self._pointer_idx
        return int(string
                  .replace('>', str(pointer + 1))
                  .replace('<', str(pointer - 1)))
    
    cpdef void setdata(self, object data):
        self._check()
        self._regs[self._cursor_idx][self._pointer_idx] = data
    
    cpdef void setdatato(self, int to, object data):
        self._check()
        self._regs[self._cursor_idx][to] = data
    
    cpdef void setdataraw(self, int reg, int to, object data):
        self._check()
        self._regs[reg][to] = data
    
    cpdef object getfrom_p(self, int index):
        self._check()
        return self.params.get(index, 0)
    
    cpdef void setto_p(self, int index, object data):
        self._check()
        self.params[index] = data
    
    cpdef void setpointer(self, int index):
        self._hands[self._hand][1] = index
        self._pointer_idx = index
    
    cpdef void setcursor(self, int index):
        self._hands[self._hand][0] = index
        self._cursor_idx = index
    
    cpdef void repeat(self, object object, int iters):
        cdef int iter = 0
        for iter in range(iters): object()
    
    cpdef void _create_reg(self, int index):
        self._regs[index] = [0] * self.__std_section_size

class Memory(_Memory): pass