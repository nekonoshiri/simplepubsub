from typing import List

from simplepubsub import Publisher


class StubMessage:
    def __init__(self, id: int) -> None:
        self.id = id


class SpySubscriber:
    def __init__(self) -> None:
        self.published_messages: List[StubMessage] = []

    def __call__(self, message: StubMessage) -> None:
        self.published_messages.append(message)


def test_pubsub() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber1 = SpySubscriber()
    subscriber2 = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)

    subscription1 = publisher.subscribe(subscriber1)
    publisher.publish(message1)
    subscription2 = publisher.subscribe(subscriber2)
    publisher.publish(message2)
    publisher.unsubscribe(subscription1)
    publisher.publish(message3)

    assert [msg.id for msg in subscriber1.published_messages] == [1, 2]
    assert [msg.id for msg in subscriber2.published_messages] == [2, 3]

    publisher.unsubscribe(subscription2)


def test_unsubscribe_idempotency() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscription = publisher.subscribe(lambda message: None)
    publisher.unsubscribe(subscription)
    publisher.unsubscribe(subscription)


def test_unsubscribe_all() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber1 = SpySubscriber()
    subscriber2 = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)

    subscription1 = publisher.subscribe(subscriber1)  # noqa: F841
    subscription2 = publisher.subscribe(subscriber2)  # noqa: F841

    publisher.publish(message1)
    publisher.publish(message2)
    publisher.unsubscribe_all()
    publisher.publish(message3)

    assert [message.id for message in subscriber1.published_messages] == [1, 2]
    assert [message.id for message in subscriber2.published_messages] == [1, 2]


def test_delete_subscriber_automatically_when_no_strong_reference() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)

    subscription = publisher.subscribe(subscriber)
    publisher.publish(message1)
    publisher.publish(message2)
    del subscription
    publisher.publish(message3)

    assert [message.id for message in subscriber.published_messages] == [1, 2]


def test_not_delete_subscriber_automatically_when_persist_is_true() -> None:
    publisher: Publisher[StubMessage] = Publisher(persist=True)
    subscriber = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)

    subscription = publisher.subscribe(subscriber)
    publisher.publish(message1)
    publisher.publish(message2)
    del subscription
    publisher.publish(message3)

    assert [message.id for message in subscriber.published_messages] == [1, 2, 3]
