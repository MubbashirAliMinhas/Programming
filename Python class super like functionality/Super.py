import inspect

class Specials:
    def __init__(self):
        self.specials = set(x for x in dir(self) if x.startswith('__') and x.endswith('__'))


class SpecialsStore:
    specials = Specials().specials


class Super:
    def __init__(self, owner=None, obj=None):
        if obj is not None and owner is not None:
            self.obj = obj
            self.owner = owner
            self.mro_start = 0
            if isinstance(self.get_obj, self.owner):
                self.mro_start = 1
        else:
            self.obj = self.get_obj
            self.owner = type(self.obj)
            self.mro_start = 1
        
    @property
    def get_obj(self):
        return inspect.currentframe().f_back.f_back.f_back.f_locals['self']

    def __getattribute__(self, name):
        if name in SpecialsStore.specials:
            raise AttributeError
        return object.__getattribute__(self, name)
    
    def __getattr__(self, name):
        attr = None
        mro = self.owner.mro()
        for x in range(self.mro_start, len(mro)):
            p_owner = mro[x]
            p_obj = p_owner()
            if hasattr(p_owner, name):
                attr = getattr(p_owner, name)
                break
            elif hasattr(p_obj, name):
                attr = getattr(p_obj, name)
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

class C(B):
    def __init__(self):
        self.a = Super().a
        self.b = Super().b

b = B()
print(b.repr())

c = C()
print(c.a)