import pytest
from _pytest.outcomes import OutcomeException

from src.fluent_assertions import assert_that


class TestAssertThatString:
    def test_assert_contains(self):
        assert_that("fake string with some content").contains("some content")

    def test_assert_startswith(self):
        assert_that("fake string with some content").starts_with("fake string")

    def test_assert_startswith_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that("fake string with some content").starts_with("some content")

    def test_assert_endswith(self):
        assert_that("fake string with some content").ends_with(" content")

    def test_assert_endswith_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that("fake string with some content").ends_with("some")
