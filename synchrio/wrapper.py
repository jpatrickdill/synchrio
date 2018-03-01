"""
Synchrio is a wrapper for async libraries that allows you to use them in blocking code.
Copyright (C) 2018  James Patrick Dill

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import inspect


class AsyncWrapper(object):
    """
    This class accepts any object, including modules, and will return any coroutine functions as blocking functions that
    run the asynchronous code.

    Attributes and methods' return values also get passed into :class:`AsyncWrapper`
    Coroutine methods can be run as regular blocking code.

    :param obj: Object to wrap.
    """

    __mine__ = ["__obj__", "__loop__",
                "__name__", "__doc__", "__annotations__"]

    def __init__(self, obj, *, _loop=None):
        self.__obj__ = obj
        self.__loop__ = _loop or asyncio.get_event_loop()

        self.__name__ = getattr(obj, "__name__", "")
        self.__doc__ = getattr(obj, "__doc__", "")
        self.__annotations__ = getattr(obj, "__annotations__", {})

    def _run_as_blocking(self, coroutine):
        """Runs a coroutine in blocking code."""

        value = self.__loop__.run_until_complete(coroutine)

        return value

    def __getattr__(self, item):
        if item in AsyncWrapper.__mine__:
            return object.__getattribute__(self, item)

        obj = getattr(self.__obj__, item)

        return AsyncWrapper(obj, _loop=self.__loop__)  # wrap any attributes with AsyncWrapper

    def __setattr__(self, name, value):
        if name in AsyncWrapper.__mine__:
            return object.__setattr__(self, name, value)

        if isinstance(value, AsyncWrapper):
            value = value.__obj__  # don't set values to AsyncWrappers, only return them

        setattr(self.__obj__, name, value)

    def __call__(self, *args, **kwargs):
        value = self.__obj__(*args, **kwargs)

        # coroutine functions return coroutines
        # executing any returned coroutine allows async functions to be wrapped as well
        if inspect.iscoroutine(value):
            return AsyncWrapper(self.run_as_blocking(value), _loop=self.__loop__)

        return AsyncWrapper(value)

    def __repr__(self):
        return "AsyncWrapper( {!r} )".format(self.__obj__)

    def __str__(self):
        return str(self.__obj__)

    def __dir__(self):
        return dir(self.__obj__)

    def __enter__(self):
        if hasattr(self.__obj__, "__aenter__"):
            return AsyncWrapper(self._run_as_blocking(self.__obj__.__aenter__()), _loop=self.__loop__)

    def __exit__(self, *args):
        if hasattr(self.__obj__, "__aexit__"):
            self._run_as_blocking(self.__obj__.__aexit__(*args))

    def __del__(self):
        self.__obj__.__del__()

    def __bytes__(self):
        return bytes(self.__obj__)

    def __format__(self, format_spec):
        return format(self.__obj__, format_spec)

    def __lt__(self, other):
        return self.__obj__ < other

    def __le__(self, other):
        return self.__obj__ <= other

    def __eq__(self, other):
        return self.__obj__ == other

    def __ne__(self, other):
        return self.__obj__ != other

    def __gt__(self, other):
        return self.__obj__ > other

    def __ge__(self, other):
        return self.__obj__ >= other

    def __hash__(self):
        return hash(self.__obj__)

    def __bool__(self):
        return bool(self.__obj__)

    def __get__(self, instance, owner):
        return AsyncWrapper(self.__obj__.__get__(instance, owner), _loop=self.__loop__)

    def __set__(self, instance, value):
        self.__obj__.__set__(instance, value)

    def __delete__(self, instance):
        self.__obj__.__delete__(instance)

    def __len__(self):
        return len(self.__obj__)

    def __getitem__(self, item):
        return AsyncWrapper(self.__obj__[item], _loop=self.__loop__)

    def __missing__(self, key):
        return AsyncWrapper(self.__obj__.__missing__(key), _loop=self.__loop__)

    def __setitem__(self, key, value):
        self.__obj__[key] = value

    def __delitem__(self, key):
        del self.__obj__[key]

    def __iter__(self):
        return iter([
            AsyncWrapper(o, _loop=self.__loop__) for o in iter(self.__obj__)
        ])

    def __contains__(self, item):
        return item in self.__obj__

    def __add__(self, other):
        return AsyncWrapper(self.__obj__.__add__(other), _loop=self.__loop__)

    def __sub__(self, other):
        return AsyncWrapper(self.__obj__.__sub__(other), _loop=self.__loop__)

    def __mul__(self, other):
        return AsyncWrapper(self.__obj__.__mul__(other), _loop=self.__loop__)

    def __matmul__(self, other):
        return AsyncWrapper(self.__obj__.__matmul__(other), _loop=self.__loop__)

    def __truediv__(self, other):
        return AsyncWrapper(self.__obj__.__truediv__(other), _loop=self.__loop__)

    def __floordiv__(self, other):
        return AsyncWrapper(self.__obj__.__floordiv__(other), _loop=self.__loop__)

    def __mod__(self, other):
        return AsyncWrapper(self.__obj__.__mod__(other), _loop=self.__loop__)

    def __divmod__(self, other):
        return AsyncWrapper(self.__obj__.__divmod__(other), _loop=self.__loop__)

    def __pow__(self, power, modulo=None):
        return AsyncWrapper(self.__obj__.__pow__(power, modulo=modulo), _loop=self.__loop__)

    def __lshift__(self, other):
        return AsyncWrapper(self.__obj__.__lshift__(other), _loop=self.__loop__)

    def __rshift__(self, other):
        return AsyncWrapper(self.__obj__.__rshift__(other), _loop=self.__loop__)

    def __and__(self, other):
        return AsyncWrapper(self.__obj__.__and__(other), _loop=self.__loop__)

    def __xor__(self, other):
        return AsyncWrapper(self.__obj__.__xor__(other), _loop=self.__loop__)

    def __or__(self, other):
        return AsyncWrapper(self.__obj__.__or__(other), _loop=self.__loop__)

    def __neg__(self):
        return AsyncWrapper(-self.__obj__, _loop=self.__loop__)

    def __pos__(self):
        return AsyncWrapper(+self.__obj__, _loop=self.__loop__)

    def __abs__(self):
        return AsyncWrapper(abs(self.__obj__), _loop=self.__loop__)

    def __invert__(self):
        return AsyncWrapper(~self.__obj__, _loop=self.__loop__)

    def __complex__(self):
        return complex(self.__obj__)

    def __int__(self):
        return int(self.__obj__)

    def __float__(self):
        return float(self.__obj__)

    def __round__(self, n=None):
        return round(self.__obj__, n)
