import time

class Event:
    _instancecounter = 0
    
    def __init__(self):
        # Store timestamp associated with event creation
        self.timestamp = time.time()
    
        # Allot a unique id to each event, by virtue of class counter
        self.id = Event._instancecounter
        Event._instancecounter += 1
    
        self.content = None
    
    def set_event_data(self, data):
        self.content = data
    
    def get_event_data(self):
        return self.content