"""単純な pub/sub パターンの実装です。

手動で ``subscribe``/``unsubscribe`` する場合
=============================================

手動で ``subscribe`` した場合は必ず ``unsubscribe`` を行うのを
忘れないようにしてください。

.. code-block::

    from simplepubsub import Publisher


    def subscriber(message):
        print(message)


    publisher = Publisher()
    subscription = publisher.subscribe(subscriber)
    publisher.publish("hello")  # 出力される

    subscription.unsubscribe()
    publisher.publish("hi")  # 出力されない

デフォルトでは、メモリリークを防ぐため、`Publisher.subscribe` メソッドの戻り値
（`Subscription` クラスのインスタンス）が参照されなくなった場合は
自動的に購読が停止されます。
但し、この場合 ``unsubscribe`` メソッドが呼ばれることは保証されません。

.. code-block::

    from simplepubsub import Publisher


    def subscriber(message):
        print(message)


    publisher = Publisher()


    def subscribe():
        # 戻り値を使わずに捨てるため自動的に購読が停止される
        # （通常は明示的に unsubscribe を行うことを推奨します）
        publisher.subscribe(subscriber)


    subscribe()
    publisher.publish("hi")  # 出力されない

``persist`` オプションを ``True`` にすることで、
`Publisher.subscribe` の戻り値（`Subscription` クラスのインスタンス）が
参照されなくなった場合でも購読を停止しないようにすることができます。

.. code-block::

    from simplepubsub import Publisher


    def subscriber(message):
        print(message)


    publisher = Publisher(persist=True)


    def subscribe():
        publisher.subscribe(subscriber)


    subscribe()
    publisher.publish("hello")  # 出力される

    publisher.unsubscribe_all()

コンテキストマネージャを使用する場合
====================================

``with`` 文を抜けると自動で `Subscription.unsubscribe` メソッドが呼ばれるため、
安全です。

.. code-block::

    from simplepubsub import Publisher


    def subscriber(message):
        print(message)


    publisher = Publisher()

    with publisher.subscribe(subscriber):
        publisher.publish("hello")  # 出力される

    publisher.publish("hi")  # 出力されない
"""

from .publisher import Publisher
from .subscription import Subscription
