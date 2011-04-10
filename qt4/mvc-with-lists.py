#!/usr/bin/env python
# Copyright (C) 2009  Simon Liedtke
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from PyQt4 import QtGui, QtCore

class Model(QtCore.QAbstractListModel):
    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        # usaually dynamic, but here only a static list to make it simple
        self.records = [
            QtCore.QVariant('Blub'),
            QtCore.QVariant('Foo'),
            QtCore.QVariant('Bar'),
            QtCore.QVariant('eggs')
        ]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.records)

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.records[index.row()])

if __name__ == '__main__':
    model = Model()
    app = QtGui.QApplication(sys.argv)
    records = QtGui.QListView()
    records.setModel(model)
    records.show()
    sys.exit(app.exec_())
