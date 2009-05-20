.. _getting_started:

PyFactory: Howto
=====================================

You should read the :ref:`install` section, if you haven't installed
*PyFactory* yet.

Basic Example: Creating a Factory for a :class:`User` class
-------------------------------------
Suppose you have two ``.py`` files::

  [~/django-project/site]
  % ls
  models.py    tests.py

The file named ``models.py`` contains your Django-Models and ``tests.py`` the
unit-tests of your Django models. 
The contents of the classes might be:

``models.py``:

.. literalinclude:: ../../examples/models.py

``tests.py``:

.. literalinclude:: ../../examples/tests.py

Writing the Factory
-------------------------------------

Your factories must be derived from pyfactory.FactoryObject class. In the
inner ``Meta``-class ``class`` of the model, which should be created
through the factory, and the actual ``name`` of the factory must be specified.
The ``Elements``-class contains the actual fields with which the factory should
be initialized.


Creating the objects.
-------------------------------------

The actual objects are created through the 
``pyfactory.Factory.*('factory_name')`` methods. There are currently three
methods, which can be used to create models:

* ``build``: Only builds the model, but doesn't actually save it
* ``create``: Creates the model and saves it.
* ``attributes_for``: Returns a dictionary of the fields used to create the
  model.

Moreover named parameters can be passed to those methods in order to overwrite
the default-values specified in the ``Elements``-inner-class of the factory
code::
  
  pyfactory.Factory.build('user', name='overwritten name') 
  # => (<User name='overwritten name', ...>)
  

Special Elements
-------------------------------------

There are some special attributes which can be used to create referenced models
via other factories or which can be used to create unique values, like the
original `factory_girl`_. Currently the following attributes are exising:

* ``pyfactory.Foreign`` can be used to assign the results of an other 
  Factory to the assigned attribute.
* ``Generator`` can be used to create unique values to test attributes with
  a ``unique`` constraint. A callback must be specified to which an unique id
  gets passed.

You might define your own special attributes by deriving from
``pyfactory.FactoryAttribute``.

.. _factory_girl: http://github.com/thoughtbot/factory_girl/tree/master
