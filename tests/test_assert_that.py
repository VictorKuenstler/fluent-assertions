import dataclasses

import pytest
from _pytest.outcomes import OutcomeException

from src.fluent_assertions import assert_that


class TestAssertThat:
    def test_assert_not_none(self):
        assert_that("").is_not_none()

    def test_assert_not_none_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that(None).is_not_none()

    def test_assert_is_none(self):
        assert_that(None).is_none()

    def test_assert_is_none_should_fail(self):
        with pytest.raises(OutcomeException):
            assert_that("None").is_none()

    def test_assert_end_to_end(self):
        @dataclasses.dataclass
        class User:
            name: str
            age: int

            def get_name(self):
                return self.name

        list_of_users = [User(name="Guenther", age=51), User(name="Jack", age=12)]
        (
            assert_that(list_of_users)
            .has_size(2)
            .extracting(User.get_name)
            .contains_exactly(["Guenther", "Jack"])
            .last()
            .is_equal_to("Jack")
        )

        example_dict = {
            "name": "Guenther",
            "age": "51",
        }

        (
            assert_that(example_dict)
            .is_not_empty()
            .contains_keys(["name", "age"])
            .contains_values(["Guenther", "51"])
        )

        (
            assert_that([1, 2, 3])
            .contains_only(1, 2, 3)
            .has_size(3)
            .contains_subsequence([2, 3])
        )
