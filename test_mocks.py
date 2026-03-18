class MockTk:
    def __init__(self):
        self.title_text = ""
        self.geometry_text = ""
        self.style = MockStyle()
        self.configure_args = {}
        self._w = "."  # Tkinter internal widget path
        self.children = {}
        self.tk = self  # Mock the tk interpreter

    def title(self, text):
        self.title_text = text

    def geometry(self, text):
        self.geometry_text = text

    def update(self):
        pass

    def destroy(self):
        pass

    def configure(self, **kwargs):
        self.configure_args.update(kwargs)

    def _root(self):
        return self

    def getvar(self, name):
        return ""

    def setvar(self, name="", value=""):
        pass

    def winfo_exists(self):
        return True

    def call(self, *args):
        """Mock the Tcl interpreter call"""
        return None

    def globalsetvar(self, name, value):
        """Mock setting a global Tcl variable"""
        pass

    def globalgetvar(self, name):
        """Mock getting a global Tcl variable"""
        return ""

    def eval(self, script):
        """Mock Tcl interpreter eval"""
        return None

class MockStyle:
    def __init__(self):
        self.theme = "default"
        self.configure_args = {}

    def theme_use(self, theme):
        self.theme = theme

    def configure(self, style, **kwargs):
        self.configure_args[style] = kwargs

class MockWidget:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.configure_args = kwargs
        self._w = "."  # Tkinter internal widget path

    def grid(self, **kwargs):
        self.grid_args = kwargs

    def pack(self, **kwargs):
        self.pack_args = kwargs

    def configure(self, **kwargs):
        self.configure_args.update(kwargs)

    def destroy(self):
        pass

    def update(self):
        pass

class MockStringVar:
    def __init__(self, master=None, value="", name=None):
        self.master = master
        self._value = value
        self.name = name
        self._callbacks = []

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
        for callback in self._callbacks:
            callback()

    def trace_add(self, mode, callback):
        if mode == "write":
            self._callbacks.append(callback)

    def trace_remove(self, mode, cbname):
        if mode == "write" and cbname in self._callbacks:
            self._callbacks.remove(cbname) 