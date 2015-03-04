kotti_contentgenerator
**********************

This is an extension to `Kotti`_ that allows adding lots of fake content to
your website. This could be useful in various testing situations (performance,
having dummy content inserted in your testing website, etc).

Usage
=====

You can get the ``@@contentgenerator`` view by including
``kotti_contentgenerator.views`` to your ``pyramid.includes`` setting::

    pyramid.includes = kotti_contentgenerator.views

Screenshot
----------

.. image:: https://raw.githubusercontent.com/Pixelblaster/kotti_contentgenerator/master/screenshots/contentgenerator.png
  :alt: kotti_contentgenerator screenshot
  :width: 500
  :align: center
  

Beyond the builtin types
------------------------
You can integrate your own content type with kotti_contentgenerator by writing
your own factory and attaching it to 
``kotti_contentgenerator.generator.default_factories``.

If you call the fake content generator from your own call, you can pass the
new factories in the ``Generator`` constructor.::

    from kotti_contentgenerator.generator import Generator
    from kotti.resources import Document, File, get_root
    from kotti_forum.resources import Forum     # example

    generator = Generator(seed=123, depth=2, top_level=10000, sub_level=0,
                          users=2, root_types=(Document,)
                          content_types=(Document, File, Forum)
                          factories={Forum: my_forum_factory}
                          )
    generator.generate(get_root())

The parameters to the Generator constructor are:

    * seed: a number that will seed the faker
    * depth: how many levels deep to go
    * top_level: how many items in the top level
    * sub_level: how many content items to create per level
    * users: how many users to create
    * root_types: content type names of objects to put in root
    * content_types: a list of content type names to build content from
    * factories: a mapping of factories for content, mapped by their content
      type name. This can be used to add new factories

Using a specific seed number is useful because it makes content generation
repeatable. When generating content, kotti_contentgenerator wraps and iterates
through the list of root_types and content_types, making the order of the
generation the same all the time. By using fake-factory and seeding it with the
seed number, the generated strings are the same for all repeated calls.

|build status|_

Development happens at `Github repository`_

.. |build status| image:: https://secure.travis-ci.org/pixelblaster/kotti_contentgenerator.png?branch=master
.. _build status: http://travis-ci.org/pixelblaster/kotti_contentgenerator
.. _Kotti: http://pypi.python.org/pypi/Kotti


Development
===========

Contributions to kotti_contentgenerator are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _Github repository: https://github.com/pixelblaster/kotti_contentgenerator
