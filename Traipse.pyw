#!/usr/bin/env python
import runpy

#This sets the install Dir, and Enviromental variables
import location

try: runpy.run_module('start')
except: runpy.run_module('start_release')
