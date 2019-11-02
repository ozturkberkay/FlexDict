"""Unit tests for FlexDict."""

from pytest import mark, raises
from flexdict import FlexDict

DATA = {'a': {'b': {'c': 1, 'd': 2}}, 'e': {'f': 3, 'g': 4}, 'h': 5}


def test_init():
    """Initialization with dictionary."""
    assert FlexDict() == dict()
    assert FlexDict(DATA) == DATA


def test_init_value_error():
    """Invalid initialization."""
    data = {1, 2}
    with raises(ValueError):
        FlexDict(data)


@mark.parametrize(
    'keys', [
        ['a'],
        ['a', 'b'],
        ['a', 'c'],
        ['d'],
        ['d', 'e'],
        ['d', 'f'],
        ['g'],
    ]
)
def test_init_lock(keys):
    """Recursive locking on init."""
    flex = FlexDict(DATA)
    assert flex.locked is False
    assert flex[keys].locked is False


def test_equals():
    """Equality comparisons."""
    flex = FlexDict()
    assert (flex == flex) is True
    assert (flex is flex) is True
    assert (flex == FlexDict()) is True
    assert (flex is FlexDict()) is False


@mark.parametrize(
    'keys', [
        ['a'],
        ['a', 'b'],
        ['e']
    ]
)
def test_lock(keys):
    """Recursive locking mechanism."""
    flex = FlexDict(DATA)
    flex.lock()
    assert flex.locked is True
    assert flex[keys].locked is True


def test_lock_inplace_false():
    """Creating a locked and unlocked copies."""
    flex = FlexDict(DATA)
    flex_locked = flex.lock(inplace=False)
    flex_unlocked = flex_locked.unlock(inplace=False)
    assert flex.locked is False
    assert flex_locked.locked is True
    assert flex_unlocked.locked is False


def test_lock_error():
    """KeyError after locking."""
    flex = FlexDict(DATA)
    flex.lock()
    with raises(KeyError):
        flex['z', 'k']  # pylint: disable=W0104
    with raises(KeyError):
        flex['z', 'k'] = 1
    assert flex == DATA


@mark.parametrize(
    'keys', [
        ['a'],
        ['a', 'b'],
        ['a', 'c'],
        ['d'],
        ['d', 'e'],
        ['d', 'f'],
        ['g'],
        ['z']
    ]
)
def test_unlock(keys):
    """Recursive (un)locking mechanism."""
    flex = FlexDict(DATA)
    flex.lock()
    flex.unlock()
    assert flex.locked is False
    assert flex[keys].locked is False


def test_unlock_set():
    """Set values after unlocking."""
    flex = FlexDict(DATA)
    flex.lock()
    flex.unlock()
    flex['z', 'k'] = 1


def test_get_func_default():
    """Getting default values for non-existing items."""
    flex = FlexDict()
    assert flex.get('j', default=0) == 0
    assert flex.get(['j', 'k'], default=0) == 0


def test_set_func_increment():
    """Setting values."""
    flex = FlexDict()
    for i in range(5):
        flex.set(['b', 'c', 'd'], i, increment=True)
    assert flex['b', 'c', 'd'] == 10


def test_set_func_overwrite_false():
    """Setting values without overwriting existing ones."""
    flex = FlexDict(DATA)
    res = flex.set('a', 0, overwrite=False)
    assert flex['a'] == DATA['a']
    assert res is None


def test_set_func_value_error():
    """Invalid argument for set()."""
    flex = FlexDict()
    with raises(TypeError):
        flex.set({'a': 1}, 1)


def test_keys():
    """Getting keys."""
    flex = FlexDict(DATA)
    assert flex.keys() == DATA.keys()


def test_keys_unique():
    """Getting unique keys."""
    flex = FlexDict(DATA)
    assert sorted(flex.keys(unique=True)) == sorted(set(DATA.keys()))


def test_keys_nested():
    """Getting nested keys."""
    flex = FlexDict(DATA)
    assert sorted(flex.keys(nested=True)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
    ]


def test_keys_nested_unique():
    """Getting nested unique keys."""
    flex = FlexDict(DATA)
    assert flex.keys(nested=True, unique=True) == {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
    }


def test_values():
    """Getting values."""
    flex = FlexDict(DATA)
    assert list(flex.values()) == list(DATA.values())


def test_values_unique():
    """Getting unique values."""
    flex = FlexDict(DATA)
    assert all([item in [
        {'b': {'c': 1, 'd': 2}}, {'f': 3, 'g': 4}, 5
    ] for item in flex.values(unique=True)]) is True


def test_values_nested():
    """Getting nested values."""
    flex = FlexDict(DATA)
    assert sorted(flex.values(nested=True)) == [
        1, 2, 3, 4, 5
    ]


def test_values_nested_unique():
    """Getting nested unique values."""
    flex = FlexDict(DATA)
    assert flex.values(nested=True, unique=True) == {1, 2, 3, 4, 5}


def test_flatten():
    """Flatenning the dictionary."""
    flex = FlexDict(DATA)
    assert sorted(flex.flatten()) == [
        (['a', 'b', 'c'], 1),
        (['a', 'b', 'd'], 2),
        (['e', 'f'], 3),
        (['e', 'g'], 4),
        (['h'], 5)
    ]


def test_len():
    """Getting the dictionary length."""
    flex = FlexDict(DATA)
    assert len(flex) == 3


def test_length():
    """Getting the dictionary length."""
    flex = FlexDict(DATA)
    assert flex.length() == 3


def test_length_unique():
    """Getting the number of keys."""
    flex = FlexDict(DATA)
    assert flex.length(unique=True) == 3


def test_length_nested():
    """Recursively getting the total number of keys."""
    flex = FlexDict(DATA)
    assert flex.length(nested=True) == 8


def test_length_nested_unique():
    """Recursively getting the total number of unique keys."""
    flex = FlexDict(DATA)
    assert flex.length(nested=True, unique=True) == 8


def test_size():
    """Recursively count the total number of keys and values."""
    flex = FlexDict(DATA)
    assert flex.size() == 13


def test_size_unique():
    """Recursively count the total number of unique keys and values."""
    flex = FlexDict(DATA)
    assert flex.size(unique=True) == 13


def test_pop():
    """Popping items from the dictionary."""
    flex = FlexDict(DATA)
    items = list(flex.items())[::-1]
    for key, val in items:
        assert flex.pop() == {key: val}
    assert flex.pop() is None


@mark.parametrize('get_keys, get_val', [
    (['a'], DATA['a']),
    (['a', 'b'], DATA['a']['b']),
    (['a', 'b', 'c'], DATA['a']['b']['c']),
    (['a', 'b', 'd'], DATA['a']['b']['d']),
    (['e'], DATA['e']),
    (['e', 'f'], DATA['e']['f']),
    (['e', 'g'], DATA['e']['g']),
    (['h'], DATA['h']),
    ('a', DATA['a'])
])
class TestFlexDictGet:
    """Unit tests for getting items."""

    @staticmethod
    def test_get(get_keys, get_val):
        """Getting values."""
        flex = FlexDict(DATA)
        assert flex[get_keys] == get_val

    @staticmethod
    def test_get_function(get_keys, get_val):
        """Getting value."""
        flex = FlexDict(DATA)
        assert flex.get(get_keys) == get_val


@mark.parametrize('set_keys, set_val', [
    ('a', 1),
    ('a', {'b': 1}),
    (['a', 'b'], 1),
    (['a', 'b'], {'c': 1}),
    ({'a', 'b'}, 1),
    ({'a', 'b'}, {'c': 1}),
    (('a', 'b'), 1),
    (('a', 'b'), {'c': 1})
])
class TestFlexDictSet:
    """Unit tests for setting items."""

    @staticmethod
    def test_set(set_keys, set_val):
        """Setting values."""
        flex = FlexDict()
        flex[set_keys] = set_val
        assert flex[set_keys] == set_val

    @staticmethod
    def test_set_func(set_keys, set_val):
        """Setting values."""
        flex = FlexDict()
        flex.set(set_keys, set_val)
        assert flex[set_keys] == set_val


@mark.parametrize('s_set, flag', [
    (DATA, True),
    ({'h': 5}, True),
    ({'g': 4}, True),
    ({'f': 3}, True),
    ({'f': 3, 'g': 4}, True),
    ({'e': {'f': 3, 'g': 4}}, True),
    ({'d': 2}, True),
    ({'c': 1}, True),
    ({'c': 1, 'd': 2}, True),
    ({'b': {'c': 1, 'd': 2}}, True),
    ({'a': {'b': {'c': 1, 'd': 2}}}, True),
    ({'e': {'f': 3, 'g': 4}, 'h': 5}, True),
    ({'a': {'b': {'c': 1, 'd': 2}}, 'e': {'f': 3, 'g': 4}}, True),
    ({'a': 1}, False)
])
class TestFlexDictSSet:
    """Unit tests for superset/subset detection."""

    @staticmethod
    def test_contains(s_set, flag):
        """Subset detection."""
        flex = FlexDict(DATA)
        assert flex.contains(s_set) is flag

    @staticmethod
    def test_inside(s_set, flag):
        """Superset detection."""
        assert FlexDict(s_set).inside(DATA) is flag
