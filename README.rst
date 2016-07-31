POBOT's ``pybot`` collection
============================

This package is part of POBOT's ``pybot`` packages collection, which aims
at gathering contributions created while experimenting with various technologies or
hardware in the context of robotics projects.

Although primarily focused on robotics applications (taken with its widest acceptation)
some of these contributions can be used in other contexts. Don't hesitate to keep us informed
on any usage you could have made.

Package content
===============

General interest fabric (http://www.fabfile.org/) tasks.

Installation
============

::

    $ cd <PROJECT_ROOT_DIR>
    $ python setup.py install

Documentation
=============

Usage
-----

Example:
::

    from pybot.fabtasks import *
    from fabric.api import env
    from fabric.state import output

    env.hosts = ['rpi3']
    output.output = False

This fabric file defines the remote host as `rpi3` and makes fabric output a bit less verbose by not
displaying the invoked commands output.


Provided tasks
--------------

In short :

- version number management : increment major, minor, build/patch numbers independently
- wheel package generation
- deployment on target host(s)
- remote installation on target host(s)
- macro-task chaining wheel generation, deployment and installation on host(s)

Use `fab --list` to display the tasks and their description.

