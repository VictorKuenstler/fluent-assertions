import typing

import pytest
from _pytest.outcomes import OutcomeException

T = typing.TypeVar("T")
V = typing.TypeVar("V")
K = typing.TypeVar("K")


class AssertThat(typing.Generic[T]):
    """
    Base class for assertions of any type
    """

    def __init__(self, value: T) -> None:
        self.value = value
        self.with_trace = True

    def without_trace(self) -> typing.Self:
        self.with_trace = False
        return self

    def _check(self, condition: bool, fail_message: str) -> None:
        if not condition:
            pytest.fail(fail_message, self.with_trace)

    def is_not_none(self) -> typing.Self:
        self._check(self.value is not None, "Value is None")
        return self

    def is_none(self) -> typing.Self:
        self._check(self.value is None, "Value is not None")
        return self

    def is_equal_to(self, value: T) -> typing.Self:
        self._check(self.value == value, "Value is not equal to value")
        return self


class AssertThatEqualityMixin(AssertThat[T], typing.Generic[T]):
    """
    Mixin for equality assertions
    """

    def equals(self, value: T) -> None:
        self._check(self.value == value, fail_message="Equality check failed")


class AssertThatSequence(AssertThat, typing.Generic[T]):
    """
    Assertions for sequence types
    """

    def __init__(self, value: typing.Sequence[T]) -> None:
        super().__init__(value)

    def contains(self, v: T) -> typing.Self:
        """
        Verifies that the sequence contains the given value
        :param v: value to contain
        :return:
        """
        self._check(v in self.value, f"{self.value} does not contain {v}")
        return self

    def contains_only(self, *args: T) -> typing.Self:
        """
        Verifies that the sequence only contains the given values, ignoring duplicates.
        :param args: values to contain
        :return:
        """
        distinct_values = set(self.value)
        distinct_values_to_contain = set(args)
        self._check(
            len(distinct_values) == len(distinct_values_to_contain),
            f"Number of distinct values of {args} does not match with {self.value}",
        )
        for value in distinct_values_to_contain:
            self._check(
                value in distinct_values,
                f"{self.value} does not contain only {args}",
            )
        return self

    def contains_exactly(self, to_contain: typing.Sequence[T]) -> typing.Self:
        """
        Verifies that the sequence contains exactly the given values (in order).
        :param to_contain: values to contain exactly
        :return:
        """

        self._check(
            self.value == to_contain,
            f"{self.value} does not contain exactly {to_contain}",
        )
        return self

    def contains_exactly_in_any_order(
        self, to_contain: typing.Sequence[T]
    ) -> typing.Self:
        """
        Verifies that the sequence contains exactly the given values in any order.
        :param to_contain: values to contain exactly
        :return:
        """
        for value in to_contain:
            self._check(
                value in self.value,
                f"{self.value} does not contain {value}",
            )
        return self

    def contains_subsequence(self, subsequence: typing.Sequence[T]) -> typing.Self:
        """
        Verifies whether the sequence contains a subsequence of the given value.
        :param subsequence: sequence to contain
        :return:
        """
        length = len(subsequence)
        contains = False
        for i in range(len(self.value)):
            if self.value[i : i + length] == subsequence:
                contains = True
        self._check(contains, f"{self.value} does not contain {subsequence}")
        return self

    def contains_only_once(self, sub_sequence: typing.Sequence[T]) -> typing.Self:
        """
        Verifies that the sequence contains only once of every given values.
        :param sub_sequence:  values to contain only once
        :return:
        """

        found = [False] * len(sub_sequence)
        for i, value in enumerate(sub_sequence):
            for value_in_list in self.value:
                if value_in_list == value:
                    if found[i]:
                        self._check(
                            False, f"{self.value} contains {value} multiple times"
                        )
                    found[i] = True

        self._check(
            all(found), f"{self.value} does not contain all values {sub_sequence}"
        )
        return self

    def has_size(self, size: int) -> typing.Self:
        """
        Verifies that the sequence has size
        :param size: size of the sequence to verify
        :return:
        """
        self._check(len(self.value) == size, f"{self.value} has not size {size}")
        return self

    def first(
        self,
    ) -> "AssertThat[T]":  # This is not yet ideal, type hints will be not available for more complex elements
        """Extracts first element of the sequence"""
        return assert_that(self.value[0])

    def last(
        self,
    ) -> "AssertThat[T]":  # This is not yet ideal, type hints will be not available for more complex elements
        """Extracts last element of the sequence"""
        return assert_that(self.value[-1])

    def all_satisfy(self, consumer: typing.Callable[[T], typing.Any]) -> typing.Self:
        """
        Verify that all elements of the sequence are satisfying the given consumer
        :param consumer: assertions expressed via consumer
        :return:
        """

        for value in self.value:
            consumer(value)
        return self

    def any_satisfy(
        self, consumer: typing.Callable[[T], typing.Any]
    ) -> typing.Self:  # any as return is needed to support lambda functions
        """
        Verify that at least one element of the sequence are satisfying the given consumer
        :param consumer: assertions expressed via consumer
        :return:
        """
        any_satisfies_give_consumer = False
        for value in self.value:
            try:
                consumer(value)
                any_satisfies_give_consumer = True
                break
            except OutcomeException:
                pass
        self._check(
            any_satisfies_give_consumer, "No element satisfies the given assertions"
        )
        return self

    def none_satisfy(self, consumer: typing.Callable[[T], typing.Any]) -> typing.Self:
        """
        Verify that none of the elements of the sequence are satisfying the given consumer
        :param consumer: assertions expressed via consumer
        :return:
        """
        satisfies_given_consumer = False
        for value in self.value:
            try:
                consumer(value)
                satisfies_given_consumer = True
            except OutcomeException:
                pass
        self._check(
            not satisfies_given_consumer, "One element satisfies the given assertions"
        )
        return self

    def filtered_on(
        self, predicate: typing.Callable[[T], bool]
    ) -> "AssertThatSequence[T]":
        """
        Filter elements based on a given predicate
        :param predicate: function that returns whether element should stay in the sequence
        :return:
        """
        return assert_that([value for value in self.value if predicate(value)])

    def extracting(self, attribute: typing.Callable[[], V]) -> "AssertThatSequence[V]":
        """
        Extracting values from the given attribute of all elements in the sequence
        :param attribute: Method to extract attribute
        :return:
        """
        return AssertThatSequence(
            [getattr(v, attribute.__name__)() for v in self.value]
        )


class AssertThatList(AssertThatSequence[T]):
    """
    Assertions for lists
    """

    def __init__(self, value: typing.List[T]) -> None:
        super().__init__(value)


class AssertThatTuple(AssertThatSequence[T]):
    """
    Assertions for tuples
    """

    def __init__(self, value: typing.Tuple[T, ...]) -> None:
        super().__init__(value)


class AssertThatString(AssertThatSequence[str], AssertThatEqualityMixin[str]):
    """
    Assertions for strings
    """

    def __init__(self, value: str) -> None:
        super().__init__(value)

    def starts_with(self, value: str) -> typing.Self:
        self._check(
            self.value.startswith(value), f"{self.value} does not start with {value}"
        )
        return self

    def ends_with(self, value: str) -> typing.Self:
        self._check(
            self.value.endswith(value), f"{self.value} does not start with {value}"
        )
        return self


class AssertThatDict(
    AssertThatEqualityMixin[typing.Dict[K, V]],
    typing.Generic[K, V],
):
    """
    Assertions for dictionaries
    """

    def __init__(self, value: typing.Dict[K, V]) -> None:
        super().__init__(value)

    def contains_keys(self, keys: typing.List[K]) -> typing.Self:
        """
        Verify that the dictionary contains the keys
        :param keys: list of keys to contain
        :return:
        """
        for key in keys:
            self._check(
                self.value.get(key) is not None,
                f"{self.value} does not contain key {key}",
            )
        return self

    def does_not_contain_keys(self, keys: typing.List[K]) -> typing.Self:
        """
        Verify that the dictionary does not contain the keys
        :param keys: list of keys to contain
        :return:
        """
        for key in keys:
            self._check(
                self.value.get(key) is None,
                f"{self.value} does contain key {key}",
            )
        return self

    def contains_values(self, values: typing.List[V]) -> typing.Self:
        """
        Verify that the dictionary contains the values
        :param values: list of values to contain
        :return:
        """
        dictionary_values = set(self.value.values())
        for value in values:
            self._check(
                value in dictionary_values,
                f"{self.value} does not contain value {value}",
            )
        return self

    def is_empty(self) -> typing.Self:
        """
        Verify that the dictionary is empty
        :return:
        """
        self._check(len(self.value) == 0, f"{self.value} is not empty")
        return self

    def is_not_empty(self) -> typing.Self:
        """
        Verify that the dictionary is not empty
        :return:
        """
        self._check(len(self.value) != 0, f"{self.value} is empty")
        return self

    def extracting(self, key: K) -> AssertThat[V | None]:
        """
        Extracts values from the given key and returns assert that
        :param key:
        :return:
        """
        return assert_that(self.value.get(key))


@typing.overload
def assert_that(value: typing.List[T]) -> AssertThatList[T]: ...


@typing.overload
def assert_that(value: typing.Tuple[T, ...]) -> AssertThatTuple[T]: ...


@typing.overload
def assert_that(value: str) -> AssertThatString: ...


@typing.overload
def assert_that(value: typing.Dict[K, V]) -> AssertThatDict[K, V]: ...


@typing.overload
def assert_that(value: T) -> AssertThat[T]: ...


def assert_that(value: typing.Any) -> AssertThat:
    """
    Fluent api for assertions in pytest
    :param value: Value to verify
    :return:
    """
    match value:
        case list():
            return AssertThatList(value)
        case tuple():
            return AssertThatTuple(value)
        case str():
            return AssertThatString(value)
        case dict():
            return AssertThatDict(value)
        case _:
            return AssertThat(value)
