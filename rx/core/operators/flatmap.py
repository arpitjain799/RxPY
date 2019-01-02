import collections
from typing import Any, Callable
from rx.core import Observable, StaticObservable
from rx.core.typing import Mapper, MapperIndexed
from rx.internal.utils import is_future

from .map import mapi
from .merge import merge_all


def _flat_map(source, mapper=None, mapper_indexed=None):
    def projection(x, i):
        mapper_result = mapper(x) if mapper else mapper_indexed(x, i)
        if isinstance(mapper_result, collections.abc.Iterable):
            result = StaticObservable.from_(mapper_result)
        else:
            result = StaticObservable.from_future(mapper_result) if is_future(
                mapper_result) else mapper_result
        return result

    return source.pipe(
        mapi(projection),
        merge_all()
    )


def flat_map(mapper: Mapper = None) -> Callable[[Observable], Observable]:
    """One of the Following:
    Projects each element of an observable sequence to an observable
    sequence and merges the resulting observable sequences into one
    observable sequence.

    Example:
        >>> flat_map(lambda x: Observable.range(0, x))

    Or:
    Projects each element of the source observable sequence to the other
    observable sequence and merges the resulting observable sequences
    into one observable sequence.

    Example:
        >>> flat_map(Observable.of(1, 2, 3))

    Keyword arguments:
    mapper -- A transform function to apply to each element or an
        observable sequence to project each element from the source
        sequence onto.

    Returns:
        An operator function that takes a source observable and returns
        an observable sequence whose elements are the result of invoking
        the one-to-many transform function on each element of the
        input sequence .
    """

    def partial(source: Observable) -> Observable:
        if callable(mapper):
            ret = _flat_map(source, mapper=mapper)
        else:
            ret = _flat_map(source, mapper=lambda _: mapper)

        return ret
    return partial


def flat_mapi(mapper_indexed: MapperIndexed = None) -> Callable[[Observable], Observable]:
    """One of the Following:
    Projects each element of an observable sequence to an observable
    sequence and merges the resulting observable sequences into one
    observable sequence.

        >>> flat_mapi(lambda x, i: Observable.range(0, x))

    Or:
    Projects each element of the source observable sequence to the other
    observable sequence and merges the resulting observable sequences
    into one observable sequence.

        >>> flat_mapi(Observable.of(1, 2, 3))

    Args:
        mapper_indexed -- [Optional] A transform function to apply to
            each element or an observable sequence to project each
            element from the source sequence onto.

    Returns:
        An operator function that takes a source observable and returns
        an observable sequence whose elements are the result of invoking
        the one-to-many transform function on each element of the input
        sequence.
    """

    def partial(source: Observable) -> Observable:
        if callable(mapper_indexed):
            ret = _flat_map(source, mapper_indexed=mapper_indexed)
        else:
            ret = _flat_map(source, mapper=lambda _: mapper_indexed)
        return ret
    return partial
