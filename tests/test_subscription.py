from typing import List

from tinypubsub import Publisher


class StubMessage:
    def __init__(self, id: int) -> None:
        self.id = id


class SpySubscriber:
    def __init__(self) -> None:
        self.published_messages: List[StubMessage] = []

    def __call__(self, message: StubMessage) -> None:
        self.published_messages.append(message)


def test_unsubscribe() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)

    subscription = publisher.subscribe(subscriber)
    publisher.publish(message1)
    subscription.unsubscribe()
    publisher.publish(message2)

    assert [message.id for message in subscriber.published_messages] == [1]


def test_context_manager() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)

    with publisher.subscribe(subscriber):
        publisher.publish(message1)
        publisher.publish(message2)

    publisher.publish(message3)

    assert [message.id for message in subscriber.published_messages] == [1, 2]


def test_unsubscribe_within_context_manager() -> None:
    publisher: Publisher[StubMessage] = Publisher()
    subscriber = SpySubscriber()
    message1 = StubMessage(1)
    message2 = StubMessage(2)
    message3 = StubMessage(3)
    message4 = StubMessage(4)

    with publisher.subscribe(subscriber) as subscription:
        publisher.publish(message1)
        publisher.publish(message2)
        subscription.unsubscribe()
        publisher.publish(message3)

    publisher.publish(message4)

    assert [message.id for message in subscriber.published_messages] == [1, 2]
