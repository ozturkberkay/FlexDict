![FlexDict Logo](docs/source/_static/logo.png)
# FlexDict
![Travis (.org)](https://img.shields.io/travis/ozturkberkay/FlexDict?style=flat-square) ![Codacy coverage](https://img.shields.io/codacy/coverage/66f007ce4acf4076802667c726e89753?style=flat-square) ![Codacy grade](https://img.shields.io/codacy/grade/66f007ce4acf4076802667c726e89753?style=flat-square) ![GitHub repo size](https://img.shields.io/github/repo-size/ozturkberkay/FlexDict?style=flat-square) ![PyPI](https://img.shields.io/pypi/v/flexdict?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flexdict?style=flat-square) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg?style=flat-square)](https://github.com/PyCQA/bandit)


> Elegantly nested Python dictionaries.

Easily work with deeply nested dictionaries **and** write clean code using FlexDict; a *small* subclass of ``dict``. FlexDict provides automatic and arbitrary levels of nesting along with additional utility functions.

## Getting Started

1) Install
    ```console
    pip install flexdict
    ```

2) Import
    ```python
    from flexdict import FlexDict
    ```

3) Create
    ```python
    f = FlexDict()
    ```

## User's Guide

The main purpose of `FlexDict` is to allow you to work with deeply nested dictionaries with minimal amount of code. It achieves this purpose by providing an automatic nesting algorithm. It can be a dangerous feature if not used with caution. That's why, `FlexDict` provides some helper methods to prevent any unintentional side-effects.

### Setting Items

When it comes to setting dictionary items, `FlexDict` provides many options. Let's start with the most *slick* way:

```python
f = FlexDict()

f['easily', 'create', 'deeply', 'nested', 'structures'] = 1
```

The resulting dictionary would be:

```terminal
{'easily':{'create':{'deeply':{'nested':{'structures': 1}}}}
```

You can directly pass instances of `list`, `tuple` or `set` instead:

```python
f[['easily', 'create', 'deeply', 'nested', 'structures']]
f[('easily', 'create', 'deeply', 'nested', 'structures')]
f[{'easily', 'create', 'deeply', 'nested', 'structures'}]
```

You also have other options:

```python
f['easily']['create']['deeply']['nested']['structures'] = 1

f.set(['easily', 'create', 'deeply', 'nested', 'structures'], 1)
f.set(('easily', 'create', 'deeply', 'nested', 'structures'), 1)
f.set({'easily', 'create', 'deeply', 'nested', 'structures'}, 1)
```

The resulting dictionary would be the same for all these examples. However, the `set` method provides many other features. For example, you may only want to set the dictionary items if they do not already exist:

```python
f = FlexDict({'a': {'b':1}})

f.set(['a', 'b'], 2, overwrite=False)
f.set(['a', 'c'], 2, overwrite=False)
```

This prevents you to overwrite existing values:

```terminal
{'a': {'b': 1, 'c': 2}}
```

Or, if you need a counter, you can use the `increment` argument to do exactly that:

```python
f = FlexDict()

for i in range(20):
    if i % 2 == 0:
        f.set('Even', 1, increment=True)
    else:
        f.set('Odd', 1, increment=True)

f
```

Output:
```terminal
{'Even': 10, 'Odd': 10}
```

(Note that `overwrite` argument has no effect when `increment` is enabled.)

## Getting Items

Again, `FlexDict` provides many alternative ways to access your dictionary items:

```python
f = FlexDict({'key1': {'key2': {'key3': 1}}})

# 1
f['key1', 'key2', 'key3']

# 2
f['key1']['key2']['key3']

# 3
f.get(['key1', 'key2', 'key3'])
f.get(('key1', 'key2', 'key3'))
f.get({'key1', 'key2', 'key3'})
```

They will all return the same result:

```terminal
1
```

There is a crucial distinction between these alternatives. Whenever you use squared brackets to access an item, `FlexDict` **will automatically create the keys and fill the value with an empty** `FlexDict` **if there is no such item**:

```python
f = FlexDict()

f['a', 'b']

f
```

Output:
```terminal
{'a': {'b': {}}}
```

To prevent this side-effect, `FlexDict` provides two options. First one, is the `get` method:

```python
f = FlexDict()

f.get(['a', 'b']), f.get(['a', 'b'], default=0), f
```

The `get` method returns the value provided with the `default` argument if the target item does not exist:

```terminal
(None, 0, {})
```

The other option to avoid the aformentioned side-effect is to use the recursive locking mechnasim via the `lock` method. We will cover it later in this guide. However, just to give you a taste of it, the following example is added:

```python
f = FlexDict()

f.lock()

f['a', 'b']
```

Output:
```terminal
KeyError: 'a'
```

Getting the top level keys and values works just like a regular `dict`:

```python
f = FlexDict({'a': 1, 'b': 2})

f.keys(), f.values()
```

The only difference you would notice is `f.values()` returns a `list` instead of `dict_values`. This is an intentional behavior since we are working with nested dictionaries:

```terminal
(dict_keys(['a', 'b']), [1, 2])
```

You may also want to get every key and/or value inside your `FlexDict` instance, even the nested ones. `FlexDict` can do this with recursion:

```python
f = FlexDict({
    'a': {
        'b': 1,
        'c': {
            'd': 1,
            'e': {
                'a': 3
            }
        }
    },
    'g': 4
})

f.keys(nested=True), f.values(nested=True)
```

This allows you to check exactly what is inside your `FlexDict` instance:

```terminal
(['a', 'b', 'c', 'd', 'e', 'a', 'g'], [1, 1, 3, 4])
```

You can even get rid of the duplicates:

```python
f.keys(nested=True, unique=True), f.values(nested=True, unique=True)
```

Note that unique items gets returned inside of a `set`:

```terminal
({'a', 'b', 'c', 'd', 'e', 'g'}, {1, 3, 4})
```

If you wish, you can flatten the entire `FlexDict` instance. The `flatten` method returns a `list` of values and their respective key-paths:

```python
f.flatten()
```

Output:
```
[(['a', 'b'], 1), (['a', 'c', 'd'], 1), (['a', 'c', 'e', 'a'], 3), (['g'], 4)]
```

Last but not least, if you wish to get the last item and remove it from the `FlexDict` instance, you can use the `pop` method:

```python
f = FlexDict({'a': 1, 'b': 2})

f.pop(), f
```

Output:
```python
({'b': 2}, {'a': 1})
```

### Locking & Unlocking Automatic Nesting

Like we discussed above, automatic nesting can be very dangerous in some cases. Thats why, aside from the previously mentioned workarounds, `FlexDict` provides a recursive algorithm to lock and unlock this feature:

```python
f = FlexDict()

f.lock()

f['a'] = 1  # Normal `dict` behavior works as expected

try:
    f['b', 'c'] = 1 # Will throw a KeyError
except KeyError:
    f.unlock()
    f['b', 'c'] = 1

f
```

Output:
```terminal
{'a': 1, 'b': {'c': 1}}
```

Each `FlexDict` instance has an attribute called `locked` which tells if it is locked. **Each nested dictionary inside a** `FlexDict` **instance is also a seperate** `FlexDict` **instance!** This means, each of them has seperate `locked` attributes. The `lock` method sets the `locked` attribute of the specified `FlexDict` instance and of all the other nested dictionaries inside of it to `True`. `unlock` method on the other hand, does the exact opposite. This means that you can create any hybrid lock structure you want (Do that with caution!):

```python
f = FlexDict({'secure': {}, 'not_secure': {}})

f['secure'].lock()

f.locked, f['secure'].locked, f['not_secure'].locked
```

Output:
```terminal
(False, True, False)
```

Both `lock` and `unlock` methods provide an argument called `inplace` which allows you to create locked/unlocked copies of your `FlexDict` instances:

```python
f = FlexDict()

f_locked = f.lock(inplace=False)

f.locked, f_locked.locked
```

Output:
```terminal
(False, True)
```

### Other Utility Methods

You can check if your `FlexDict` instance contains (is a superset of) or inside of (is a subset of) another `dict` instance.

```python
f = FlexDict({'a': {'b': 1}})

f.contains({'b': 1}), f.inside({'c': {'a': {'b': 1}}})
```

Output:
```terminal
(True, True)
```

`FlexDict` also allows you to easily get the length (number of keys) and size (number of keys and values) inside your dictionaries via `length` and `size` methods. They both utilize the previously mentioned `keys` and `values` methods. Hence, they can work recursively and get rid of duplicates if you wish:

```python
f = FlexDict({
    'a': {
        'b': 1,
        'c': {
            'd': 1,
            'e': {
                'a': 3
            }
        }
    },
    'g': 4
})

# Can be used as a replacement for len()
print(f'Number of keys:', f.length())
print(f'Number of keys (Recursive):', f.length(nested=True))
print(f'Number of keys (Recursive, Unique):', f.length(nested=True, unique=True))

# Saves some of your time
print(f'\nNumber of items (Recursive):', f.size())
print(f'Number of items (Recursive, Unique):', f.size(unique=True))
```

Output:
```terminal
Number of keys: 2
Number of keys (Recursive): 7
Number of keys (Recursive, Unique): 6

Number of items (Recursive): 11
Number of items (Recursive, Unique): 9
```

## Contributing
See [contributing](https://github.com/ozturkberkay/FlexDict/CONTRIBUTING.md) for the details.