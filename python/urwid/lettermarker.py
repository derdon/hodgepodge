import urwid
from string import ascii_lowercase


def on_key_press(key):
    if key in ascii_lowercase:
        pass
    elif key == 'esc':
        raise urwid.ExitMainLoop()


def main(letters_to_be_marked):
    def attr_name(letter):
        return 'marked' if letter in letters_to_be_marked else 'unmarked'
    def decorate(letter):
        return letter.upper() if letter in letters_to_be_marked else letter
    letters = [
        urwid.Text((attr_name(letter), decorate(letter))) for letter in ascii_lowercase]
    cols = urwid.Columns(letters)
    fill = urwid.Filler(cols, 'top')
    palette = [
        ('unmarked', 'dark gray', 'black'),
        ('marked', 'white,bold', 'black')]
    loop = urwid.MainLoop(
        fill, palette, handle_mouse=False, unhandled_input=on_key_press)
    loop.run()

if __name__ == '__main__':
    main(set(u'dgkprtx'))
