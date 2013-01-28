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

class Model(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        # usaually dynamic, but here only a static list to make it simple
        self.records = zip(
            [
                QtCore.QVariant('Blub'),
                QtCore.QVariant('Foo'),
                QtCore.QVariant('Bar'),
                QtCore.QVariant('eggs')
            ],
            [
                QtCore.QVariant('Table tennis'),
                QtCore.QVariant('Basketball'),
                QtCore.QVariant('Baseball'),
                QtCore.QVariant('Squash'),
            ]
        )

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.records)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return max(len(item) for item in self.records)

    def headerData(self, section, orientation, role):
        """ set the column and row headers """
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        column_headers = [
            QtCore.QVariant('nonsense'),
            QtCore.QVariant('sports')
        ]

        if orientation == QtCore.Qt.Horizontal:
            return column_headers[section]

        # the row headers (a regular counter)
        else:
            return QtCore.QVariant(section + 1)

    def data(self, index, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        else:
            return QtCore.QVariant(self.records[index.row()][index.column()])

if __name__ == '__main__':
    model = Model()
    app = QtGui.QApplication(sys.argv)
    records = QtGui.QTableView()
    records.setModel(model)
    records.resize(250, 200)
    records.show()
    sys.exit(app.exec_())
