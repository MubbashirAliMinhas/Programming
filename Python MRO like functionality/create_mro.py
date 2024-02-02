class MRO:
    def __init__(self, name):
        if isinstance(name, list):
            self.MRO = name
        else:
            self.MRO = [name]
    
    def __getitem__(self, index):
        return self.MRO[index]

    def __len__(self):
        return len(self.MRO)
    
    def __iter__(self):
        for Type in self.MRO:
            yield Type

    def __contains__(self, name):
        if name in self.MRO:
            return True
        return False

    def merge(self, *others):
        self_i = 1
        offsets = [0 for x in range(len(others))]
        states = [None for x in range(len(others))]
        if len(others) > 1:
            iter_mros = others
            others = [{key: value for key, value in zip(other.MRO, range(len(other.MRO)))} for other in others]
            first_mro = iter_mros[0]
            first_i = 1
            key = first_mro[offsets[0]]
            while True:
                try:
                    for x in range(first_i, len(iter_mros)):
                        if key in others[x]:
                            if others[x][key] - offsets[x] == 0:
                                states[x] = True
                            else:
                                states[x] = False
                        else:
                            states[x] = None
                    
                    states[first_i - 1] = False
                    for x in range(first_i, len(iter_mros)):
                        if states[x] == False:
                            states[first_i - 1] = None
                            break
                    if states[first_i - 1] is not None:
                        for x in range(first_i, len(iter_mros)):
                            if states[x] == True:
                                states[first_i - 1] = True
                                break
                    
                    if states[first_i - 1] is None:
                        for x in range(1, len(iter_mros)):
                            if states[x] == False:
                                new_offset = others[x][key]
                                for _ in range(new_offset):
                                    self.MRO.append(iter_mros[x][offsets[x]])
                                    offsets[x] += 1
                    elif states[first_i - 1] == True:
                        for x in range(len(iter_mros)):
                            if states[x] == True:
                                offsets[x] += 1
                        self.MRO.append(key)
                        while offsets[first_i - 1] == len(first_mro):
                            first_mro = iter_mros[first_i]
                            first_i += 1
                        key = first_mro[offsets[first_i - 1]]  
                    else:
                        self.MRO.append(key)
                        if offsets[first_i - 1] < len(first_mro) - 1:
                            offsets[first_i - 1] += 1
                        else:
                            # states[first_i - 1] = 0
                            first_mro = iter_mros[first_i]
                            first_i += 1
                        key = first_mro[offsets[first_i - 1]]
                except IndexError:
                    break
        elif len(others) == 1:
            iter_mro = others[0].MRO
            self_i = 1
            for key in iter_mro:
                self.MRO.append(key)
                self_i += 1

    def __repr__(self) -> str:
        self.next_mro = iter(self.MRO)
        string = f'MRO({next(self.next_mro)}'
        for key in self.next_mro:
            string += f', {key}'
        string += ')'
        return string


mro1 = MRO(['D', 'E', 'G', 'H', 'F'])
mro2 = MRO(['B', 'C', 'E', 'G', 'H'])
mro3 = MRO(['E', 'G'])

mro1.merge(mro2, mro3)

print(mro1)