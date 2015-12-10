Introduction
============

* sensor_logger: This is the deamon that periodically logs data from a number
                 of sensors
* multi_sensor_manager_web.py: This is a web application which provides simple
                      representations of the logged data.

Installation
============

Requirements: ::

	pip install tinkerforge
	apt-get install python-sqlite sqlite sqlitebrowser python-sqlalchemy
	# we use version 0.9.3
	pip install bokeh --user --upgrade


::

    python setup.py install


Add to .bashrc

::

	PYTHONPATH=$HOME/.local/lib/python2.7/site-packages/:$PYTHONPATH
	PATH=$HOME/.local/bin:$PATH

Usage
=====


Database structure
==================

