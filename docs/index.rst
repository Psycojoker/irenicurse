.. Irenicurse documentation master file, created by
   sphinx-quickstart on Sun Mar 11 19:10:32 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Irenicurse!
======================

Irenicurse is a project that have the aim to create an high level python framework to write
ncurse applications. It is based on `urwid <http://excess.org/urwid/>`_, a python ncurse library.

.. Note:: You can find the project repository `here <https://github.com/Psycojoker/irenicurse>`_.

Focus
-----

* simplicity
* allow to dev very fast, at least for most of the standard and simple use cases
* promote re-usability as much as possible
* if possible, be easy and fast to learn

Approach
--------

Build a collection of high level generic widgets and allowing the user to
extends those widgets to match his needs. The transitions betweens widgets is
very similar to the call/answer mechanism of the `smalltalk web framework
seaside <http://seaside.st>`_.

In a nutshell, the current widget can "*call*" another widget and give him a
callback, this widget will then be the current widget, it can then, if desired,
"*answer*". This will the callback, with arguments if necessary and the focus
will be given back to the first widget.

Example: in a todo list manager, the main widget is a TodoListWidget that
display the title of a list of todos. When the user press some key, the
TodoListWidget will call a EditTodoWidget that will display a detail view of
the todo with editing possibility. Then, the EditTodoWidget will answer by
calling the callback with the modified todo, this callback will then save this
modified todo.

Installation
============

From source
-----------

First, get the source::

    git clone https://github.com/Psycojoker/irenicurse

Then::

    python setup.py install

Using pip
---------

Simply (no release are available yet on pypi).::

    pip install git+git://github.com/Psycojoker/irenicurse.git

Make sure that your version of pip is recent enough. If you get an error, simply update it with::

    pip install -U pip


.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

