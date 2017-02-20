# Overview

Sentry is a modern error logging and aggregation platform.

# Usage

Step by step instructions on using the charm:

juju deploy sentry

Browse to `http://`

## Scale out Usage

See Known Limitations and Issues

## Known Limitations and Issues

This charm needs to be split into 2 seperate charms - the web and celery worker.  At 
this point, we would be able to scale the charm properly.  At this point, we can only 
scale the web and celery workers together.

# Configuration

The configuration options will be listed on the charm store, however If you're
making assumptions or opinionated decisions in the charm (like setting a default
administrator password), you should detail that here so the user knows how to
change it immediately, etc.

# Contact Information

`joedborg` on Freenode

## Upstream Project Name

  - [Sentry website](https://sentry.io/)
  - [Sentry bug tracker](https://github.com/getsentry/sentry/issues)


[service]: http://example.com
[icon guidelines]: https://jujucharms.com/docs/stable/authors-charm-icon
