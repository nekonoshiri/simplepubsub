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

## Features

- `tinypubsub.Publisher` has abstract methods: `publish`, `subscribe`, `unsubscribe`, `unsubscribe_all`.
- `tinypubsub.simple.SimplePublisher`: Dict-based implementation of `Publisher`.
- `tinypubsub.weakref.WeakrefPublisher`: WeakKeyDictionary-based implementation of `Publisher`.

## API

### Module `tinypubsub`

#### *abstract class* `Publisher[Message]`

Abstract publisher class.

##### *type parameter* `Message`

Type of message that will be published.

##### *abstract method* `publish(message: Message) -> None`

Publish message to subscribers.

##### *abstract method* `subscribe(subscriber: Callable[[Message], None]) -> Subscription`

Add subscriber.

##### *abstract method* `unsubscribe(subscription: Subscription) -> None`

Delete subscriber.

##### *abstract method* `unsubscribe_all() -> None`

Delete all subscribers.

#### *class* `Subscription`

Return value of `Publisher.subscribe()`.
It can be used as a context manager as:

```Python
with publisher.subscribe(...) as subscription:
    ...
```

and `subscription.unsubscribe()` will be called when exit.

##### *method* `unsubscribe() -> None`

`subscription.unsubscribe()` is the same as `publisher.unsubscribe(subscription)`, where `subscription = publisher.subscribe(...)`.

### Module `tinypubsub.simple`

#### *class* `SimplePublisher[Message]`

Implementation of `Publisher[Message]`.

### Module `tinypubsub.weakref`

#### *class* `WeakrefPublisher[Message]`

Implementation of `Publisher[Message]`.

This implementation uses WeakKeyDictionary to manage subscribers.
This may prevent a memory leak if subscription loses all strong references before unsubscribed:

```Python
publisher = WeakrefPublisher()

subscription = publisher.subscribe(...)

assert len(publisher._subscribers) == 1

del subscription

assert len(publisher._subscribers) == 0
```

Note that the `unsubscribe` method will not be called in the above case,
so normally you should unsubscribe explicitly or use context manager.

