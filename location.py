import sys
import os

dyn_dir = "System"
_home = os.getcwd()
_userbase_dir = os.getcwd() + os.sep + dyn_dir
sys.path.append(_userbase_dir)
try: os.chdir(_userbase_dir)
except: print "Failed to find " + _userbase_dir + "\nHopefuly you are running setup.py which would make this error normal."
