# -*- coding: utf-8 -*-

import os.path

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QVector3D, QQuaternion
from PyQt5.Qt3DCore import QEntity, QTransform
from PyQt5.Qt3DRender import QPointLight
from PyQt5.Qt3DExtras import Qt3DWindow, QCuboidMesh, QSphereMesh, QConeMesh, QPlaneMesh, QCylinderMesh, QPhongMaterial
from PyQt5.QtQml import QQmlComponent, QQmlEngine

from . import util


class Animation(object):
    """
    Abstract class for setting up a 3D scene and animating it.
    """

    def __init__(self, title, frame_rate, run_time):
        """
        Create a new Animation.

        Arguments:
            title: str, the window title
            frame_rate: float, the number of frames to display per second
            run_time: float, the number of seconds to run the animation
        """
        self.title = title
        assert 0 < frame_rate < 1000
        self.frame_rate = frame_rate
        assert run_time > 0
        self.run_time = run_time

        self.frame = 0
        self.prev_update_time = None

        # import OpenGL so Qt can use it for rendering
        from OpenGL import GL
        # create the 3D window
        self.view = Qt3DWindow()
        self.view.setX(100)
        self.view.setY(100)

        self.view.setTitle(self.title)

        self.qml_engine = QQmlEngine(self.view)

    def load_qml(self, path, parent):
        """
        Helper method to load an object using Qt's QML system.

        Arguments:
            path: str, a path to a QML file
            parent: QObject, the parent of the object to be loaded

        Returns:
            the loaded QObject
        """
        component = QQmlComponent(self.qml_engine, path, parent)
        obj = component.create()
        if obj is None:
            print('Error loading {}'.format(path))
            for error in component.errors():
                print(error.toString())
            exit()
        return obj

    def add_light(self, position, intensity=1.0, color=util.hsl(0, 0, 100)):
        """
        Helper method to add a simple point light to the scene.

        Arguments:
            position: QVector3D, the position of the light in the scene
            intensity: float, the intensity of the light
            color: QColor, the color of the light
        """
        light_entity = QEntity(self.scene)

        light = QPointLight(light_entity)
        light.setColor(color)
        light.setIntensity(intensity)

        light_transform = QTransform(self.scene)
        light_transform.setTranslation(position)
        light_entity.addComponent(light)
        light_entity.addComponent(light_transform)

    def add_rgb_cube(self):
        """
        Helper method to add an RGB-textured cube to the scene.

        Returns:
            the QTransform of the cube
        """
        cube_entity = QEntity(self.scene)

        cube_mesh = QCuboidMesh()
        cube_entity.addComponent(cube_mesh)

        cube_transform = QTransform(self.scene)
        cube_entity.addComponent(cube_transform)

        if not hasattr(self, 'rgb_cube_material'):
            # load material definition from QML
            # this was the easiest way I could find to create a custom shader in Qt3D...
            self.rgb_cube_material = self.load_qml(os.path.join(os.path.dirname(__file__), 'RGBCubeMaterial.qml'), self.scene)
        cube_entity.addComponent(self.rgb_cube_material)

        return cube_transform

    def add_sphere(self, color=util.hsl(0, 0, 50)):
        """
        Helper method to add a sphere to the scene.

        Returns:
            the QTransform of the sphere
        """
        sphere_entity = QEntity(self.scene)

        sphere_mesh = QSphereMesh()
        sphere_entity.addComponent(sphere_mesh)

        sphere_transform = QTransform(self.scene)
        sphere_entity.addComponent(sphere_transform)

        sphere_material = QPhongMaterial(self.scene)
        sphere_material.setDiffuse(color)
        sphere_entity.addComponent(sphere_material)

        return sphere_transform

    def add_cylinder(self, color=util.hsl(0, 0, 50)):
        """
        Helper method to add a cylinder to the scene.

        Returns:
            the QTransform of the cylinder
        """
        cylinder_entity = QEntity(self.scene)

        cylinder_mesh = QCylinderMesh()
        cylinder_entity.addComponent(cylinder_mesh)

        cylinder_transform = QTransform(self.scene)
        cylinder_entity.addComponent(cylinder_transform)

        cylinder_material = QPhongMaterial(self.scene)
        cylinder_material.setDiffuse(color)
        cylinder_entity.addComponent(cylinder_material)

        return cylinder_transform

    def add_cone(self, color=util.hsl(0, 0, 50)):
        """
        Helper method to add a cone to the scene.

        Returns:
            the QTransform of the cone
        """
        cone_entity = QEntity(self.scene)

        cone_mesh = QConeMesh()
        cone_entity.addComponent(cone_mesh)

        cone_transform = QTransform(self.scene)
        cone_entity.addComponent(cone_transform)

        cone_material = QPhongMaterial(self.scene)
        cone_material.setDiffuse(color)
        cone_entity.addComponent(cone_material)

        return cone_transform

    def add_plane(self, color=util.hsl(0, 0, 50)):
        """
        Helper method to add a plane to the scene.

        Returns:
            the QTransform of the plane
        """
        plane_entity = QEntity(self.scene)

        plane_mesh = QPlaneMesh()
        plane_entity.addComponent(plane_mesh)

        plane_transform = QTransform(self.scene)
        plane_entity.addComponent(plane_transform)

        plane_material = QPhongMaterial(self.scene)
        plane_material.setDiffuse(color)
        plane_entity.addComponent(plane_material)

        return plane_transform

    def add_path(self, *pts, color=util.hsl(0, 0, 50)):
        """
        Helper method to add a path to the scene.

        Arguments:
            pts: list of QVector3D's, the points in the path

        Returns:
            a list of the entities added to the scene
        """
        path_material = QPhongMaterial(self.scene)
        path_material.setDiffuse(color)

        # make a bunch of cylinder objects aligned along the path
        entities = []
        prev_pt = None
        for pt in pts:
            if prev_pt is not None:
                if prev_pt != pt:
                    # for each adjacent pair of points that are different
                    # make a cylinder
                    path_entity = QEntity(self.scene)

                    path_mesh = QCylinderMesh()
                    path_mesh.setRadius(0.05) # very thin
                    path_mesh.setLength((prev_pt - pt).length()) # length is the distance between the points
                    path_entity.addComponent(path_mesh)

                    path_transform = QTransform(self.scene)
                    path_transform.setRotation(QQuaternion.fromDirection(QVector3D(0, 0, -1), prev_pt - pt)) # rotate to point along path
                    path_transform.setTranslation((pt + prev_pt) / 2) # center between points
                    path_entity.addComponent(path_transform)

                    path_entity.addComponent(path_material)

                    entities.append(path_entity)
            prev_pt = pt

        return entities

    def setup_scene(self, background_color, camera_position, camera_lookat):
        """
        Sets up the scene. Should be called before running the animation.

        Arguments:
            background_color: QColor, background color of the scene
            camera_position: QVector3D, the position of the camera in the scene
            camera_lookat: QVector3D, the point that the camera should be pointing at in the scene
        """
        # clear color is the background color
        self.view.defaultFrameGraph().setClearColor(background_color)

        self.scene = QEntity()

        # let subclass populate scene
        self.make_scene()

        # set up camera
        camera = self.view.camera()
        camera.setPosition(camera_position)
        camera.setViewCenter(camera_lookat)

        self.view.setRootEntity(self.scene)

    def make_scene(self):
        """
        Abstract method. Populates the scene with objects.
        """
        raise NotImplementedError()

    def _update(self):
        """
        Updates the animation, rendering the next frame.
        """
        # current animation time in seconds
        t = util.lerp(self.frame, 0, self.frame_rate, 0, 1)
        # change in time since the last frame
        dt = 1 / self.frame_rate if self.prev_update_time is None else t - self.prev_update_time
        # call subclass's frame update
        self.update(self.frame, t, dt)

        # stop the animation and close the window if run past run_time
        if t >= self.run_time:
            self.animation_timer.stop()
            self.view.close()

        self.prev_update_time = t
        self.frame += 1

    def update(self, frame, t, dt):
        """
        Abstract method. Updates one frame of the animation.

        Arguments:
            frame: int, the current frame number
            t: float, the current animation time in seconds
            dt: float, the number of seconds since the last update
        """
        raise NotImplementedError()

    def run(self):
        """
        Runs the animation asynchronously. The animation runs in the background for self.run_time seconds.
        """
        self.animation_timer = QTimer(self.view)
        # timer interval in msecs
        self.animation_timer.setInterval(1000 / self.frame_rate)
        # call update on each timeout of the timer
        self.animation_timer.timeout.connect(self._update)
        self.animation_timer.start()

        # show the main window
        self.view.show()
