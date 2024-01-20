import inspect

class Super:
    def __init__(self, owner=None, obj=None):
        self.init_call = True
        if obj is not None and owner is not None:
            self.obj = obj
            self.owner = owner
            self.mro_start = 0
            try:
                if isinstance(self.get_obj, self.owner):
                    self.mro_start = 1
            except KeyError:
                pass
        else:
            self.obj = self.get_obj
            self.owner = type(self.obj)
            self.mro_start = 1
        
    @property
    def get_obj(self):
        return inspect.currentframe().f_back.f_back.f_back.f_locals['self']

    def __getattribute__(self, name):
        if name == '__init__':
            if self.init_call:
                self.init_call = False
            if not self.init_call:
                raise AttributeError
        return object.__getattribute__(self, name)
    
    def __getattr__(self, name):
        attr = None
        mro = self.owner.mro()
        for x in range(self.mro_start, len(mro)):
            p_owner = mro[x]
            if hasattr(p_owner, name):
                attr = getattr(p_owner, name)
                break
        if attr is None:
            raise AttributeError('Attribute not found in the class hierarchy')
        if hasattr(type(attr), '__get__'):
            attr = attr.__get__(self.obj)
        return attr
    
    def __repr__(self):
        return f'{self.obj}, {self.owner}'


class A:
    def __init__(self) -> None:
        self.a = 5
        self.b = 6

    def repr(self):
        return f'{self.a}, {self.b}'

class B(A):
    def __init__(self):
        Super().__init__()


b = B()
print(b.repr())