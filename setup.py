import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    README = ''
    CHANGES = ''


setup(
    name='Flask-CMDB',
    version='0.1.0',
    license='BSD',
    url='https://github.com/lufeng4828/flask_cmdb',
    author='Feng Lu',
    author_email='lufeng044@qq.com',
    maintainer='Feng Lu',
    maintainer_email='lufeng044@qq.com',
    description='A cmdb api client for Flask applications.',
    long_description=README + '\n\n' + CHANGES,
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    packages=['flask_cmdb'
    ],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
