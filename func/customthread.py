from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from typing import Any


class Worker(Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.target = target
        self.args = args
        self.value = None
    def run(self):
        self.value = self.target(*self.args)