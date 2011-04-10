from itertools import imap

import urwid


class TestDisplay(object):
    BUTTON_LABEL_PREFIX = '< '
    BUTTON_LABEL_SUFFIX = ' >'
    BASE_CELL_WIDTH_LENGTH = len(BUTTON_LABEL_PREFIX + BUTTON_LABEL_SUFFIX)

    def __init__(self):
        self.number = urwid.Text('0')
        self.increment_button = urwid.Button(
            'increment', on_press=self.increment_number)
        self.decrement_button = urwid.Button(
            'decrement', on_press=self.decrement_number)
        buttons = [self.increment_button, self.decrement_button]
        button_grid = self.create_button_grid(buttons)
        main_layout = urwid.Pile([button_grid, self.number])
        filler = urwid.Filler(main_layout, 'top')
        self.loop = urwid.MainLoop(
            filler, unhandled_input=self.unhandled_input)

    def main(self):
        self.loop.run()

    def unhandled_input(self, input):
        if input in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()

    def create_button_grid(self, buttons):
        longest_label_length = max(
            imap(lambda button: len(button.label), buttons))
        cell_width = longest_label_length + self.BASE_CELL_WIDTH_LENGTH
        button_grid = urwid.GridFlow(buttons, cell_width, 1, 1, 'left')
        return button_grid

    def increment_number(self, button):
        current_number = int(self.number.text)
        if current_number < 10:
            self.number.set_text(str(current_number + 1))
        else:
            # remove or disable the button
            new_button_grid = self.create_button_grid([self.decrement_button])
            new_main_layout = urwid.Pile([new_button_grid, self.number])
            new_filler = urwid.Filler(new_main_layout, 'top')
            self.loop.widget = new_filler
            self.loop.draw_screen()

    def decrement_number(self, button):
        current_number = int(self.number.text)
        if current_number > -10:
            self.number.set_text(str(current_number - 1))
        else:
            # remove or disable the button
            pass


def main():
    TestDisplay().main()

if __name__ == '__main__':
    main()
