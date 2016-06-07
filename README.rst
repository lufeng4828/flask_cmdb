flask_cmdb
============================

cmdb api client


Installation
------------

Installing is simple with pip::

    $ pip install flask-cmdb


Usage
-----

Setting up the debug toolbar is simple::

    from flask import Flask
    from flask_cmdb import CMDB

    app = Flask(__name__)
    cmdb = CMDB(app)
