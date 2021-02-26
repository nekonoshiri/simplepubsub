from __future__ import annotations

from types import TracebackType
from typing import Callable, ContextManager, Optional, Type


class Subscription(ContextManager["Subscription"]):
    """購読情報を格納するクラスです。

    このクラスのインスタンスは、コンテキストマネージャとして
    ``with`` 文と共に使用することができます。
    ``with`` 文と共に使用する場合、``with`` 文を抜けると自動的に
    `unsubscribe` メソッドが呼び出されます。

    .. code-block:: python

        from tinypubsub import Publisher


        def subscriber(message):
            print(message)


        publisher = Publisher()

        with publisher.subscribe(subscriber):
            publisher.publish("hello")  # 出力される

        publisher.publish("hi")  # 出力されない
    """

    def __init__(self, unsubscribe: Callable[[Subscription], None]) -> None:
        """コンストラクタ。

        このクラスを直接インスタンス化しないでください。
        このクラスのインスタンスは、
        `Publisher.subscribe` メソッドを通じて生成されます。
        """
        self._unsubscribe: Callable[[Subscription], None] = unsubscribe

    def __enter__(self) -> Subscription:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.unsubscribe()

    def unsubscribe(self) -> None:
        """購読を停止します。

        このメソッドは、自身を生成した `Publisher` の
        `Publisher.unsubscribe` メソッドを、自身を引数にして呼び出します。

        このメソッドを使用せずに、直接
        `Publisher.unsubscribe` メソッドを利用しても構いません。
        """
        self._unsubscribe(self)
