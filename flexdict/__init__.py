"""
Easily work with deeply nested data and write
clean code using FlexDict; a small subclass of
dict. FlexDict provides automatic and arbitrary
levels of nesting along with additional utility
methods.
"""

__version__ = '0.0.1.a1'


class FlexDict(dict):
    """
    Provides automatic and arbitrary levels of
    nesting along with additional utility methods.

    Args:
        data (dict): Data to initialize the FlexDict with.

    Attributes:
        locked (bool): Flag indicating if auto-nesting is locked.
    """

    def __init__(self, data=None):
        super(FlexDict, self).__init__()
        self.locked = False
        if data:
            if isinstance(data, dict):
                for items in self.__kv(data):
                    self.__setitem__(*items)
            else:
                raise ValueError(
                    'FlexDict can only be initialized with instances of dict!'
                )

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.flatten() == FlexDict(other).flatten()
        return False

    def __getitem__(self, key):
        key = self.__sanitize(key)
        if isinstance(key, list):
            for _, k in enumerate(key, start=1):
                self = self[k]
            return self
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if not self.locked:
                return self.setdefault(key, FlexDict())
            raise

    def __setitem__(self, key, val):
        key = self.__sanitize(key)
        if isinstance(key, list):
            for i, k in enumerate(key[:-1], start=1):
                if not self.locked or k in self:
                    self = self[k]
                else:
                    if i == len(key) - 1:
                        raise KeyError(k)
            self[key[-1]] = val
        else:
            dict.__setitem__(
                self, key, FlexDict(val) if isinstance(val, dict) else val
            )

    @staticmethod
    def __sanitize(key):
        if isinstance(key, (list, set, tuple)):
            return list(key)
        if isinstance(key, dict):
            raise TypeError('unhashable type: \'dict\'')
        return key

    def __kv(self, data, results=None):
        if results is None:
            results = []
        for key, value in data.items():
            if isinstance(value, dict) and value:
                for item in self.__kv(value, results + [key]):
                    yield item
            else:
                yield results + [key], value

    def __k(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                yield key
                for nested_key in self.__k(value):
                    yield nested_key
            else:
                yield key

    def __v(self, data):
        for _, value in data.items():
            if isinstance(value, dict) and value:
                for nested_value in self.__v(value):
                    yield nested_value
            else:
                yield value

    def __lock(self, lock, inplace, data=None):
        if not data:
            data = self if inplace else FlexDict(self)
        data.locked = lock
        for key, val in data.items():
            if isinstance(val, FlexDict):
                data[key].locked = lock
                self.__lock(lock, inplace, data[key])
        return None if inplace else data

    def __contains(self, superset, subset, dicts):
        if superset == subset:
            return True
        if dicts:
            superset = {
                key: value
                for sub_dict in dicts
                for key, value in sub_dict.items()
            }
            dicts = []
        for sub_key, sub_val in subset.items():
            for sup_key, sup_value in superset.items():
                if {sup_key: sup_value} == {sub_key: sub_val}:
                    return True
                if isinstance(sup_value, dict):
                    if sup_value == subset:
                        return True
                    dicts.append(sup_value)
            if dicts:
                return self.__contains(superset, subset, dicts)
        return False

    def get(self, keys, default=None):
        """
        Gets a value from the dictionary with the provided keys.

        Args:
            keys: Keys pointing to the target value.
            default (any): Default value to return if target does not exists.

        Returns:
            any: The corresponding dictionary value.
        """
        keys = self.__sanitize(keys)
        if isinstance(keys, list):
            for key in keys:
                if key in self:
                    self = self[key]
                else:
                    return default
            return self
        if keys in self:
            return self[keys]
        return default

    def set(self, keys, value, overwrite=True, increment=False):
        """
        Sets a dictionary value with the given keys.

        Args:
            keys (any): Key(s) pointing to the value.
            value (any): Value to set.
            overwrite (bool): If `False`, only sets a value if it not exists.
            increment (bool):
                Increments the value by `value` if set to `True`.
                `overwrite` argument has no effect on this.
                Causes the method to return the target value.

        Returns:
            Union[int, float, None]:
                Final state of the target value if `increment` is enabled.
        """
        keys = self.__sanitize(keys)
        if not increment:
            if overwrite or keys[-1] in self.get(keys[:-1], default=[]):
                self[keys] = value
            return None
        self[keys] = value if (
            not self[keys]
        ) else self[keys] + value
        return self[keys]

    def keys(self, nested=False, unique=False):
        """
        Gets keys from the dictionary.

        Args:
            nested (bool): Gets all keys recursively if set to `True`.
            unique (bool): Gets only the unique keys if set to `True`.

        Returns:
            Union[dict_keys, list, set]:
                dict_keys
                    If `nested` is `False` and `unique` is `False`.
                list
                    If `nested` is `True` and `unique` is `False`.
                set
                    If `unique` is `True`.
        """
        return dict.keys(self) if not nested else (
            list(self.__k(self)) if not unique else set(self.__k(self))
        )

    def values(self, nested=False, unique=False):
        """
        Gets values from the dictionary.

        Args:
            nested (bool): Gets all values recursively if set to `True`.
            unique (bool): Gets only the unique values if set to `True`.

        Returns:
            Union[dict_values list, set]:
                dict_values
                    If `nested` is `False` and `unique` is `False`.
                list:
                    If `nested` is `True` and `unique` is `False`.
                list:
                    If `unique` is `True`.
        """
        vals = (
            list(dict.values(self))
            if not nested
            else list(self.__v(self))
        )
        return (
            vals
            if not unique
            else list(set(vals))
            if not nested
            else set(vals)
        )

    def pop(self):
        """
        Removes and returns the last key-value pair from the dictionary.

        Returns:
            Union[FlexDict, None]:
                FlexDict
                    The last key-value pair of the dictionary.
                None
                    If `self` is empty.
        """
        if self:
            key, val = list(self.items())[-1]
            del self[key]
            return FlexDict({key: val})
        return None

    def length(self, nested=False, unique=False):
        """
        Counts the number of keys inside the dictionary.

        Args:
            nested (bool): Counts all keys recursively if set to `True`.
            unique (bool): Counts only the unique keys if set to `True`.

        Returns:
            int: Number of keys.
        """
        return len(self.keys(nested=nested, unique=unique))

    def size(self, unique=False):
        """
        Counts the number of keys and values inside the dictionary.

        Args:
            nested (bool): Counts all items recursively if set to `True`.
            unique (bool): Counts only the unique items if set to `True`.

        Returns:
            int: Number of items.
        """
        return len(self.keys(nested=True, unique=unique)) + len(
            self.values(nested=True, unique=unique)
        )

    def flatten(self):
        """
        Flattens the dictionary.

        Returns:
            list: A list of tuples containing key-paths and values.
        """
        return list(self.__kv(self))

    def lock(self, inplace=True):
        """
        Locks the automatic nesting mechanism.

        Args:
            inplace (bool): Creates a locked copy if `True`.

        Returns:
            Union[None, FlexDict]:
                None
                    If `inplace` is set to `True`.
                FlexDict
                    If `inplace`set to `False`.
        """
        return self.__lock(True, inplace)

    def unlock(self, inplace=True):
        """
        Unlocks the automatic nesting mechanism.

        Args:
            inplace (bool): Creates an unlocked copy if `True`.

        Returns:
            Union[None, FlexDict]:
                None
                    If `inplace` is set to `True`.
                FlexDict
                    If `inplace`set to `False`.
        """
        return self.__lock(False, inplace)

    def contains(self, subset):
        """
        Checks if this dictionary is a superset of a given one.

        Args:
            subset (dict): Dictionary to check if it is a subset.

        Returns:
            bool: `True` if `self` contains `subset` else `False`.
        """
        return self.__contains(self, subset, [])

    def inside(self, superset):
        """
        Checks if this dictionary is a subset of a given one.

        Args:
            superset (dict): Dictionary to check if it is a superset.

        Returns:
            bool: `True` if `self` is inside the `superset` else `False`.
        """
        return self.__contains(superset, self, [])
