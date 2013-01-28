from gi.repository import Gtk


class SimpleApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.counter = 0
        self.button = Gtk.Button(label=str(self.counter))
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.connect("delete-event", Gtk.main_quit)

    def on_button_clicked(self, button):
        self.counter += 1
        self.button.set_label(str(self.counter))


def main():
    win = SimpleApp()
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
