# WPI CS 4732 Project 2: Forward Kinematics

by [Daniel Beckwith](https://github.com/dbeckwith)

[Demo](https://youtu.be/5DQCg-qx8T8)

## Installation

First, make sure Python 3.5 is installed. Then, use `pip` to install the dependencies:

```bash
pip install -r requirements.txt
```

This will install the [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5), [PyOpenGL](http://pyopengl.sourceforge.net/), and [PyQt3D](https://www.riverbankcomputing.com/software/pyqt3d/intro) packages. If you're on Windows and `pip` can't install some of the packages, you may have to download the appropriate wheel files from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/) and install them using `pip`:

```bash
pip install path/to/wheel1 path/to/wheel2 ...
```

You may want to do this in a [Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) if you don't have administrative privilages.

## Usage

From the project root, run the python module to start the animation:

```bash
python -m proj2
```
