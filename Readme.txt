Introduction
============

* sensor_logger: This is the deamon that periodically logs data from a number
                 of sensors
* web_sensor_manager: This is a web application which provides simple
                      representations of the logged data.

Installation
============

Requirements: ::

	pip install tinkerforge
	apt-get install  python-sqlite sqlite  sqlitebrowser


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

