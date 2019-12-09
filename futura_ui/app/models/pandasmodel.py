from PySide2 import QtCore
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.df = df.copy()

    def toDataFrame(self):
        return self.df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self.df.columns.tolist()[section]
            except (IndexError, ):
                return None
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self.df.index.tolist()[section]
            except (IndexError, ):
                return None

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if not index.isValid():
            return None

        if self.df.columns[index.column()] == 'Percentage':
            return "{0:.2%}".format(self.df.iloc[index.row(), index.column()])
        elif self.df.columns[index.column()] == 'Production':
            return "{0:,.0f}".format(self.df.iloc[index.row(), index.column()])
        else:
            return str(self.df.iloc[index.row(), index.column()])

    def setData(self, index, value, role):
        row = self.df.index[index.row()]
        col = self.df.columns[index.column()]

        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self.df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self.df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns)

    def sort(self, column, order):
        colname = self.df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self.df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.Property(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.Slot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return None
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype
