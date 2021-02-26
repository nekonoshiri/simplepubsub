from tinypubsub import Publisher
from tinypubsub.weakref import WeakrefPublisher


class SpySubscriber:
    def __init__(self):
        self.published_messages = []

    def __call__(self, message):
        self.published_messages.append(message)


def test_publish_subscribe_unsubscribe():
    publisher: Publisher[str] = WeakrefPublisher()
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
    publisher: Publisher[str] = WeakrefPublisher()
    subscription = publisher.subscribe(lambda message: None)
    publisher.unsubscribe(subscription)
    publisher.unsubscribe(subscription)


def test_unsubscribe_all():
    publisher: Publisher[str] = WeakrefPublisher()
    subscriber1 = SpySubscriber()
    subscriber2 = SpySubscriber()

    subscription1 = publisher.subscribe(subscriber1)  # noqa: F841
    subscription2 = publisher.subscribe(subscriber2)  # noqa: F841

    publisher.publish("m1")
    publisher.publish("m2")
    publisher.unsubscribe_all()
    publisher.publish("m3")

    assert subscriber1.published_messages == ["m1", "m2"]
    assert subscriber2.published_messages == ["m1", "m2"]


def test_delete_subscriber_automatically_when_subscription_lose_reference():
    publisher: Publisher[str] = WeakrefPublisher()
    subscriber = SpySubscriber()

    subscription = publisher.subscribe(subscriber)
    publisher.publish("m1")
    publisher.publish("m2")
    del subscription
    publisher.publish("m3")

    assert subscriber.published_messages == ["m1", "m2"]


def test_unsubscribe_via_subscription():
    publisher: Publisher[str] = WeakrefPublisher()
    subscriber = SpySubscriber()

    subscription = publisher.subscribe(subscriber)

    publisher.publish("m1")
    publisher.publish("m2")

    subscription.unsubscribe()

    publisher.publish("m3")

    assert subscriber.published_messages == ["m1", "m2"]


def test_unsubscribe_via_subscription_using_context_manager():
    publisher: Publisher[str] = WeakrefPublisher()
    subscriber = SpySubscriber()

    with publisher.subscribe(subscriber):
        publisher.publish("m1")
        publisher.publish("m2")

    publisher.publish("m3")

    assert subscriber.published_messages == ["m1", "m2"]
