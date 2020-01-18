++++++++++++
Web Scraping
++++++++++++

Web scraping means downloading multiple web pages, often from different
servers.
Typically, there is a considerable waiting time between sending a request and
receiving the answer.
Using a client that always waits for the server to answer before sending
the next request, can lead to spending most of time waiting.
Here ``asyncio`` can help to send many requests without waiting for a response
and collecting the answers later.
The following examples show how a synchronous client spends most of the time
waiting and how to use ``asyncio`` to write asynchronous client that
can handle many requests concurrently.

A Mock Web Server
-----------------

This is a very simple web server. (See below for the code.)
Its only purpose is to wait for a given amount of time.
Test it by running it from the command line::

    $ python simple_server.py

It will answer like this::

    Serving from port 8000 ...

Now, open a browser and go to this URL::

    http://localhost:8000/

You should see this text in your browser::

    Waited for 0.00 seconds.

Now, add ``2.5`` to the URL::

   http://localhost:8000/2.5

After pressing enter, it will take 2.5 seconds until you see this
response::

    Waited for 2.50 seconds.

Use different numbers and see how long it takes until the server responds.

The full implementation looks like this:

.. literalinclude:: examples/simple_server.py
    :language: python

Let's have a look into the details.
This provides a simple multi-threaded web server:

.. literalinclude:: examples/simple_server.py
    :language: python
    :start-after: ENCODING = 'utf-8'
    :end-before: class MyRequestHandle

It uses multiple inheritance.
The mix-in class ``ThreadingMixIn`` provides the multi-threading support and
the class ``HTTPServer`` a basic HTTP server.


The request handler only has a ``GET`` method:


.. literalinclude:: examples/simple_server.py
    :language: python
    :start-after: pass
    :end-before: def run(

It takes the last entry in the paths with ``self.path[1:]``, i.e.
our ``2.5``, and tries to convert it into a floating point number.
This will be the time the function is going to sleep, using ``time.sleep()``.
This means waiting 2.5 seconds until it answers.
The rest of the method contains the HTTP header and message.

A Synchronous Client
--------------------

Our first attempt is synchronous.
This is the full implementation:

.. literalinclude:: examples/synchronous_client.py

Again, we go through it step-by-step.

While about 80 % of the websites use ``utf-8`` as encoding
(provided by the default in ``ENCODING``), it is a good idea to actually use
the encoding specified by ``charset``.
This is our helper to find out what the encoding of the page is:

.. literalinclude:: examples/synchronous_client.py
    :language: python
    :start-after: ENCODING = 'ISO-8859-1'
    :end-before: def get_page

It falls back to ``ISO-8859-1`` if it cannot find a specification of the
encoding.

Using ``urllib.request.urlopen()``, retrieving a web page is rather simple.
The response is a bytestring and ``.encode()`` is needed to convert it into a
string:

.. literalinclude:: examples/synchronous_client.py
    :language: python
    :start-after: return ENCODING
    :end-before: def get_multiple_pages

Now, we want multiple pages:

.. literalinclude:: examples/synchronous_client.py
    :language: python
    :start-after: return html
    :end-before: if __name__ == '__main__':

We just iterate over the waiting times and call ``get_page()`` for all
of them.
The function ``time.perf_counter()`` provides a time stamp.
Taking two time stamps a different points in time and calculating their
difference provides the elapsed run time.

Finally, we can run our client::

    $ python synchronous_client.py

and get this output::

    It took 11.08 seconds for a total waiting time of 11.00.
    Waited for 1.00 seconds.
    That's all.

    Waited for 5.00 seconds.
    That's all.

    Waited for 3.00 seconds.
    That's all.

    Waited for 2.00 seconds.
    That's all.

Because we wait for each call to ``get_page()`` to complete, we need to
wait about 11 seconds.
That is the sum of all waiting times.
Let's see if we can do it any better going asynchronously.


Getting One Page Asynchronously
-------------------------------

This module contains a functions that reads a page asynchronously,
using the new Python 3.5 keywords ``async`` and ``await``:

.. literalinclude:: examples/async_page.py

As with the synchronous example, finding out the encoding of the page
is a good idea.
This function helps here by going through the lines of the HTTP header,
which it gets as an argument, searching for ``charset`` and returning its value
if found.
Again, the default encoding is ``ISO-8859-1``:

.. literalinclude:: examples/async_page.py
    :language: python
    :start-after: ENCODING = 'ISO-8859-1'
    :end-before: async def get_page

The next function is way more interesting because it actually works
asynchronously:

.. literalinclude:: examples/async_page.py
    :language: python
    :start-after: return ENCODING

The function ``asyncio.open_connection()`` opens a connection to the given URL.
It returns a coroutine.
Using ``await``, which had to be ``yield from`` in Python versions prior
to 3.5, it yields an instance of a ``StreamReader`` and one of a
``StreamWriter``.
These only work within the event loop.

Now, we can send a ``GET`` request, suppling our waiting time by
writing to the ``StreamWriter`` instance ``writer``.
The request has to be in bytes.
Therefore, we need to convert our strings in to bytestrings.

Next, we read header and message from the reader, which is a ``StreamReader``
instance.
We need to iterate over the reader by using a special or loop for
``asyncio``:

.. code-block:: python

    async for raw_line in reader:


Header and message are dived by an empty line.
We just stop the iteration as soon as we found an empty line.
Handing the header over too ``get_encoding()`` provides the encoding
of the retrieved page.
The ``.decode()`` method uses this encoding to convert the read bytes
into strings.
After closing the writer, we can return the message lines joined by newline
characters.

Getting Multiple Pages Asynchronously - Without Time Savings
------------------------------------------------------------

This is our first approach retrieving multiple pages, using our asynchronous
``get_page()``:


.. literalinclude:: examples/async_client_blocking.py


The interesting things happen in a few lines in ``get_multiple_pages()``
(the rest of this function just measures the run time and displays it):

.. literalinclude:: examples/async_client_blocking.py
    :language: python
    :start-after: pages = []
    :end-before: duration

The ``closing`` from the standard library module ``contextlib`` starts
the event loop within a context and closes the loop when leaving the context:

.. code-block:: python

    with closing(asyncio.get_event_loop()) as loop:
        <body>

The two lines above are equivalent to these five lines:

.. code-block:: python

    loop = asyncio.get_event_loop():
    try:
        <body>
    finally:
        loop.close()

We call ``get_page()`` for each page in a loop.
Here we decide to wrap each call in ``loop.run_until_complete()``:

.. code-block:: python

    for wait in waits:
        pages.append(loop.run_until_complete(get_page(host, port, wait)))

This means, we wait until each pages has been retrieved before asking for
the next.
Let's run it from the command-line to see what happens::

    $ async_client_blocking.py
    It took 11.06 seconds for a total waiting time of 11.00.
    Waited for 1.00 seconds.
    That's all.
    Waited for 5.00 seconds.
    That's all.
    Waited for 3.00 seconds.
    That's all.
    Waited for 2.00 seconds.
    That's all.

So it still takes about eleven seconds in total.
We made it more complex and did not improve speed.
Let's see if we can do better.

Getting Multiple Pages Asynchronously - With Time Savings
---------------------------------------------------------

We want to take advantage of the asynchronous nature of ``get_page()``
and save time.
We modify our client to use a list with four instances of
a :term:`task <task>`.
This allows us to send out requests for all pages we want to retrieve without
waiting for the answer before asking for the next page:

.. literalinclude:: examples/async_client_nonblocking.py

The interesting part is in this loop:

.. code-block:: python

    with closing(asyncio.get_event_loop()) as loop:
        for wait in waits:
            tasks.append(get_page(host, port, wait))
        pages = loop.run_until_complete(asyncio.gather(*tasks))

We append all return values of ``get_page()`` to our lits of tasks.
This allows us to send out all request, in our case four, without
waiting for the answers.
After sending all of them, we wait for the answers, using:

.. code-block:: python

    loop.run_until_complete(asyncio.gather(*tasks))

We used ``loop.run_until_complete()`` already for each call to ``get_page()``
in the previous section.
The difference here is the use of ``asyncio.gather()`` that is called with all
our tasks in the list ``tasks`` as arguments.
The ``asyncio.gather(*tasks)`` means for our example with four list entries:

.. code-block:: python

    asyncio.gather(tasks[0], tasks[1], tasks[2], tasks[3])

So, for a list with 100 tasks it would mean:

.. code-block:: python

    asyncio.gather(tasks[0], tasks[1], tasks[2],
                   # 96 more tasks here
                   tasks[99])


Let's see if we got any faster::

    $ async_client_nonblocking.py
    It took 5.08 seconds for a total waiting time of 11.00.
    Waited for 1.00 seconds.
    That's all.
    Waited for 5.00 seconds.
    That's all.
    Waited for 3.00 seconds.
    That's all.
    Waited for 2.00 seconds.
    That's all.

Yes! It works.
The total run time is about five seconds.
This is the run time for the longest wait.
Now, we don't have to wait for the sum of ``waits`` but rather for
``max(waits)``.

We did quite a bit of work, sending a request and scanning an answer,
including finding out the encoding.
There should be a shorter way as these steps seem to be always necessary for
getting the page content with the right encoding.
Therefore, in the next section, we will have a look at high-level library
``aiohttp`` that can help to make our code shorter.

Exercise
++++++++

Add more waiting times to the list ``waits`` and see how this impacts
the run times of the blocking and the non-blocking implementation.
Try (positive) numbers that are all less than five.
Then try numbers greater than five.

High-Level Approach with ``aiohttp``
------------------------------------

The library aiohttp_ allows to write HTTP client and server applications,
using a high-level approach.
Install with::

    $ pip install aiohttp


.. _aiohttp: https://aiohttp.readthedocs.io/en/stable/

The whole program looks like this:

.. literalinclude:: examples/aiohttp_client.py

The function to get one page is asynchronous, because of the ``async def``:


.. literalinclude:: examples/aiohttp_client.py
    :language: python
    :start-after: import aiohttp
    :end-before: def get_multiple_pages

The arguments are the same as those for the previous function to retrieve one
page plus the additional argument ``session``.
The first task is to construct the full URL as a string from the given
host, port, and the desired waiting time.

We use a timeout of 10 seconds.
If it takes longer than the given time to retrieve a page, the programm
throws a ``TimeoutError``.
Therefore, to make this more robust, you might want to catch this error and
handle it appropriately.

The ``async with`` provides a context manager that gives us a response.
After checking the status being ``200``, which means that all is alright,
we need to ``await`` again to return the body of the page, using the method
``text()`` on the response.

This is the interesting part of ``get_multiple_pages()``:

.. code-block:: python

    with closing(asyncio.get_event_loop()) as loop:
        with aiohttp.ClientSession(loop=loop) as session:
            for wait in waits:
                tasks.append(fetch_page(session, host, port, wait))
            pages = loop.run_until_complete(asyncio.gather(*tasks))

It is very similar to the code in the example of the time-saving implementation
with ``asyncio``.
The only difference is the opened client session and handing over this session
to ``fetch_page()`` as the first argument.

Finally, we run this program::

    $ python aiohttp_client.py
    It took 5.04 seconds for a total waiting time of 11.00.
    Waited for 1.00 seconds.
    That's all.

    Waited for 5.00 seconds.
    That's all.

    Waited for 3.00 seconds.
    That's all.

    Waited for 2.00 seconds.
    That's all.

It also takes about five seconds and gives the same output as our version
before.
But the implementation for getting a single page is much simpler and takes
care of the encoding and other aspects not mentioned here.

