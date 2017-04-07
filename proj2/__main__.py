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
        super().__init__(
            title='CS 4732 Project 2 by Daniel Beckwith',
            frame_rate=60.0,
            run_time=30.0)

        self.setup_scene(
            background_color=util.hsl(0, 0, 0),
            camera_position=QVector3D(1.0, 4.0, -10.0),
            camera_lookat=QVector3D(0.0, 0.0, 0.0))

    def make_scene(self):
        """
        Overriddes Animation.make_scene
        """
        # origin sphere
        center = self.add_sphere()
        center.setScale(0.03)

        # ground plane
        ground = self.add_plane()
        ground.setScale(10.0)

        self.path_radius = 1.5 # radius of the circle that the rig follows

        self.spine_len = 10 # number of spinal joints
        self.spine_joint_len = 0.2 # length of each spinal joint
        self.spine_bend_angle = 2 * math.asin(self.spine_joint_len / (2 * self.path_radius)) # angle to bend around circular path

        self.wing_len = 5 # number of wing joints
        self.wing_joint_len = 0.15 # length of each wing joint

        # initialize rig with root joint (which is part of the spine)
        self.rig = Rig(Joint(self,
            length=self.spine_joint_len,
            thickness=0.06,
            color=util.hsl(0, 100, 80))) # red color

        self.rig.joints.spine[0] = self.rig.joints.root # include root in list of spine joints
        # create rest of spine
        for i in range(1, self.spine_len):
            self.rig.joints.spine[i] = Joint(self,
                length=self.spine_joint_len,
                thickness=0.04,
                parent=self.rig.joints.spine[i - 1], # parent is previous spine joint
                color=util.hsl(util.lerp(i, 1, self.spine_len - 1, 120, 180), 100, 80)) # fade from green to cyan

        self.rig.joints.wing_root = self.rig.joints.spine[self.spine_len // 2] # pick root for wings as halfway along spine
        # create both wings
        for w in range(2):
            for i in range(self.wing_len):
                self.rig.joints.wings[w][i] = Joint(self,
                    length=self.wing_joint_len,
                    thickness=0.02,
                    parent=self.rig.joints.wing_root if i == 0 else self.rig.joints.wings[w][i - 1], # first joint's parent is the wing root, rest is previous wing joint
                    color=util.hsl(util.lerp(i, 0, self.wing_len - 1, 240, 300), 100, 80)) # fade from blue to magenta

        # add some lights
        self.add_light(QVector3D(-20.0, 20.0, -20.0), 1.0) # upper right key light
        self.add_light(QVector3D(20.0, 10.0, -20.0), 0.5) # upper left fill light

    def update(self, frame, t, dt):
        """
        Overriddes Animation.update
        """
        spine_wave_phase = util.lerp(t, 0, 1, 0, 2 * math.pi)
        spine_wave_magnitude = 0.5
        wing_wave_phase = util.lerp(t + 0.5, 0, 1, 0, -2 * math.pi)
        wing_wave_magnitude = 0.4

        self.rig.reset() # reset all transforms

        # set position and orientation of the root joint, which positions the entire rig
        self.rig.joints.root.local_transform.translate(0, 0.7 + math.cos(util.lerp(t, 0, 10, 0, 2 * math.pi)) * spine_wave_magnitude * self.spine_joint_len, 0) # undulate up and down
        self.rig.joints.root.local_transform.rotate(util.rad2deg(util.lerp(t, 0, 8.5, 0, 2 * math.pi)), 0, -1, 0) # rotate around circular path
        self.rig.joints.root.local_transform.translate(self.path_radius, 0, 0) # move outward by the path's radius
        self.rig.joints.root.local_transform.translate(0, 0, -self.spine_joint_len / 2) # small adjustment to center root joint on the circular path since the joint's origin is its base, not its center

        # transform spinal joints
        prev_global_angle = 0
        for i, joint in enumerate(self.rig.joints.spine):
            if i != 0:
                # rotate each joint by the bend amount for bending along circular path
                # except root, which should stay pointing forward
                joint.local_transform.rotate(
                    util.rad2deg(self.spine_bend_angle),
                    0, -1, 0)

            # rotate joints to form a sine wave
            theta = util.lerp(i + spine_wave_phase, 0, self.spine_len, 0, 2 * math.pi)
            # global angle is the absolute angle from the x-axis of the sine graph at this point
            # the angle is just the inverse tangent of the derivative of the sine curve
            global_angle = math.atan(spine_wave_magnitude * math.cos(theta))
            # angle needed for this joint to rotate has to relative to previous joint
            local_angle = global_angle - prev_global_angle
            prev_global_angle = global_angle
            joint.local_transform.rotate(
                util.rad2deg(local_angle),
                1, 0, 0)

        # transform wing joints
        for d, wing in zip((-1, 1), self.rig.joints.wings):
            prev_global_angle = 0
            for i, joint in enumerate(wing):
                if i == 0:
                    # rotate first wing joint outwards away from body in the wing's direction
                    joint.local_transform.rotate(90, 0, d, 0)
                # rotate each wing joint a little bit backwards for a nice bend
                joint.local_transform.rotate(5, 0, d, 0)

                # same sine wave idea as for the spine
                theta = util.lerp(i + wing_wave_phase, 0, self.wing_len * 2, 0, 2 * math.pi)
                global_angle = math.atan(wing_wave_magnitude * math.cos(theta))
                local_angle = global_angle - prev_global_angle
                prev_global_angle = global_angle
                joint.local_transform.rotate(
                    util.rad2deg(local_angle),
                    1, 0, 0)

        # update all the absolute transforms from the local transforms set above
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
