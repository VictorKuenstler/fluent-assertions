import pytest
from _pytest.outcomes import OutcomeException

from src.fluent_assertions import assert_that


class TestAssertThatDict:
    def test_contains_keys(self):
        assert_that({"test-1": "value-1", "test-2": "value-2"}).contains_keys(
            ["test-1"]
        )

    def test_contains_keys_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that({"test-1": "value-1", "test-2": "value-2"}).contains_keys(
                ["test-4"]
            )

    def test_contains_values(self):
        assert_that({"test-1": "value-1", "test-2": "value-2"}).contains_values(
            ["value-2"]
        )

    def test_contains_values_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that({"test-1": "value-1", "test-2": "value-2"}).contains_values(
                ["value-3"]
            )

    def test_is_empty(self):
        assert_that({}).is_empty()

    def test_is_not_empty(self):
        with pytest.raises(OutcomeException):
            assert_that({"value": ""}).is_empty()

    def test_extracting(self):
        assert_that({"test-1": "value-1", "test-2": "value-2"}).extracting(
            "test-1"
        ).is_not_none()

    def test_does_not_contain_keys(self):
        assert_that({"test-1": "value-1", "test-2": "value-2"}).does_not_contain_keys(
            ["test-3"]
        )

    def test_does_not_contain_keys_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(
                {"test-1": "value-1", "test-2": "value-2"}
            ).does_not_contain_keys(["test-1"])
