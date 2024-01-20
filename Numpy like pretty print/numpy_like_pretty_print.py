def dimension(array):
    x = 0
    while True:
        if isinstance(array, int):
            break
        else:
            array = array[0]
            x += 1
    return x

def fp_check(flatten_array):
    for item in flatten_array:
        if isinstance(item, float):
            return True
    return False

def padding_length_int(flatten_array):
    max_value = max(flatten_array)
    min_value = min(flatten_array)
    max_value_length = len(str(max_value))
    min_value_length = len(str(min_value))
    return max(min_value_length, max_value_length)

def floats(flatten_array):
    fp_array = []
    for item in flatten_array:
        fp_item = item - int(item)
        fp_item = str(float(f'{fp_item:.8f}'))
        fp_item = fp_item[1:]
        if fp_item == '.0':
            fp_item = '.'
        fp_array.append(fp_item)
    return fp_array

def integers(flatten_array):
    int_array = []
    for item in flatten_array:
        int_item = str(int(item))
        int_array.append(int_item)
    return int_array

def padding_length_fp(int_array, fp_array):
    max_fp = max(fp_array, key=len)
    min_fp = min(fp_array, key=len)
    max_int = max(int_array, key=len)
    min_int = min(int_array, key=len)
    pad_right = len(max(min_fp, max_fp, key=len))
    pad_left = len(max(min_int, max_int, key=len))
    return pad_left, pad_right

def rebuild(array, dim):
    x = 1
    while dim - x != 1:
        rebuild_array = []
        for item in array:
            if item == '[' or item == ']':
                rebuild_array.append(item)
            else:
                rebuild_array.append('[')
                rebuild_array.extend(item)
                rebuild_array.append(']')
        array = rebuild_array
        x += 1
    return array

def flatten(rebuild_array):
    flattened = []
    for item in rebuild_array:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            continue
    return flattened

def restructure_1d_int(array, padding):
    str_array = ''
    for item in array:
        str_array += f'{item:>{padding+1}}'
    return f'[{str_array[1:]}]'

def restructure_1d_fp(array, pad_left, pad_right):
    int_array = integers(array)
    fp_array = floats(array)
    str_array = ''
    for int_item, fp_item in zip(int_array, fp_array):
        str_array += f'{int_item:>{pad_left+1}}{fp_item:<{pad_right}}'
    return f'[{str_array[1:]}]'

def restructure_1d_fp_special(int_array, fp_array, pad_left, pad_right):
    str_array = ''
    for int_item, fp_item in zip(int_array, fp_array):
        str_array += f'{int_item:>{pad_left+1}}{fp_item:<{pad_right}}'
    return f'[{str_array[1:]}]'

def restructure_multi_int(array, padding, dim):
    str_array = ''
    for item in array:
        if isinstance(item, list):
            str_array += restructure_1d_int(item, padding)
        else:
            str_array += item
    str_array = f'[{str_array}]'
    finalized = finalize(str_array, dim)
    return finalized

def restructure_multi_fp(array, pad_left, pad_right, dim):
    str_array = ''
    for item in array:
        if isinstance(item, list):
            str_array += restructure_1d_fp(item, pad_left, pad_right)
        else:
            str_array += item
    str_array = f'[{str_array}]'
    finalized = finalize(str_array, dim)
    return finalized

def restructure_1d_general(array):
    if fp_check(array):
        int_array = integers(array)
        fp_array = floats(array)
        pad_left, pad_right = padding_length_fp(int_array, fp_array)
        return restructure_1d_fp_special(int_array, fp_array, pad_left, pad_right)
    else:
        padding = padding_length_int(array)
        return restructure_1d_int(array, padding)

def restructure_multi_general(array, dim):
    rebuild_array = rebuild(array, dim)
    flatten_array = flatten(rebuild_array)
    if fp_check(flatten_array):
        int_array = integers(flatten_array)
        fp_array = floats(flatten_array)
        pad_left, pad_right = padding_length_fp(int_array, fp_array)
        return restructure_multi_fp(rebuild_array, pad_left, pad_right, dim)
    else:
        padding = padding_length_int(flatten_array)
        return restructure_multi_int(rebuild_array, padding, dim)

def restructure(array):
    dim = dimension(array)
    if dim == 1:
        return restructure_1d_general(array)
    else:
        return restructure_multi_general(array, dim)
        

def finalize(restructure, dim):
    for x in range(dim, 0, -1):
        enter = '\n' * x
        tab = ' ' * (dim - x)
        enter_full = enter + tab
        bracket_part_A = ']' * x
        bracket_part_B = '[' * x
        bracket = bracket_part_A + bracket_part_B
        replace_bracket = bracket_part_A + enter_full + bracket_part_B
        restructure = restructure.replace(bracket, replace_bracket)
    return restructure

def white_space(dim, component_dim):
    return ('\n' * component_dim) + (' ' * (dim - component_dim))

array = [[[[1, 2, 3], [4, 5, 6]], 
          [[7, 8, 9], [-10, 11, 12]]],
         [[[1, 2, 3], [4, 5.246, 6]], 
          [[7, 8, 9.200000001], [10, 11, 12]]]]


import numpy as np

print('INPUT LIST/ARRAY')
print(array)

print('\nNUMPY')
print(np.array(array))

print('\nMY REFORMAT ALGORITHM')
print(restructure(array))
