from distutils.core import setup, Extension

module1 = Extension('optimised',
                    sources = ['optimised.c', 'vector.c'])

setup (name = 'Optimised',
       version = '1.0',
       description = 'Optimised modules for simulator',
       ext_modules = [module1])
