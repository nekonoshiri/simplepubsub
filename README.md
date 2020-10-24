# simplepubsub

Simple Pub/Sub pattern implementation

## Usage

```
from simplepubsub import Publisher


def subscriber(message):
    print(message)


publisher = Publisher()

subscription = publisher.subscribe(subscriber)

publisher.publish("will be printed")

subscription.unsubscribe()

publisher.publish("will not be printed")
```

Or you can use with `with` statement:

```
from simplepubsub import Publisher


def subscriber(message):
    print(message)


publisher = Publisher()

with publisher.subscribe(subscriber):
    publisher.publish("will be printed")

publisher.publish("will not be printed")
```

