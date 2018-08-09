from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

def handle(req):
    sourcefiles = ['cube.pyx','lib/cube_c.c']
    ext_modules = [Extension("cube", 
                              sourcefiles
                              )]
    
    setup(
      name = 'cube app',
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules
    )
    return req
