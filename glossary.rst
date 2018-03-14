.. _glossary:

********
Glossary
********

.. if you add new entries, keep the alphabetical sorting!

.. glossary::

    coroutine
        A coroutine is a piece of code that can be paused and resumed. In
        contrast to threads which are preemptively multitasked by the operating
        system, coroutines multitask cooperatively. I.e. they choose when to
        pause (or to use terminology for coroutines before 3.4 - ``yield``)
        execution. They can also execute other coroutines.

    event loop
        The event loop is the central execution device to launch execution of
        coroutines and handle I/O (Network, sub-processes...)

    future
        It's like a mailbox where you can subscribe to receive a result when it
        will be done. See the `Future section`_ of the official documentation.

    task
        It represents the execution of a coroutine and take care the result in a
        future. See the `Task section`_ of the official documentation.

.. _Future section: https://docs.python.org/3/library/asyncio-task.html#future
.. _Task section: https://docs.python.org/3/library/asyncio-task.html#task
