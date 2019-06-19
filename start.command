#!/usr/bin/env python3
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
print(current_dir)
os.chdir(current_dir)
os.system("pip3 install -r requirements.txt")
os.system("python3 ./sys_listener.py")
