+++++++++++
Hello World
+++++++++++

This is a series of examples showing the basics of how to write
:term:`coroutines <coroutine>` and schedule them in the asyncio
:term:`event loop <event loop>`.

Simple coroutine
----------------

This example uses the :py:meth:`asyncio.AbstractEventLoop.run_until_complete`
method to schedule a simple function that will wait one second, print
``hello`` and then finish.

Because it is launched with :py:meth:`asyncio.AbstractEventLoop.run_until_complete`,
the :term:`event loop <event loop>` itself
will terminate once the :term:`coroutine <coroutine>` is completed.

.. literalinclude:: examples/hello_world.py


Creating tasks
--------------

This second example shows how you can schedule multiple :term:`coroutines
<coroutine>` in the
event loop, and then run the :term:`event loop <event loop>`.

Notice that this example will print ``second_hello`` before ``first_hello``,
as the first :term:`task <task>` scheduled waits longer that the second one
before printing.

Also note that this example will never terminate, as the  :term:`loop <event
loop>` is asked to
`run_forever`.

.. literalinclude:: examples/create_task.py


Stopping the loop
-----------------

This third example adds another :term:`task <task>` that will stop the
:term:`event loop <event loop>` before
all scheduled :term:`tasks <task>` could execute, which results in a warning.

.. literalinclude:: examples/loop_stop.py

Warning::

      Task was destroyed but it is pending!
      task: <Task pending coro=<say() done, defined at examples/loop_stop.py:3>
      wait_for=<Future pending cb=[Task._wakeup()]>>

