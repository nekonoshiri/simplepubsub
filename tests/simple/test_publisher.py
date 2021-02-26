from tinypubsub import Publisher
from tinypubsub.simple import SimplePublisher


class SpySubscriber:
    def __init__(self):
        self.published_messages = []

    def __call__(self, message):
        self.published_messages.append(message)


def test_publish_subscribe_unsubscribe():
    publisher: Publisher[str] = SimplePublisher()
    subscriber1 = SpySubscriber()
    subscriber2 = SpySubscriber()

    subscription1 = publisher.subscribe(subscriber1)
    publisher.publish("m1")

    subscription2 = publisher.subscribe(subscriber2)
    publisher.publish("m2")

    publisher.unsubscribe(subscription1)
    publisher.publish("m3")

    assert subscriber1.published_messages == ["m1", "m2"]
    assert subscriber2.published_messages == ["m2", "m3"]

    publisher.unsubscribe(subscription2)


def test_unsubscribe_idempotency():
    publisher: Publisher[str] = SimplePublisher()
    subscription = publisher.subscribe(lambda message: None)
    publisher.unsubscribe(subscription)
    publisher.unsubscribe(subscription)


def test_unsubscribe_all():
    publisher: Publisher[str] = SimplePublisher()
    subscriber1 = SpySubscriber()
    subscriber2 = SpySubscriber()

    publisher.subscribe(subscriber1)
    publisher.subscribe(subscriber2)

    publisher.publish("m1")
    publisher.publish("m2")
    publisher.unsubscribe_all()
    publisher.publish("m3")

    assert subscriber1.published_messages == ["m1", "m2"]
    assert subscriber2.published_messages == ["m1", "m2"]


def test_unsubscribe_via_subscription():
    publisher: Publisher[str] = SimplePublisher()
    subscriber = SpySubscriber()

    subscription = publisher.subscribe(subscriber)

    publisher.publish("m1")
    publisher.publish("m2")

    subscription.unsubscribe()

    publisher.publish("m3")

    assert subscriber.published_messages == ["m1", "m2"]


def test_unsubscribe_via_subscription_using_context_manager():
    publisher: Publisher[str] = SimplePublisher()
    subscriber = SpySubscriber()

    with publisher.subscribe(subscriber):
        publisher.publish("m1")
        publisher.publish("m2")

    publisher.publish("m3")

    assert subscriber.published_messages == ["m1", "m2"]
