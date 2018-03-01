Synchrio
========

Synchrio is a tool that allows you to wrap an object containing asynchronous code and run it fully in blocking code.
The wrapper class simply executes async functions rather than return a coroutine for them, and doesn't limit any
functionality of the wrapped object.

This is useful for creating libraries that can be used in blocking or non-blocking code. Create the library using async,
and have another version where the top level module is wrapped with the AsyncWrapper class for users who want to run
your code synchronously (You can even use the wrapped version to test without async!)

Using Synchrio
--------------

To use Synchrio, all you need to do is pass an object to the `AsyncWrapper` class. The object can be a module, class,
function, coroutine, etc.. Any time you try to call a coroutine, it will be run in an asyncio event loop for the
wrapper. If you'd like to see a working example, you can test it on aiohttp_ (although this isn't the best use case
of Synchrio):

.. code-block:: Python
    from synchrio import AsyncWrapper
    import aiohttp as _aiohttp

    aiohttp = AsyncWrapper(_aiohttp)

    session = aiohttp.ClientSession()
    with session.get("https://httpbin.org/status/418") as resp:  # normally "async with"
        print(resp.text())  # normally "await resp.text()"


    >>>    -=[ teapot ]=-
    ...
    ...       _...._
    ...     .'  _ _ `.
    ...    | ."` ^ `". _,
    ...    \_;`"---"`|//
    ...      |       ;/
    ...      \_     _/
    ...        `"""`
    ...

.. _aiohttp: https://aiohttp.readthedocs.io/en/stable/