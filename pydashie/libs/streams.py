import sys
import json
if sys.version_info >= (3, 0):
    import queue as Queue
else:
    import Queue


class ConnectionStreams:
    def __init__(self):
        self.MAX_QUEUE_LENGTH = 20
        self.MAX_LAST_EVENTS = 2
        self.events_queue = {}
        self.last_events = ['data: {}\n\n'] * self.MAX_LAST_EVENTS
        self.using_events = True
        self.stopped = False

    def __del__(self):
        self.stop()

    def __len__(self):
        return len(self.events_queue)

    def send(self, body, bStoreEvent=True):
        formatted_json = 'data: %s\n\n' % (json.dumps(body))
        for event_queue in self.events_queue.values():
            event_queue.put(formatted_json)
        if bStoreEvent:
            self.last_events.append(formatted_json)
            self.last_events.pop(0)
        return formatted_json

    def openStream(self, streamID):
        current_event_queue = Queue.Queue()
        self.events_queue[streamID] = current_event_queue
        # Start the newly connected client off by pushing the current last events
        for event in self.last_events:
            current_event_queue.put(event)
        while not self.stopped:
            try:
                data = current_event_queue.get(timeout=0.1)
                yield data
            except Queue.Empty:
                # this makes the server quit nicely - previously the queue threads would block and never exit.
                # This makes it keep checking for dead application
                pass

    def closeStream(self, streamID):
        del self.events_queue[streamID]

    def stop(self):
        self.stopped = True



