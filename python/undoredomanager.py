from __future__ import print_function

from abc import ABCMeta, abstractmethod


class EmptyCommandStackError(Exception):
    pass


class SetOperation(object):
    __metaclass__ = ABCMeta

    def __init__(self, set_, element):
        self.set_ = set_
        self.element = element

    @abstractmethod
    def __call__(self):
        return

    @abstractmethod
    def undo(self):
        return


class ElementAdder(SetOperation):
    def __call__(self):
        self.set_.add(self.element)

    def undo(self):
        self.set_.remove(self.element)


class ElementRemover(SetOperation):
    def __call__(self):
        self.set_.remove(self.element)

    def undo(self):
        self.set_.add(self.element)


class CommandManager(object):
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []

    def push_undo_command(self, command):
        """Push the given command to the undo command stack."""
        self.undo_commands.append(command)

    def pop_undo_command(self):
        """Remove the last command from the undo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            raise EmptyCommandStackError()
        return last_undo_command

    def push_redo_command(self, command):
        """Push the given command to the redo command stack."""
        self.redo_commands.append(command)

    def pop_redo_command(self):
        """Remove the last command from the redo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            raise EmptyCommandStackError()
        return last_redo_command

    def do(self, command):
        """Execute the given command. Exceptions raised from the command are
        not catched.

        """
        command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []

    def undo(self, n=1):
        """Undo the last n commands. The default is to undo only the last
        command. If there is no command that can be undone because n is too big
        or because no command has been emitted yet, EmptyCommandStackError is
        raised.

        """
        for _ in xrange(n):
            command = self.pop_undo_command()
            command.undo()
            self.push_redo_command(command)

    def redo(self, n=1):
        """Redo the last n commands which have been undone using the undo
        method. The default is to redo only the last command which has been
        undone using the undo method. If there is no command that can be redone
        because n is too big or because no command has been undone yet,
        EmptyCommandStackError is raised.

        """
        for _ in xrange(n):
            command = self.pop_redo_command()
            command()
            self.push_undo_command(command)


if __name__ == "__main__":
    my_set = {3, 5, 13}
    print("initial set: {}".format(my_set))
    manager = CommandManager()
    # remove element 5 from the set
    manager.do(ElementRemover(my_set, 5))
    print("set after removing 5: {}".format(my_set))
    # add element -7 to the set
    manager.do(ElementAdder(my_set, -7))
    print("set after adding -7 to the set: {}".format(my_set))
    # undo adding the element -7
    manager.undo()
    print("set after undoing adding -7 to the set: {}".format(my_set))
    # undo removing the element 5 from the set
    manager.undo()
    print("set after undoing removing 5 from the set: {}".format(my_set))
    # redo both undone operations
    manager.redo(2)
    print("set after redoing the just undone operations: {}".format(my_set))
