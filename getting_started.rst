+++++++++++++++
Getting Started
+++++++++++++++

Python 3.5 (or higher) only
===========================

This documentation is written for Python 3.5 to avail of the new
``async`` and ``await`` keywords.

If you have Python 3.5 installed you only need to install ``aiohttp``:

.. sourcecode:: console

    $ pip install -U aiohttp

If you don't have Python 3.5 installed yet, you have several options
to install it.

All platforms with ``conda``
----------------------------

* Download and install
  `Miniconda <http://conda.pydata.org/miniconda.html>`_  for our platform.
* Create a new Python 3.5 environment (named ``aio35``, use a different
  if you like):

  .. sourcecode:: console

       $ conda create -n aio35 python=3.5

* Activate it.
  Linux and OS X:

  .. sourcecode:: console

       $ source activate aio35

  Windows:

  .. sourcecode:: console

       $ source activate aio35

* Install ``aiohttp``:

  .. sourcecode:: console

       $(aio35) pip install aiohttp


Platform specific
-----------------

.. would be good to have some word about installing on Windows

* Windows: The easiest way to use Python 3.5 would be to use a package manager
  such as conda. See the installation instructions above.
* Mac OS X: Install `Homebrew </usr/bin/ruby -e "$(curl -fsSL
  https://raw.githubusercontent.com/Homebrew/install/master/install)">`_ and
  then type ``brew install python3``
* Linux: Ubuntu 16.04+ and Arch linux ship with Python 3.5 included.
  If you don't have Python 3.5+ on your computer, you can compile it or use
  `Pythonz <https://github.com/saghul/pythonz>`_.


Create a virtual environment to run examples
============================================

If you don't use conda (see above), create a virtual environment:

.. sourcecode:: console

    $ python3 -m venv venv

.. note::
    Depending on your platform, the Python 3 interpreter could be invoked by
    ``python`` instead. This is the case for conda on Windows for example.

Install ``aiohttp`` in the virtual environment:

.. sourcecode:: console

    $ ./venv/bin/python -m pip install -U aiohttp
