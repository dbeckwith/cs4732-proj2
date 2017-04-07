# -*- coding: utf-8 -*-

from collections import defaultdict

from PyQt5.QtGui import QMatrix4x4

from . import util


class Rig(object):
    """
    Class representing a kinematic rig containing joints.
    """

    class Joints(object):
        """
        Utility class that acts as a namespace allowing arbitrary attributes to be set on it.
        When an attribute is referenced that doesn't exist,
        it gets by default initialized to another instance of this class.
        This allows easily defining nested attributes like so:
            j = Joints()
            j.a.b.c = 'joint'
        The attribute 'a' of j gets initialized to a new Joint() instance when it is referenced, and so on.
        """

        def __init__(self):
            # all attributes stored in defaultdict, which initializes missing keys to another instance of this class
            self._joints = defaultdict(Rig.Joints)

        def __getitem__(self, index):
            return self._joints[index]

        def __setitem__(self, index, value):
            self._joints[index] = value

        def __delitem__(self, index):
            del self._joints[index]

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

        def __delattr__(self, attr):
            if not attr.startswith('_'):
                del self._joints[attr]
            else:
                super().__delattr__(attr)

    def __init__(self, root):
        """
        Initializes the joints object with the required root joint.
        """
        self.joints = Rig.Joints()
        self.joints.root = root

    def reset(self):
        """
        Resets the local transforms of the entire joint hieararchy.
        """
        for joint in self.joints.root.iter_hierarchy():
            joint.reset()

    def update(self):
        """
        Updates the global transforms of the entire joint hieararchy.
        """
        self.joints.root.update_transform()

class Joint(object):
    """
    Class representing a single kinematic joint.
    """

    def __init__(self, ani, length, thickness, parent=None, color=util.hsl(0, 0, 50)):
        """
        Creates a new joint.

        Arguments:
            ani: Animation, the animation to add objects to
            length: float, the length of the joint
            thickness: float, the thickness of the joint
            parent: Joint or None, the parent joint of this joint
            color: QColor, the color of the joint's material
        """
        self.parent = parent
        if self.parent is not None:
            # maintain parent's children list
            self.parent.children.add(self)
        self.children = set()
        self.length = length
        self.thickness = thickness
        self._obj_transform = ani.add_cone(color=color) # add cone, keep reference to its transform

        # transform for forming the shape of the joint
        self._shape_transform = QMatrix4x4()
        self._shape_transform.scale(thickness, thickness, length) # scale to joint's thickness and length
        self._shape_transform.translate(0, 0, 0.5) # move forward so joint's origin is at its base
        self._shape_transform.rotate(90, 1, 0, 0) # make sure cone points forward

        # transform for making sure child joints start at the endpoint of this joint
        self.joint_pos = QMatrix4x4()
        self.joint_pos.translate(0, 0, length)

        # local transform of this joint relative to its parent
        self.local_transform = QMatrix4x4()

        # global transform of this joint relative to the world
        self._global_transform = QMatrix4x4()

    def reset(self):
        """
        Resets the local transform of this joint.
        """
        self.local_transform = QMatrix4x4()

    def update_transform(self):
        """
        Updates this joint's global transform by using its local transform and its parent's global transform.
        """
        if self.parent is None:
            # base case, just use local transform
            self._global_transform = self.local_transform
        else:
            # has a parent
            # first do local transform, then move to parent's joint position, then move by parent's global transform
            self._global_transform = self.parent._global_transform * self.parent.joint_pos * self.local_transform

        # transform actual object
        # do shape transform first to get model shape, then do global transform
        self._obj_transform.setMatrix(self._global_transform * self._shape_transform)

        # update children recursively
        for child in self.children:
            child.update_transform()

    def iter_hierarchy(self):
        """
        Iterates the entire joint hierarchy under this joint.

        Returns:
            an iterator of Joints, this joint's hierarchy in pre-order
        """
        # this joint first
        yield self
        # then for each child
        for child in self.children:
            # yield that child's entire hierarchy
            yield from child.iter_hierarchy()
