# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: nonecheck=False
# cython: cdivision=True

import pickle
import os
from functools import lru_cache
class VMEXCEPTION(Exception): pass
    
cdef class FastRepeater:
    cdef:
        object _obj
        Py_ssize_t _iters
    
    def __cinit__(self, object obj, Py_ssize_t iters):
        self._obj = obj
        self._iters = iters
    
    cpdef void run(self):
        cdef:
            Py_ssize_t i
            object obj = self._obj
            Py_ssize_t iters = self._iters
        
        for i in range(iters):
            obj()
    
    def __call__(self):
        self.run()







cdef class _Memory:
    cdef int __std_params, __std_section_size, __std_registers
    cdef list[int, int] _regs
    cdef dict _hands, params
    cdef str _hand
    cdef int _cursor_idx, _pointer_idx
    
    def __init__(self):
        self.__std_params = 1024
        self.__std_section_size = 4096
        self.__std_registers = 2048
        self.CHECK = True
        
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
        ln1 = len(self._regs)
        if not self._is_valid_index(self._cursor_idx, ln1):
            raise VMEXCEPTION(f"CURSOR {self._cursor_idx} out of range 0-{ln1}")
        if not self._is_valid_index(self._pointer_idx, self.__std_registers):
            raise VMEXCEPTION(f"POINTER {self._pointer_idx} out of range 0-{self.__std_registers}")
    
    cpdef check(self):
        if self.CHECK: self._check()
    
    cpdef list getreg(self, object reg=None):
        self._check()
        if reg is None:
            return self._regs[self._cursor_idx]
        return self._regs[reg]
    
    cpdef int getsum(self, object reg='curr'):
        cdef list reg_list
        self._check()
        if reg == 'curr':
            reg_list = self._regs[self._cursor_idx]
        else:
            reg_list = self._regs[reg]
        try:
            return int(sum(reg_list))
        except:
            return -1
    
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
        FastRepeater(obj=object, iters=iters)()
    
    cpdef void _create_reg(self, int index):
        if index < len(self.regs): self._regs[index] = [0] * self.__std_section_size
        else: self._regs.append([0] * self.__std_section_size)

class Memory(_Memory): pass


cdef class _Memory2:
    cdef dict memory
    
    def __init__(self) -> None:
        self.memory = {}
    
    cpdef void setto(self, object key, object data):
        self.memory[key] = data
    
    cpdef object getfrom(self, object key):
        return self.memory[key]
    
    cdef inline object _getfrom_fast(self, object key):
        return self.memory[key]
    
    cpdef object getfrom_str(self, str key):
        return self.memory.get(key)
    
    cpdef object getfrom_int(self, int key):
        return self.memory.get(key)
    
    cpdef void setto_int(self, int key, object data):
        self.memory[key] = data
    
    cpdef void setto_str(self, str key, object data):
        self.memory[key] = data
    
    cpdef void update_batch(self, dict batch_data):
        self.memory.update(batch_data)
    
    cpdef void clear(self):
        self.memory.clear()
    
    cpdef has_key(self, object key):
        return key in self.memory

    cpdef int size(self):
        return len(self.memory)
    
    cpdef list keys(self):
        return list(self.memory.keys())

    cpdef void save(self, str name):
        with open(name, 'wb') as f:
            pickle.dump(self.memory, f)
    
    cpdef void load(self, str name):
        with open(name, 'rb') as f:
            content = pickle.load(f)
        self.memory = dict(content)

    cpdef str path(self):
        return os.getcwd()
    
class Memory2(_Memory2): pass