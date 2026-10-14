"""A tiny name -> class registry: components register themselves, configs pick them by string.

WHAT PROBLEM THIS SOLVES

Picking "which implementation to use" with an `if/elif` chain or a hand-written dict means every new model, loss or
dataset edits one central place. A `Registry` moves that decision into a name: a new implementation registers ITSELF,
in its own file, and nothing central grows.

    BACKBONES = Registry("backbone")

    @BACKBONES.register("transformer_small")
    class SmallTransformer:
        ...

    model = BACKBONES.build(config["backbone"], **config["backbone_args"])

No `if name == ...` anywhere, ever: not here, not in the caller.

WHY NOT MORE THAN THIS (no plugin discovery, no auto-import): build those only once a real need shows up (Rule of Three).
"""
from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """Named registry for one kind of thing (e.g. all backbones).

    One instance per protocol, so a bad lookup fails with a message naming the
    kind of thing that was being looked up, not a bare `KeyError`.

    Registers anything CALLABLE that returns a `T` — a class (called as a
    constructor) or a plain factory function, which is why this is typed
    `Callable[..., T]` rather than `type[T]`: a class is already callable.
    """

    def __init__(self, kind: str):
        self.kind = kind
        self._items: dict[str, Callable[..., T]] = {}

    def register(self, name: str):
        """Decorator: `@BACKBONES.register("transformer_small")` — on a class or a function."""
        def deco(fn: Callable[..., T]) -> Callable[..., T]:
            if name in self._items:
                raise ValueError(
                    f"{self.kind} {name!r} already registered to "
                    f"{self._items[name].__qualname__}"
                )
            self._items[name] = fn
            return fn
        return deco

    def build(self, name: str, /, **kwargs) -> T:
        """Look up by name AND construct, in one call.

        This is the shape a config value actually needs to take: a plain
        string (`config["backbone"]`, from a dict or a `yaml.safe_load()`'d
        file, no code-path difference) goes in, a ready-to-use instance comes
        out. `**kwargs` forwards to the constructor.
        """
        return self.get(name)(**kwargs)

    def get(self, name: str) -> Callable[..., T]:
        try:
            return self._items[name]
        except KeyError:
            available = ", ".join(sorted(self._items)) or "(none registered)"
            raise KeyError(
                f"unknown {self.kind} {name!r}; available: {available}"
            ) from None

    def names(self) -> list[str]:
        return sorted(self._items)
