# Mock classes for testing
class MockStringVar:
    def __init__(self, master=None, value=""):
        self.value = value
        self.master = master
        
    def get(self):
        return self.value
        
    def set(self, value):
        self.value = value
        
    def trace(self, *args, **kwargs):
        pass
        
    def trace_add(self, *args, **kwargs):
        pass
