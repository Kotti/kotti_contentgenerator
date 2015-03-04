kotti_contentgenerator
**********************

This is an extension to `Kotti`_ that allows adding lots of fake content to
your website. This could be useful in various testing situations (performance,
having dummy content inserted in your testing website, etc).

. image:: screenshots/contentgenerator.png
  :alt: kotti_contentgenerator screenshot

Usage
=====

You can get the `@@contentgenerator` view by including `kotti_contentgenerator.views`
to your `pyramid.includes` setting::

    pyramid.includes =
        pyramid_debugtoolbar
        pyramid_tm
        kotti_contentgenerator.views

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
