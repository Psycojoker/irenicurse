# Introduction

Irenicurse is a project to build an high level python framework to write ncurse
applications. It is based on the awesome [urwid](http://excess.org/urwid/) and
aim for simplicity, fast development speed and reusability. Widget management
is inspired by the smalltalk framework seaside with it's call/answer mechanism.

Currently the project is already usable and stable (it's an abstraction of
urwid) but lack of content and of a real documentation.

# Documentation

You can find it here: (for the moment this is pretty much empty) http://irenicurse.readthedocs.org

You can also find code example in the examples/ directory.

# Installation

From source:

    git clone https://github.com/Psycojoker/irenicurse
    cd irenicurse
    python setup.py install

Using pip:

    pip install git+git://github.com/Psycojoker/irenicurse.git

Make sure your pip version is recent enough otherwise the git+ syntax isn't
supported.
