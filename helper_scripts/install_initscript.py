#!/usr/bin/env python
from pkg_resources import Requirement, resource_filename

filename = resource_filename(Requirement.parse("MyProject"), "sample.conf")
