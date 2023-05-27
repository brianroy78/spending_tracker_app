import typing as ty
from functools import partial

A = ty.TypeVar("A")
D = ty.TypeVar("D")
E = ty.Callable[[A], D]
G = ty.Callable[[A], ty.Iterator[D]]


class Functor(ty.Generic[A]):
    def __init__(self, value: A):
        self.value: A = value

    def apply(self, func: E) -> "Functor[D]":
        return Functor(func(self.value))

    def split(self, func: G) -> "IterFunctor[D]":
        return IterFunctor(func(self.value))


B = ty.Iterator[A]
F = ty.Iterator[D]
C = ty.Callable[[B], F]
H = ty.Callable[[B], D]


class IterFunctor(ty.Generic[A]):
    def __init__(self, value: B):
        self.value: B = value

    def apply(self, func: C) -> "IterFunctor[D]":
        return IterFunctor(func(self.value))

    def map(self, func: E) -> "IterFunctor[D]":
        return IterFunctor(map(func, self.value))

    def flat(self, func: H) -> Functor[D]:
        return Functor(func(self.value))

    def list(self):
        return list(self.value)

    def map_partial(self, func: E, *args, **kwargs) -> "IterFunctor[D]":
        return IterFunctor(map(partial(func, *args, **kwargs), self.value))

    def apply_partial(self, func: C, *args, **kwargs) -> "IterFunctor[D]":
        return IterFunctor(partial(func, *args, **kwargs)(self.value))
