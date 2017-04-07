# -*- coding: utf-8 -*-

import sys
import math
import itertools

from PyQt5.QtGui import QVector3D
from PyQt5.QtWidgets import QApplication

from .animation import Animation
from .rig import Rig, Joint
from . import util


class Proj2Ani(Animation):
    """
    Implements the kinematics animation.
    """

    def __init__(self):
        super().__init__('CS 4732 Project 2 by Daniel Beckwith', 60.0, 10.0)

        self.setup_scene(
            background_color=util.hsl(0, 0, 0),
            camera_position=QVector3D(1.0, 4.0, -10.0),
            camera_lookat=QVector3D(0.0, 0.0, 0.0))

    def make_scene(self):
        """
        Overriddes Animation.make_scene
        """
        center = self.add_sphere()
        center.setScale(0.03)

        ground = self.add_plane()
        ground.setScale(10.0)

        self.rig = Rig(Joint(self, 0.06, 0.06, 0.2))
        for i in range(10):
            self.rig.joints.spine[i] = Joint(self, 0.04, 0.04, 0.2, self.rig.joints.root if i == 0 else self.rig.joints.spine[i - 1])

        # add some lights
        self.add_light(QVector3D(-20.0, 20.0, -20.0), 1.0) # upper right key light
        self.add_light(QVector3D(20.0, 10.0, -20.0), 0.5) # upper left fill light

    def update(self, frame, t, dt):
        """
        Overriddes Animation.update
        """
        self.rig.reset()
        self.rig.joints.root.local_transform.rotate(-90, 1, 0, 0)
        spine = [self.rig.joints.root] + list(self.rig.joints.spine)
        prev_global_angle = 0
        for i, s in enumerate(spine):
            phase = util.lerp(t, 0, 1, 0, 2 * math.pi)
            magnitude = util.lerp(math.sin(util.lerp(t, 0, 10, 0, 2 * math.pi)), -1, 1, 0.5, 1.5)
            theta = util.lerp(i + phase, 0, len(spine), 0, 2 * math.pi)
            global_angle = math.atan(magnitude * math.cos(theta))
            local_angle = global_angle - prev_global_angle
            prev_global_angle = global_angle
            s.local_transform.rotate(
                util.rad2deg(local_angle),
                0, 1, 0)
        self.rig.update()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='proj2',
        description='Animates a kinematic skeleton.',
        epilog='Created by Daniel Beckwith for WPI CS 4732.')
    args = parser.parse_args()

    app = QApplication([])

    ani = Proj2Ani()
    ani.run()

    sys.exit(app.exec_())
