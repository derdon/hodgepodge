import urwid


class TestDisplay(object):
    DEFAULT_TEXT = 'default text'
    OTHER_TEXT = 'other text'
    BUTTON_LABEL_PREFIX = '< '
    BUTTON_LABEL_SUFFIX = ' >'
    BASE_CELL_WIDTH_LENGTH = len(BUTTON_LABEL_PREFIX + BUTTON_LABEL_SUFFIX)

    def __init__(self):
        # create a text widget with a default content
        self.text = urwid.Text(self.DEFAULT_TEXT)

        # create a button widget whose callback toggles the content of the
        # text widget
        toggle_text_button = urwid.Button(
            'change the text',
            on_press=self.toggle_text)

        # To display the button, it is stored in a GridFlow widget. This
        # container widget is made for the widgets Button, CheckBox and
        # RadioButton. One special thing about GridFlow is that all the widgets
        # in it get the same width. To compute this width, the length of the
        # button label is used.
        button_label_length = len(toggle_text_button.label)
        cell_width = button_label_length + self.BASE_CELL_WIDTH_LENGTH

        # Create a GridFlow widget with the button in it, as explained above.
        # The two ones define the number of blank columns and rows between the
        # widgets, respectively.
        buttons = urwid.GridFlow(
            [toggle_text_button], cell_width, 1, 1, 'left')

        # put the button and the text widget in a Pile widget to stack these
        # widgets vertically
        main_layout = urwid.Pile([buttons, self.text])

        # urwid.MainLoop receives a box widget as the first parameter. Because
        # main_layout is a Pile widget with two flow widgets in it, main_layout
        # itself is a flow widget. To convert it into a box widget, the flow
        # widget main_layout is put into a Filler widget. Filler is always a
        # box widget, so everything is fine now :-)
        filler = urwid.Filler(main_layout, 'top')

        # The first parameter is the topmost widget of the application. This
        # must be a box widget, as said above.
        # The keyword argument unhandled_input receives a function with one
        # argument, the passed input as a string. This function will be called
        # each time the user entered a key but no particular widget waits for
        # this input.
        self.loop = urwid.MainLoop(
            filler, unhandled_input=self.unhandled_input)

    def main(self):
        # start the main loop
        self.loop.run()

    def unhandled_input(self, input):
        # exit the script with the key q, Q or the Escape key
        if input in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()

    def toggle_text(self, button):
        if self.text.text == self.DEFAULT_TEXT:
            self.text.set_text(self.OTHER_TEXT)
        else:
            assert self.text.text == self.OTHER_TEXT
            self.text.set_text(self.DEFAULT_TEXT)


def main():
    TestDisplay().main()

if __name__ == '__main__':
    main()
