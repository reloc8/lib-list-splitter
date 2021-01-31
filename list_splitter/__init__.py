import sys
from typing import Callable, List, Tuple, Type, TypeVar


A = TypeVar('A')
B = TypeVar('B')


def split(elements: List[Type[A]],
          weight_fun: Callable[[List[Type[A]]], Type[B]],
          weight_max: Type[B],
          size_max: int = sys.maxsize) -> Tuple[List[List[Type[A]]], List[Type[A]]]:
    """Splits a list into batches such that each batch weights less than a threshold

    :param elements:    List to split
    :param weight_fun:  Callable that returns a batch weight
    :param weight_max:  Max batch weight
    :param size_max:    Optional max batch size
    :return:            A tuple containing the list of batches and the list of elements that could not fit in any batch
    """

    batches = [[]]
    ignored = []

    if size_max <= 0:

        ignored = elements
        return batches, ignored

    current_batch = 0
    current_element = 0
    while current_element < len(elements):

        element = elements[current_element]

        batch_weight_before = weight_fun(batches[current_batch])
        batch_weight_after = weight_fun(batches[current_batch] + [element])

        if weight_fun([element]) > weight_max:
            ignored.append(element)
            current_element += 1
        elif batch_weight_before < weight_max \
                and batch_weight_after <= weight_max \
                and len(batches[current_batch]) < size_max:
            batches[current_batch].append(element)
            current_element += 1
        elif len(batches[current_batch]) > 0:
            batches.append([])
            current_batch += 1

    return batches, ignored
