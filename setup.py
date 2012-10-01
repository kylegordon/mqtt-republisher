from sys import version

from distutils.core import setup
setup(name='mqtt-republisher',
    version='0.99',
    description='MQTT topic remapper and republisher',
    author='Kyle Gordon',
    author_email='kyle@lodge.glasgownet.com',
    url='http://github.com/kylegordon/mqtt-republisher',
    download_url='http://github.com/kylegordon/mqtt-republisher',
    license='GNU General Public License v3 or later (GPLv3+)',
    py_modules=['mqtt-republisher'],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Topic :: Communications',
    'Topic :: Internet',
    ]
    )
