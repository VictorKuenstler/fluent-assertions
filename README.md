# fluent-assertions for Pytest

This project aims to provide a **fluent API** for assertions supporting **pytest**, designed with simplicity and ease of use in mind. 

The core idea is to make writing assertions more intuitive, readable, and enjoyable by offering a fluent interface that leverages the power of modern Python **typing**. It aims to be easy to use in any IDE for enhanced developer productivity.


*⚠️ Current Status This project is in its early exploratory phase. While the core functionality is present, it is not yet fully mature. Use with caution as the API may evolve rapidly and changes could be breaking.*


## 🎯 Features

- Fluent API for pytest assertions.
- Full typing support for IDE-friendly development.
- Designed to improve readability and expressiveness of test cases.

## 🛠️ Examples

Classes:
```python
from fluent_assertions import assert_that

def test_class(): 
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

```

Dictionaries:
```python
def test_dict():
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
```

Lists:
```python  
def test_list():
    (
        assert_that([1, 2, 3])
        .contains_only(1, 2, 3)
        .has_size(3)
        .contains_subsequence([2, 3])
    )

```

## 📦 Installation

Available on PyPi:

```bash
pip install fluent-assertions
```

## 🤝 Contributing

Feedback and collaboration are highly encouraged! If you encounter bugs, have feature requests, or want to contribute improvements, feel free to open an issue or submit a pull request.

## 🚧 Roadmap

- Add more assertion types and methods.
- Improve documentation and add examples.


## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.


