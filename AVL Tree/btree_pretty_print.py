class IndexNode:
    def __init__(self, item=None):
        self.value = item
        self.left = None
        self.right = None
        self.index = 0

    def __repr__(self):
        return repr(self.value)


def levels(node):
    stack = [node]
    traversed = []
    level_indexes = [0]
    while stack:
        stack2 = []
        level_indexes2 = []
        level = []
        for node, index in zip(stack, level_indexes):
            outer_node = IndexNode(str(node.value))
            outer_node.level_index = index
            level.append(outer_node)
            if node.left:
                stack2.append(node.left)
                level_indexes2.append(index * 2)
                outer_node.left = True
            if node.right:
                stack2.append(node.right)
                level_indexes2.append(index * 2 + 1)
                outer_node.right = True
        traversed.append(level)
        stack = stack2
        level_indexes = level_indexes2
    return traversed


def add_char(node, left, right, char):
    if not node.left:
        left_space = ' ' * left
        right_space = char * right
    elif not node.right:
        left_space = char * left
        right_space = ' ' * right
    else:
        left_space = char * left
        right_space = char * right
    return left_space + node.value + right_space


def reformat_node(node, final_max_length, index, char='_'):
    length = len(node.value)
    half_length = (final_max_length - length) // 2
    if final_max_length % 2 == 1 and length % 2 == 0:
        if index % 2 == 0:
            left = half_length + 1
            right = half_length
        else:
            left = half_length
            right = half_length + 1
    elif final_max_length % 2 == 0 and length % 2 == 1:
        if index % 2 == 0:
            left = half_length
            right = half_length + 1
        else:
            left = half_length + 1
            right = half_length
    else:
        left = half_length
        right = half_length
    return add_char(node, left, right, char)


def reformat_edge(node, max_length):
    if not node.left:
        return ' ' * (max_length + 1) + '\\'
    elif not node.right:
        return '/' + ' ' * (max_length + 1)
    else:
        return '/' + ' ' * max_length + '\\'


def pretty_print(root_node):
    if root_node is None:
        print('Empty')
        return
    elif root_node.left is None and root_node.right is None:
        print(root_node.value)
        return
    levels_traversed = levels(root_node)
    height = len(levels_traversed)
    max_lengths = []
    for level in reversed(levels_traversed):
        max_lengths.append(len(str(max((x.value for x in level), key=len))))

    if max_lengths[0] == 1:
        max_lengths[0] = 2

    deepest_length = max_lengths[0]
    final_max_lengths = [deepest_length]
    union_lengths = [final_max_lengths[0] // 2 - 1]
    disjoint_lengths = [final_max_lengths[0] - union_lengths[0]]
    parities = []
    acc = 0

    if deepest_length == 2 or deepest_length == 3:
        final_max_lengths.append(max_lengths[1])
        parities.append(max_lengths[1])
    else:
        if max_lengths[1] % 2 == 0:
            parity = 2
        else:
            parity = 1

        union_length = final_max_lengths[0] // 2 - 1
        final_max_length = union_length * 2 + parity
        if final_max_length < max_lengths[1]:
            parity = max_lengths[1] - union_length * 2
            final_max_length = max_lengths[1]

        final_max_lengths.append(final_max_length)
        parities.append(parity)

    initial_spaces = [0]
    for x in range(1, height - 1):
        union_length = final_max_lengths[x] // 2 - 1
        disjoint_length = final_max_lengths[x] - union_length
        union_lengths.append(union_length)
        disjoint_lengths.append(disjoint_length)

        acc += disjoint_lengths[x - 1]
        if max_lengths[x + 1] % 2 == 0:
            parity = 2
        else:
            parity = 1

        final_max_length = (acc + union_length) * 2 + parity
        if final_max_length < max_lengths[x + 1]:
            parity = max_lengths[x + 1] - (acc + union_length) * 2
            final_max_length = max_lengths[x + 1]

        final_max_lengths.append(final_max_length)
        parities.append(parity)
        initial_spaces.append(acc)
    initial_spaces.append(acc + disjoint_lengths[-1])

    space_between_lengths = []
    parity_pointer = len(parities) - 1
    for x in range(height - 1):
        space_between_level = []
        for y in range(2 ** (x + 1) - 1):
            if y % 2 == 0:
                space_between_level.append(initial_spaces[height - x - 2] * 2 + parities[parity_pointer])
            else:
                space_between_level.append(space_between_lengths[x - 1][y // 2] + (initial_spaces[height - x - 2] - initial_spaces[height - x - 1]) * 2)
        space_between_lengths.append(space_between_level)
        parity_pointer -= 1

    for level in space_between_lengths:
        level.append(0)

    reformatted_level = ' ' * initial_spaces[-1] + reformat_node(levels_traversed[0][0], final_max_lengths[-1], 0)
    edges = ''
    if levels_traversed[0][0].left:
        edges = (' ' * (initial_spaces[-1] - 1)) + '/' + (' ' * final_max_lengths[-1])
        if levels_traversed[0][0].right:
            edges += '\\'
    else:
        edges = (' ' * (initial_spaces[-1])) + (' ' * final_max_lengths[-1]) + '\\'
    reformatted_bst = [reformatted_level, edges]

    range_size = 2
    for x in range(1, height - 1):
        reformatted_level = ' ' * initial_spaces[height - x - 1]
        edges = ' ' * (initial_spaces[height - x - 1] - 1)
        z = 0
        for y in range(range_size):
            try:
                if y == levels_traversed[x][z].level_index:
                    if levels_traversed[x][z].left or levels_traversed[x][z].right:
                        reformatted_level += reformat_node(levels_traversed[x][z], final_max_lengths[height - x - 1], y)
                        edges += reformat_edge(levels_traversed[x][z], final_max_lengths[height - x - 1])
                    else:
                        reformatted_level += reformat_node(levels_traversed[x][z], final_max_lengths[height - x - 1], y, ' ')
                        edges += ' ' * (final_max_lengths[height - x - 1] + 2)
                    z += 1
                else:
                    reformatted_level += ' ' * final_max_lengths[height - x - 1]
                    edges += ' ' * (final_max_lengths[height - x - 1] + 2)
            except IndexError:
                break
            reformatted_level += ' ' * space_between_lengths[x - 1][y]
            edges += ' ' * (space_between_lengths[x - 1][y] - 2)
        range_size *= 2
        reformatted_bst.append(reformatted_level)
        reformatted_bst.append(edges)

    x = height - 1
    reformatted_level = ''
    z = 0
    for y in range(range_size):
        try:
            if levels_traversed[x][z].level_index == y:
                reformatted_level += reformat_node(levels_traversed[x][z], final_max_lengths[0], y, ' ')
                z += 1
            else:
                reformatted_level += ' ' * final_max_lengths[0]
        except IndexError:
            break
        reformatted_level += ' ' * space_between_lengths[x - 1][y]
    reformatted_bst.append(reformatted_level)

    for level in reformatted_bst:
        print(level)