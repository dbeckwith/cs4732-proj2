# -*- coding: utf-8 -*-

from collections import defaultdict

from PyQt5.QtGui import QMatrix4x4


class Rig(object):
    class Joints(object):
        def __init__(self):
            self._joints = defaultdict(Rig.Joints)

        def __getitem__(self, index):
            return self._joints[index]

        def __setitem__(self, index, value):
            self._joints[index] = value

        def add(self, joint):
            self._joints[len(self._joints)] = joint

        def __len__(self):
            return len(self._joints)

        def __iter__(self):
            return iter(self._joints.values())

        def __contains__(self, value):
            return value in self._joints

        def __getattr__(self, attr):
            return self._joints[attr]

        def __setattr__(self, attr, value):
            if not attr.startswith('_'):
                self._joints[attr] = value
            else:
                super().__setattr__(attr, value)

    def __init__(self, root):
        self.joints = Rig.Joints()
        self.joints.root = root

    def reset(self):
        for joint in self.joints.root.iter_hierarchy():
            joint.reset()

    def update(self):
        self.joints.root.update_transform()

class Joint(object):
    def __init__(self, ani, width, height, depth, parent=None):
        self.parent = parent
        if self.parent is not None:
            self.parent.children.add(self)
        self.children = set()
        self._width, self._height, self._depth = width, height, depth
        self._obj_transform = ani.add_rgb_cube()
        self._shape_transform = QMatrix4x4()
        self._shape_transform.scale(width, height, depth)
        self._shape_transform.translate(0, 0, 0.5)
        self.joint_pos = QMatrix4x4()
        self.joint_pos.translate(0, 0, depth)
        self.local_transform = QMatrix4x4()
        self._global_transform = QMatrix4x4()

    def reset(self):
        self.local_transform = QMatrix4x4()

    def update_transform(self):
        if self.parent is None:
            self._global_transform =  self.local_transform
        else:
            self._global_transform = self.parent._global_transform * self.parent.joint_pos * self.local_transform
        self._obj_transform.setMatrix(self._global_transform * self._shape_transform)
        for child in self.children:
            child.update_transform()

    def print_hierarchy(self, level=0):
        print('  ' * level + str(self.local_transform))
        for child in self.children:
            child.print_hierarchy(level + 1)

    def iter_hierarchy(self):
        yield self
        for child in self.children:
            yield from child.iter_hierarchy()
