import asyncio
from socket import socketpair
import sys

# Create a pair of connected file descriptors
rsock, wsock = socketpair()

loop = asyncio.new_event_loop()

def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())

    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)

    # Stop the event loop
    loop.stop()

def fileCallback(*args):
    print("Received: " + sys.stdin.readline())

# Register the file descriptor for read event
# loop.add_reader(rsock, reader)
task = loop.add_reader(sys.stdin.fileno(), fileCallback)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

try:
    # Run the event loop
    loop.run_forever()
finally:
    # We are done. Close sockets and the event loop.
    rsock.close()
    wsock.close()
    loop.close()