# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QVector3D
from PyQt5.QtWidgets import QApplication

from .animation import Animation
from . import util


class Proj2Ani(Animation):
    """
    Implements the kinematics animation.
    """

    def __init__(self):
        super().__init__('CS 4732 Project 2 by Daniel Beckwith', 60.0, 10.0)

        self.setup_scene(
            background_color=util.hsl(0, 0, 0),
            camera_position=QVector3D(3.0, 5.0, -10.0),
            camera_lookat=QVector3D(0.0, 0.0, 0.0))

    def make_scene(self):
        """
        Overriddes Animation.make_scene
        """
        self.add_rgb_cube(1.0, 1.0, 1.0)

        # add some lights
        self.add_light(QVector3D(-20.0, 20.0, -20.0), 1.0) # upper right key light
        self.add_light(QVector3D(20.0, 10.0, -20.0), 0.5) # upper left fill light

    def update(self, frame, t, dt):
        """
        Overriddes Animation.update
        """
        pass

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
