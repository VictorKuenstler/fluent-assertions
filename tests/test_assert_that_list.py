import dataclasses

import pytest
from _pytest.outcomes import OutcomeException

from src.fluent_assertions import assert_that


@dataclasses.dataclass
class FakeClass:
    name: str
    value: str

    def get_name(self):
        return self.name


class TestAssertThatList:
    def test_assert_contains(self):
        assert_that([1, 2, 3]).contains(3)
        assert_that(
            [{"name": "fake-name-1"}, {"name": "fake-name-2"}, {"name": "fake-name-3"}]
        ).contains({"name": "fake-name-2"})

    def test_assert_not_contains_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains(4)
            assert_that(
                [
                    {"name": "fake-name-1"},
                    {"name": "fake-name-2"},
                    {"name": "fake-name-3"},
                ]
            ).contains({"name": "fake-name-4"})

    def test_assert_contains_only(self):
        assert_that([1, 2, 3]).contains_only(1, 2, 3)
        assert_that([1, 2, 3]).contains_only(1, 2, 3, 1)

    def test_assert_contains_only_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_only(1, 2, 3, 4)

        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_only(1, 2)

    def test_assert_contains_exactly(self):
        assert_that([1, 2, 3]).contains_exactly([1, 2, 3])

    def test_assert_contains_exactly_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_exactly([1, 2])

        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_exactly([1, 2, 3, 4])

    def test_assert_has_size(self):
        assert_that([1, 2, 3]).has_size(3)

    def test_assert_has_size_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).has_size(2)

        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).has_size(4)

    def test_assert_contains_subsequence(self):
        assert_that([1, 2, 3]).contains_subsequence([1, 2])
        assert_that([1, 2, 3]).contains_subsequence([2, 3])
        assert_that([1, 2, 3, 4, 5, 6]).contains_subsequence([3, 4, 5])

    def test_assert_contains_subsequence_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_subsequence([1, 3])

        with pytest.raises(OutcomeException):
            assert_that([1, 2, 3]).contains_subsequence([2, 1])

    def test_assert_contains_only_once(self):
        assert_that([1, 2, 3]).contains_only_once([1, 2])
        assert_that([1, 2, 3]).contains_only_once([3])
        assert_that([1, 3, 2, 3]).contains_only_once([2, 1])

    def test_assert_contains_only_once_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that([1, 1, 2, 3]).contains_only_once([1, 3])

        with pytest.raises(OutcomeException):
            assert_that([1, 3, 2, 3]).contains_only_once([2, 3])

    def test_assert_all_satisfy(self):
        assert_that(
            [
                FakeClass(name="fake-name-1", value="fake value 1"),
                FakeClass(name="fake-name-2", value="fake value 2"),
            ]
        ).all_satisfy(lambda x: assert_that(x.name).contains("fake-name"))

    def test_assert_all_satisfy_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                [
                    FakeClass(name="fake-name-1", value="fake value 1"),
                    FakeClass(name="fake-name-2", value="fake value 2"),
                ]
            ).all_satisfy(lambda x: assert_that(x.name).equals("fake-name"))

    def test_assert_any_satisfy(self):
        assert_that(
            [
                FakeClass(name="fake-name-1", value="fake value 1"),
                FakeClass(name="fake-name-2", value="fake value 2"),
            ]
        ).any_satisfy(lambda x: assert_that(x.name).equals("fake-name-1"))

    def test_assert_any_satisfy_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                [
                    FakeClass(name="fake-name-1", value="fake value 1"),
                    FakeClass(name="fake-name-2", value="fake value 2"),
                ]
            ).any_satisfy(lambda x: assert_that(x.name).contains("fake-name-23"))

    def test_assert_none_satisfy(self):
        assert_that(
            [
                FakeClass(name="fake-name-1", value="fake value 1"),
                FakeClass(name="fake-name-2", value="fake value 2"),
            ]
        ).none_satisfy(lambda x: assert_that(x.name).equals("fake-name-23"))

    def test_assert_none_satisfy_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                [
                    FakeClass(name="fake-name-1", value="fake value 1"),
                    FakeClass(name="fake-name-2", value="fake value 2"),
                ]
            ).none_satisfy(lambda x: assert_that(x.name).contains("fake-name-1"))

    def test_assert_filter(self):
        assert_that(
            [
                FakeClass(name="fake-name-1", value="fake value 1"),
                FakeClass(name="fake-name-2", value="fake value 2"),
            ]
        ).filtered_on(lambda x: x.name == "fake-name-1").has_size(1)

    def test_assert_filter_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                [
                    FakeClass(name="fake-name-1", value="fake value 1"),
                    FakeClass(name="fake-name-2", value="fake value 2"),
                ]
            ).filtered_on(lambda x: x.name == "fake-name-0").has_size(1)

    def test_assert_extracting(self):
        assert_that(
            [
                FakeClass(name="fake-name-1", value="fake value 1"),
                FakeClass(name="fake-name-2", value="fake value 2"),
            ]
        ).extracting(FakeClass.get_name).first().is_equal_to("fake-name-1")

    def test_assert_extracting_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                [
                    FakeClass(name="fake-name-1", value="fake value 1"),
                    FakeClass(name="fake-name-2", value="fake value 2"),
                ]
            ).extracting(FakeClass.get_name).first().is_equal_to("fake-name-2")
