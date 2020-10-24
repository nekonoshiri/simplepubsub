from typing import Callable, Generic, MutableMapping, TypeVar
from weakref import WeakKeyDictionary

from .subscription import Subscription

Message = TypeVar("Message")


class Publisher(Generic[Message]):
    """出版クラス。

    購読の開始・停止および購読者へのメッセージの出版を行うメソッドを提供し、
    購読の開始により登録されたコールバックを保持します。

    :param Message: 型パラメーター。メッセージの型を表します。
    """

    def __init__(self, persist: bool = False) -> None:
        """コンストラクタ。

        :param persist: 参照されなくなった `Subscription` を保持し続けるかどうか。

            デフォルトの ``False`` の場合、`subscribe` メソッドの戻り値
            （`Subscription` クラスのインスタンス）
            が参照されなくなった場合に自動的に購読が停止されます。
            但し、この場合 `unsubscribe` メソッドが呼ばれることは保証されません。
            これは、`unsubscribe` メソッドを呼び忘れた場合に
            メモリリークを防止するのに役立ちます。

            このパラメータを ``True`` にすると、
            明示的に購読を停止しない限り購読を停止しません。
        """

        if persist:
            self._subscribers: MutableMapping[
                Subscription, Callable[[Message], None]
            ] = {}
        else:
            self._subscribers = WeakKeyDictionary()

    def publish(self, message: Message) -> None:
        """全ての購読者にメッセージを出版します。

        登録されている全てのコールバックを ``message`` を引数にして呼び出すことで、
        全ての購読者にメッセージを出版します。
        呼び出される順番は規定されていません。

        :param message: 出版するメッセージ。
        """
        for subscriber in self._subscribers.values():
            subscriber(message)

    def subscribe(self, subscriber: Callable[[Message], None]) -> Subscription:
        """購読を開始します。

        ``subscriber`` 引数で指定されたコールバックを登録することで、購読を開始します。
        登録されたコールバックは、`publish` メソッドによって呼び出されます。

        :param subscriber: 登録するコールバック（呼び出し可能オブジェクト）。
        :return: 購読情報。購読を識別するために使用されます。
        """
        subscription = Subscription(self.unsubscribe)
        self._subscribers[subscription] = subscriber
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """購読を停止します。

        購読を停止すると、購読を開始したときに登録した
        コールバックは最早呼び出されなくなります。
        このメソッドは冪等です。即ち、複数回呼び出しても問題ありません。

        :param subscription: 購読情報。`subscribe` メソッドで購読を開始したときの
            戻り値を指定します。
        """
        self._subscribers.pop(subscription, None)

    def unsubscribe_all(self) -> None:
        """全ての購読を停止します。

        デフォルトの実装では、このメソッドは `unsubscribe` メソッドを呼び出しません。
        そのため、`unsubscribe` メソッドをオーバーライドして、このメソッドが
        呼び出されたときにオーバーライドした `unsubscribe` メソッドが
        常に呼び出されるようにしたい場合は注意してください。
        """
        self._subscribers.clear()
