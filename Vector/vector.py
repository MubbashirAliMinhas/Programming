import ctypes


class Vector:
    def __init__(self):
        self.length_left = 4
        self.length_right = 8
        self.length = self.length_left + self.length_right
        self.occupations_left = 0
        self.occupations_right = 0
        c_array = ctypes.py_object * self.length
        self.array = c_array()

    def __len__(self):
        return self.occupations_left + self.occupations_right

    def __iter__(self):
        for x in range(len(self)):
            yield self.array[self.length_left - self.occupations_left + x]

    def __reversed__(self):
        for x in range(len(self)-1, -1, -1):
            yield self.array[self.length_left - self.occupations_left + x]

    def __getitem__(self, index):
        if index >= len(self) or index < -len(self):
            raise IndexError('Index out of range.')
        elif index < 0:
            index = len(self) + index
        return self.array[self.length_left - self.occupations_left + index]

    def __setitem__(self, index, item):
        self.array[self.length_left - self.occupations_left + index] = item

    def appendleft(self, item):
        if self.occupations_left == self.length_left:
            length_left = self.length_left * 2
            self.length = length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[length_left - self.occupations_left + x] = _item
            self.array = array
            self.length_left = length_left
        self.occupations_left += 1
        self.array[self.length_left - self.occupations_left] = item

    def popleft(self):
        item = self[0]
        self.occupations_left -= 1
        if self.occupations_left == self.length_left // 2 and self.length_left >= 8:
            length_left = self.length_left // 2
            self.length = length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[length_left - self.occupations_left + x] = _item
            self.array = array
            self.length_left = length_left
        elif -self.occupations_left == self.length_right // 2 and self.length_right >= 16:
            self.length_right //= 2
            self.length = self.length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[self.length_left + x] = _item
            self.occupations_right += self.occupations_left
            self.occupations_left = 0
            self.array = array
        else:
            self.array[self.length_left - self.occupations_left - 1] = None
        return item

    def append(self, item):
        if self.occupations_right == self.length_right:
            self.length_right *= 2
            self.length = self.length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[self.length_left - self.occupations_left + x] = _item
            self.array = array
        self.array[self.length_left + self.occupations_right] = item
        self.occupations_right += 1

    def pop(self):
        item = self[self.occupations_right - 1]
        self.occupations_right -= 1
        if self.occupations_right == self.length_right // 2 and self.length_right >= 16:
            self.length_right //= 2
            self.length = self.length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[self.length_left - self.occupations_left + x] = _item
            self.array = array
        elif -self.occupations_right == self.length_left // 2 and self.length_left >= 8:
            length_left = self.length_left // 2
            self.length = length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, _item in enumerate(self):
                array[length_left - self.occupations_left + x] = _item
            self.occupations_left += self.occupations_right
            self.occupations_right = 0
            self.array = array
            self.length_left = length_left
        else:
            self.array[self.length_left + self.occupations_right] = None
        return item

    def extend(self, vector):
        if self.occupations_right + len(vector) > self.length_right:
            self.length_right *= 2
            self.length = self.length_left + self.length_right
            c_array = ctypes.py_object * self.length
            array = c_array()
            for x, item in enumerate(self):
                array[self.length_left - self.occupations_left + x] = item
            self.array = array
        for x, item in enumerate(vector):
            self[self.occupations_right + x] = item
        self.occupations_right += len(vector)

    def __repr__(self):
        if not len(self):
            return 'V[]'
        repr_vector = f'V[{self.array[self.length_left - self.occupations_left]}'
        for x in range(1, len(self)):
            repr_vector += f', {self.array[self.length_left - self.occupations_left + x]}'
        return f'{repr_vector}]'


vector1 = Vector()
vector2 = Vector()

vector1.append(1)
vector1.appendleft(2)
vector1.append(3)
vector1.appendleft(4)
vector1.append(5)
vector1.appendleft(6)
vector1.popleft()

print(vector1)