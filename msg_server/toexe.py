#coding:utf-8

from distutils.core import setup 
import py2exe 


pys = ["client_server.py"]
#pys = ["testexe.py"]

setup(
      console=pys,
      dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 
                'tcl84.dll', 'tk84.dll', 'POWRPROF.dll']
      )