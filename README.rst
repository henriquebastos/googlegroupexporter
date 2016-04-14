GoogleGroup Exporter - Unlock your mailing list
===============================================

.. image:: https://img.shields.io/pypi/v/googlegroupexporter.svg
    :target: https://pypi.python.org/pypi/googlegroupexporter

.. image:: https://img.shields.io/pypi/dm/googlegroupexporter.svg
        :target: https://pypi.python.org/pypi/googlegroupexporter

GoogleGroup Exporter is an extensible tool for retrieving and analysing
your mailing list content.


Features
--------

* Dump all your messages into a *mbox* file so you can explore the
  content using email clients.

* Export all your topics with title, author, date and url to a csv
  file so you can easily explore it on a spreadsheet.

* Support extraction of private groups using your browser's cookies.

* Download all content in parallel.

* Transparently cache all requests so you can inexpensively retry
  or process the content in different ways.

* Offers an easy extension API so you write your own scripts.


Installation and Usage
----------------------

Install Python 3.5 or greater and then simply::

    pip install googlegroupexporter

Then execute the program::

    ggexport my-public-group

By default, ``ggexport`` will generate a ``my-public-group.mbox`` file
with all the messages. Then you can open it with you preferred email
client.


Exporting a Private Group
-------------------------

To export a private group you need to inform your cookie header string
to ``ggexport``.

To retrieve the cookie header on Google Chrome:

1. Login into you Google Account;
2. Visit your GoogleGroup page, for example::

    https://groups.google.com/forum/#!forum/my-private-group

3. Then inspect the page with Chrome's Developer Tool;
4. Go to ``Network``;
5. Select a request to the domain ``groups.google.com``;
6. Select ``Headers``;
7. Search for ``Request Headers``;
8. Look for the ``Cookie`` key;
9. **Copy the cookie header value string**;

Then run::

    ggexport my-private-group --cookies "COOKIE-HEADER-STRING-COPIED-FROM-MY-BROWSER"

Listing your group topics
-------------------------

To create a `csv` listing all your group's topics along with their
urls, authors, dates and number of messages, run::

    ggexport my-public-group --mode csv

How to contribute
-----------------

Fork this repository, checkout your fork, then::

    python -m venv .gge
    source .gge/bin/activate
    python setup.py develop

Change what you want, then run the tests::

    python setup.py test

To run your developed code you can use the command ``ggexport`` or run
the module ``python -m googlegroupexporter``.

When everything works, submit a *pull request*.


License
-------

MIT License
