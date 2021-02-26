from unittest.mock import Mock

from tinypubsub import Subscription


def test_unsubscribe():
    unsubscribe = Mock()

    subscription = Subscription(unsubscribe)
    subscription.unsubscribe()

    unsubscribe.assert_called_once_with(subscription)


def test_unsubscribe_is_called_when_exit():
    unsubscribe = Mock()

    with Subscription(unsubscribe) as subscription:
        unsubscribe.assert_not_called()

    unsubscribe.assert_called_once_with(subscription)
