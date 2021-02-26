# tinypubsub

[![PyPI](https://img.shields.io/pypi/v/tinypubsub)](https://pypi.org/project/tinypubsub/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinypubsub)](https://pypi.org/project/tinypubsub/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/nekonoshiri/tinypubsub)](https://github.com/nekonoshiri/tinypubsub/blob/main/LICENSE)

Tiny pub-sub (observer) pattern implementation.

## Usage

```Python
from tinypubsub.simple import SimplePublisher

publisher = SimplePublisher()

subscription = publisher.subscribe(lambda message: print(message))

publisher.publish("Hello!")

publisher.unsubscribe(subscription)
```

Or:

```Python
from tinypubsub.simple import SimplePublisher

publisher = SimplePublisher()

with publisher.subscribe(lambda message: print(message)):
    publisher.publish("Hello!")
```

## API

TODO

