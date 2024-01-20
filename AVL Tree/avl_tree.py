from collections import deque
from btree_pretty_print import pretty_print as pprint


class AVLTree:
    def __init__(self, iterable=None):
        self.root_node = None
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item):
        if self.root_node is None:
            self.root_node = self.__Node(item)
        else:
            new_node = self.__Node(item)
            next_node = self.root_node
            node = None
            nodes = []
            while next_node:
                nodes.append(next_node)
                node = next_node
                if item < node.value:
                    next_node = next_node.left
                else:
                    next_node = next_node.right
            if item < node.value:
                node.left = new_node
            else:
                node.right = new_node

            unbalanced = False
            index = len(nodes)
            for node in reversed(nodes):
                index -= 1
                left = 0
                right = 0
                node.height += 1
                if node.right:
                    right = node.right.height + 1
                if node.left:
                    left = node.left.height + 1
                if right - left == 0:
                    node.height -= 1
                    break
                elif abs(right - left) == 2:
                    unbalanced = True
                    break
            nodes.append(new_node)

            if unbalanced:
                r_node = None
                node1 = nodes[index]
                node2 = nodes[index + 1]
                node3 = nodes[index + 2]
                height = node1.height
                if height - left == 0:
                    if node2.right == node3:
                        r_node = self.rotate_left_right(node1, node2, node3)
                    else:
                        r_node = self.rotate_right(node1, node2, node3)
                else:
                    if node2.left == node3:
                        r_node = self.rotate_right_left(node1, node2, node3)
                    else:
                        r_node = self.rotate_left(node1, node2, node3)

                if r_node:
                    parent_node = nodes[index - 1]
                    if parent_node.right == node1:
                        parent_node.right = r_node
                    else:
                        parent_node.left = r_node

    def rotate_right(self, node1, node2, node3):
        node1.left = node2.right
        node2.right = node1
        node2.left = node3
        node1.height -= 2
        if node1 == self.root_node:
            self.root_node = node2
        else:
            return node2

    def rotate_left(self, node1, node2, node3):
        node1.right = node2.left
        node2.left = node1
        node2.right = node3
        node1.height -= 2
        if node1 == self.root_node:
            self.root_node = node2
        else:
            return node2

    def rotate_right_remove(self, node1, node2, node3):
        node1.left = node2.right
        node2.right = node1
        node2.left = node3
        if node1.left:
            node1.height = node1.left.height + 1
            node2.height = node2.right.height + 1
        else:
            node1.height -= 2
        if node1 == self.root_node:
            self.root_node = node2
        else:
            return node2

    def rotate_left_remove(self, node1, node2, node3):
        node1.right = node2.left
        node2.left = node1
        node2.right = node3
        if node1.right:
            node1.height = node1.right.height + 1
            node2.height = node2.left.height + 1
        else:
            node1.height -= 2
        if node1 == self.root_node:
            self.root_node = node2
        else:
            return node2

    def rotate_left_right(self, node1, node2, node3):
        node1.left = node3.right
        node2.right = node3.left
        node3.right = node1
        node3.left = node2
        node1.height -= 2
        node2.height -= 1
        node3.height += 1
        if node1 == self.root_node:
            self.root_node = node3
        else:
            return node3

    def rotate_right_left(self, node1, node2, node3):
        node1.right = node3.left
        node2.left = node3.right
        node3.left = node1
        node3.right = node2
        node1.height -= 2
        node2.height -= 1
        node3.height += 1
        if node1 == self.root_node:
            self.root_node = node3
        else:
            return node3

    def remove(self, item):
        node = self.root_node
        rotating_nodes = None
        if node.left is None and node.right is None:
            self.root_node = None
            return

        nodes = []
        unbalanced = False
        while node:
            nodes.append(node)
            if node.value > item:
                node = node.left
            elif node.value < item:
                node = node.right
            elif node.value == item:
                break

        if node.right and node.left:
            stack = [node]
            node = node.left
            while stack or node:
                if node:
                    stack.append(node)
                    node = node.right
                else:
                    node = stack.pop()
                    break

            stack[0].value = node.value
            if node.right is None and node.left is None:
                if stack[-1].value != node.value:
                    stack[-1].right = None
                    if stack[-1].height >= 2:
                        node1 = stack[-1]
                        node2 = node1.left
                        if node2.left:
                            r_node = self.rotate_right(node1, node2, node2.left)
                        else:
                            r_node = self.rotate_left_right(node1, node2, node2.right)
                        stack[-2].left = r_node
                else:
                    r_node = None
                    stack[0].left = None
                    node1 = stack[0]
                    node2 = node1.right
                    if node2.right:
                        r_node = self.rotate_left_remove(node1, node2, node2.right)
                    elif node2.left:
                        r_node = self.rotate_right_left(node1, node2, node2.left)
                    if r_node:
                        if nodes[-2].right == stack[0]:
                            nodes[-2].right = r_node
                        else:
                            nodes[-2].left = r_node
            else:
                node.value = node.left.value
                node.left = None
                node.height = 0
                r_node = None
                for n in reversed(stack):
                    left = n.left.height
                    right = n.right.height
                    n.height = max(left, right) + 1
                if nodes[-1].right.height > 1:
                    r_node = self.rotate_left_remove(nodes[-1], nodes[-1].right, nodes[-1].right.right)
                if r_node:
                    if nodes[-2].right == stack[0]:
                        nodes[-2].right = r_node
                    else:
                        nodes[-2].left = r_node

        elif node.left:
            node.value = node.left.value
            node.left = None
            node.height = 0
            index = 1
            if len(nodes) > 1:
                for x in range(1, len(nodes) + 1):
                    left = -1
                    right = -1
                    index += 1
                    if nodes[-x].left:
                        left = nodes[-x].left.height
                    if nodes[-x].right:
                        right = nodes[-x].right.height
                    nodes[-x].height = max(left, right) + 1
                    if right - left >= 2:
                        unbalanced = True
                        rotating_nodes = [nodes[-x]]
                        rotating_nodes.append(rotating_nodes[0].left)
                        break
        elif node.right:
            node.value = node.right.value
            node.right = None
            node.height = 0
            index = 1
            if len(nodes) > 1:
                for x in range(1, len(nodes) + 1):
                    left = -1
                    right = -1
                    index += 1
                    if nodes[-x].left:
                        left = nodes[-x].left.height
                    if nodes[-x].right:
                        right = nodes[-x].right.height
                    nodes[-x].height = max(left, right) + 1
                    if right - left <= -2:
                        unbalanced = True
                        rotating_nodes = [nodes[-x]]
                        rotating_nodes.append(rotating_nodes[0].left)
                        break
        else:
            nodes.pop()
            if nodes[-1].right == node:
                nodes[-1].right = None
            else:
                nodes[-1].left = None
            index = 1
            if len(nodes) > 1:
                for x in range(1, len(nodes) + 1):
                    left = -1
                    right = -1
                    index += 1
                    if nodes[-x].left:
                        left = nodes[-x].left.height
                    if nodes[-x].right:
                        right = nodes[-x].right.height
                    nodes[-x].height = max(left, right) + 1
                    if right - left >= 2:
                        unbalanced = True
                        rotating_nodes = [nodes[-x]]
                        rotating_nodes.append(rotating_nodes[0].right)
                        break
                    elif right - left <= -2:
                        unbalanced = True
                        rotating_nodes = [nodes[-x]]
                        rotating_nodes.append(rotating_nodes[0].left)
                        break

        if unbalanced:
            node1 = rotating_nodes[0]
            node2 = rotating_nodes[1]
            r_node = None
            left = -1
            right = -1
            if node2.left:
                left = node2.left.height
            if node2.right:
                right = node2.right.height
            if node1.right == node2:
                if right >= left:
                    r_node = self.rotate_left_remove(node1, node2, node2.right)
                else:
                    r_node = self.rotate_right_left(node1, node2, node2.left)
            elif node1.left == node2:
                if left >= right:
                    r_node = self.rotate_right_remove(node1, node2, node2.left)
                else:
                    r_node = self.rotate_left_right(node1, node2, node2.right)

            if r_node:
                parent_node = nodes[-index]
                if parent_node.right == node1:
                    parent_node.right = r_node
                else:
                    parent_node.left = r_node

    def __contains__(self, item):
        node = self.root_node
        is_present = False
        while node:
            if node.value > item:
                node = node.left
            elif node.value < item:
                node = node.right
            elif node.value == item:
                is_present = True
                break
        return is_present

    def preorder(self):
        node = self.root_node
        stack = deque()
        stack.append(node)
        traversed = deque()
        while stack:
            node = stack.pop()
            traversed.append(node.value)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return traversed

    def inorder(self):
        node = self.root_node
        stack = deque()
        traversed = deque()
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                traversed.append(node.value)
                node = node.right
        return traversed

    def postorder(self):
        node = self.root_node
        stack = deque()
        stack.append(node)
        traversed = deque()
        while stack:
            node = stack.pop()
            traversed.appendleft(node.value)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return traversed

    def level_order(self):
        node = self.root_node
        deq = deque()
        deq.append(node)
        traversed = deque()
        while deq:
            node = deq.pop()
            traversed.append(node.value)
            if node.left:
                deq.appendleft(node.left)
            if node.right:
                deq.appendleft(node.right)
        return traversed

    def levels(self):
        node = self.root_node
        deq = [node]
        traversed = []
        while deq:
            deq2 = []
            level = []
            for node in deq:
                level.append(node.value)
                if node.left:
                    deq2.append(node.left)
                if node.right:
                    deq2.append(node.right)
            traversed.append(level)
            deq = deq2
        return traversed

    @staticmethod
    def height(node):
        if node is None:
            return 0
        nodes1 = [node]
        h = 0
        while nodes1:
            nodes2 = []
            for node in nodes1:
                if node.left:
                    nodes2.append(node.left)
                if node.right:
                    nodes2.append(node.right)
            nodes1 = nodes2
            h += 1
        return h

    class __Node:
        def __init__(self, item=None):
            self.value = item
            self.left = None
            self.right = None
            self.height = 0

        def __repr__(self):
            return f'{self.value}'


sequence = list(range(1, 32))
print('Input Sequence:', sequence)
avl = AVLTree(sequence)
print('\nAVL Tree:')
pprint(avl.root_node)
