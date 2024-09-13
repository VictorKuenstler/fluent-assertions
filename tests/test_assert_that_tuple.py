import pytest
from _pytest.outcomes import OutcomeException

from src.fluent_assertions import assert_that


class TestAssertThatTuple:
    def test_assert_contains(self):
        assert_that((1, 2, 3)).contains(3)

    def test_assert_not_contains_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains(4)

    def test_assert_contains_only(self):
        assert_that((1, 2, 3)).contains_only(1, 2, 3)

        assert_that((1, 2, 3)).contains_only(1, 2, 3, 1)

    def test_assert_contains_only_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_only(1, 2, 3, 4)

        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_only(1, 2)

    def test_assert_contains_exactly(self):
        assert_that((1, 2, 3)).contains_exactly((1, 2, 3))

    def test_assert_contains_exactly_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_exactly((1, 2))

        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_exactly((1, 2, 3, 4))

    def test_assert_has_size(self):
        assert_that((1, 2, 3)).has_size(3)

    def test_assert_has_size_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).has_size(2)

        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).has_size(4)

    def test_assert_contains_subsequence(self):
        assert_that((1, 2, 3)).contains_subsequence((1, 2))
        assert_that((1, 2, 3)).contains_subsequence((2, 3))
        assert_that((1, 2, 3, 4, 5, 6)).contains_subsequence((3, 4, 5))

    def test_assert_contains_subsequence_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_subsequence((1, 3))

        with pytest.raises(OutcomeException):
            assert_that((1, 2, 3)).contains_subsequence((2, 1))

    def test_assert_contains_only_once(self):
        assert_that((1, 2, 3)).contains_only_once((1, 2))
        assert_that((1, 2, 3)).contains_only_once((3,))
        assert_that((1, 3, 2, 3)).contains_only_once((2, 1))

    def test_assert_contains_only_once_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that((1, 1, 2, 3)).contains_only_once((1, 3))

        with pytest.raises(OutcomeException):
            assert_that((1, 3, 2, 3)).contains_only_once((2, 3))
