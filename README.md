# bbgo
.. image:: https://secure.travis-ci.org/genonfire/bbgo.svg
    :target: http://travis-ci.org/genonfire/bbgo
Total bbs system made by django

https://gencode.me/bbgo


`bbgo` is a middleware based on Django web framework. It may help you build web service nice, quick and easy.

    - Building community? Start quickly with pre-implemented member service, boards and blogs.
    - Looking for a groupware? Host your free groupware with bbgo.
    - Want to build your own web service? MVT(Model, View, Template) structures of Django are very easy to customize.
    - It is free and open source.

# Getting started with bbgo
bbgo 2.0 is being refactored with 100% Django REST Framework + Vue.js (TBD).

It will be working on Django 2.2 and Python 3

    $ git clone https://github.com/genonfire/bbgo.git
    $ pip install -r requirements.txt

English > https://gencode.me/16/

Korean > https://gencode.me/28/


# Secrets and Config
Create secrets.json from the sample file then fill all required keys such as DB_NAME, DB_USER and DB_PASSWORD.
It is highly suggested to use your own generated SECRET_KEY.

    $ cp docs/secrets_sample.json secrets.json


# Legacy version of bbgo
Branch : 1.x
For bbgo 1.x > https://gencode.me/1/

bbgo 1.x supports Django 1.11 and python 2.7
bbgo 1.x has various apps which are implemented by Django MVT model with function view, templates, jquery and simple CSS.

    $ git clone https://github.com/genonfire/bbgo.git
    $ git checkout -b 1.x
    $ pip install -r requirements.txt


# Issue management
http://jira.gencode.me/projects/BBGO/issues/filter=allissues


# Tested by
<a href="https://www.browserstack.com/">
<img src="./docs/browserstack.png" width="50%">
</a>

BrowserStack - A cross-browser testing tool.
