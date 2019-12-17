from PySide2 import QtWidgets, QtCore, QtGui

from ..widgets.filter import FilterListerWidget, parse_filter_widget
from ..widgets.geo import LocationSelectorWidget
from ...utils import findMainWindow

from ...models import PandasModel, FuturaRecipePrettifier

from ..dialogs import EditProductionDialog, TransferProductionDialog

from ..ui_files import Ui_MarketsWizard

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import pandas as pd

from futura.utils import create_filter_from_description
from futura.markets import FuturaMarket, find_possible_additional_market_exchanges
from futura import w


class MarketsWizard(Ui_MarketsWizard, QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MarketsWizard, self).__init__(parent)

        self.setupUi(self)

        self.filter_widget = FilterListerWidget()
        self.filterLayout.addWidget(self.filter_widget)

        self.market = None
        self.model = None
        self.figure, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas)
        self.table = QtWidgets.QTableView()
        self.dataframe = None
        self.selected_item = None
        self.base_market = None
        self.base_market_filter = None

        self.recipe_section = []

        self.connect_signals()

    @property
    def final_recipe_section(self):
        recipe = {
            'action': 'alter_market',
            'tasks': [{
                'function': 'set_market',
                'kwargs': {
                    'market_filter': self.base_market_filter
                }
            }]
        }
        recipe['tasks'].extend(self.recipe_section)
        recipe['tasks'].append({
            'function': 'relink'
        })
        return recipe

    def connect_signals(self):

        self.currentIdChanged.connect(self.page_change)
        self.setButton.pressed.connect(self.set_production)
        self.transferButton.pressed.connect(self.transfer_production)
        self.addButton.pressed.connect(self.add_alternatives)

    def page_change(self, page_id):

        if page_id == 1:
            self.setup_market()
        if page_id == 2:
            self.setup_confirmation()

    def setup_market(self):

        force_market = [{'filter': 'startswith', 'args': ['name', 'market']}]
        base_filter = parse_filter_widget(self.filter_widget)

        full_filter = force_market + base_filter
        self.base_market_filter = full_filter
        this_filter = create_filter_from_description(full_filter)
        db = findMainWindow().loader.database.db

        self.base_market = w.get_one(db, *this_filter)

        self.market = FuturaMarket(self.base_market, findMainWindow().loader.database)
        self.dataframe = self.generate_dataframe()
        self.model = PandasModel(self.dataframe)
        self.tableView.setModel(self.model)
        self.tableView.selectionModel().selectionChanged.connect(self.table_selected)
        self.tableView.doubleClicked.connect(self.set_production)
        self.tableView.horizontalHeader().sectionClicked.connect(self.update_chart)
        self.update_chart()

        #self.canvas.clear()


    def update_chart(self):
        self.axes.clear()
        print("updating chart")
        self.model.df.plot(kind='pie',
                           labels=[',\n'.join(x.split(','))
                                   if self.model.df['Percentage'][n] > 0.05
                                   else ''
                                   for n, x in enumerate(self.model.df['Name'])
                                   ],
                           y='Percentage',
                           legend=None,
                           title='',
                           fontsize=8,
                           ax=self.axes)
        self.axes.yaxis.set_label_text("")

        self.canvas.draw()

    def generate_dataframe(self):
        to_df = []
        for k, v in self.market.process_dict.items():
            row = {
                'Name': k,
                'Location': v['process']['location'],
                'Production': v['production volume'],
                'Percentage': v['production volume'] / self.market.total_production,
            }
            to_df.append(row)

        to_df = sorted(to_df, key=lambda x: x['Percentage'], reverse=True)

        df = pd.DataFrame(to_df)
        df['Name'] = df['Name'].astype(str)
        df['Location'] = df['Location'].astype(str)
        # styled_df = df.style.hide_index().format({'Percentage': '{0:.2%}', 'Production': '{:,.0f}'})

        return df

    def table_selected(self, ix):
        self.selected_item = ix.indexes()
        self.setButton.setEnabled(True)
        self.transferButton.setEnabled(True)

    def set_production(self):

        validator = QtGui.QDoubleValidator()
        validator.setDecimals(0)

        dialog = EditProductionDialog()

        dialog.nameLabel.setText(self.selected_item[0].data())
        dialog.currentValueLabel.setText(self.selected_item[2].data())

        dialog.newValueLineEdit.setValidator(validator)
        # dialog.newValueLineEdit.setInputMask("0"*100)
        dialog.newValueLineEdit.setText(self.selected_item[2].data().replace(',',''))

        if dialog.exec_():
            print('Dialog set')
            print("{} | {} --> {}".format(dialog.nameLabel.text(),
                                          dialog.currentValueLabel.text(),
                                          dialog.newValueLineEdit.text()))
            self.model.setData(self.selected_item[2], dialog.newValueLineEdit.text(), QtCore.Qt.DisplayRole)

            self.update_percentages()

            recipe_item = {
                'function': 'set_pv',
                'kwargs': {
                    'process_name': self.selected_item[0].data(),
                    'new_pv': dialog.newValueLineEdit.text()
                }
            }
            print(recipe_item)
            self.recipe_section.append(recipe_item)

        else:
            print('Cancelled')

    def update_percentages(self):
        total = self.model.df['Production'].sum()
        self.model.df['Percentage'] = self.model.df['Production'] / total
        self.model.sort(2, QtCore.Qt.DescendingOrder)
        self.update_chart()

    def transfer_production(self):
        validator = QtGui.QDoubleValidator()
        validator.setDecimals(0)

        dialog = TransferProductionDialog()

        dialog.fromLabel.setText(self.selected_item[0].data())
        dialog.currentValueLabel.setText(self.selected_item[2].data())

        to_items = list(self.model.df['Name'])
        to_items.remove(self.selected_item[0].data())
        dialog.toComboBox.addItems(to_items)

        if dialog.exec_():
            print('Dialog set')
            from_name = dialog.fromLabel.text()
            to_name = dialog.toComboBox.currentText()

            recipe_item = {
                'function': 'transfer_pv',
                'kwargs': {
                    'from_name': from_name,
                    'to_name': to_name,
                }
            }

            if dialog.percentageRadioButton.isChecked():
                type = 'factor'
                amount = float(dialog.newValueLineEdit.text().replace('%',''))/100
                recipe_item['kwargs']['factor'] = amount
            else:
                type = 'amount'
                amount = float(dialog.newValueLineEdit.text())
                recipe_item['kwargs']['amount'] = amount

            print(recipe_item)
            self.recipe_section.append(recipe_item)

        #to_model_item = self.model.findItems(to_name)
        #print(to_model_item)
        match = self.model.df.index[self.model.df['Name'] == to_name].tolist()[0]

        from_pv = int(self.selected_item[2].data().replace(',', ''))
        to_pv = int(self.model.index(match, 2).data().replace(',', ''))

        print(from_pv, to_pv)

        if type == 'amount':
            assert amount <= from_pv, "you can't transfer more pv than is available"
            self.model.setData(self.selected_item[2], from_pv - amount, QtCore.Qt.DisplayRole)
            self.model.setData(self.model.index(match, 2), to_pv + amount, QtCore.Qt.DisplayRole)

        elif type == 'factor':
            assert 0 <= amount <= 1, "factor must be between 0 and 1"
            transfer_amount = from_pv*amount
            self.model.setData(self.selected_item[2], from_pv - transfer_amount, QtCore.Qt.DisplayRole)
            self.model.setData(self.model.index(match, 2), to_pv + transfer_amount, QtCore.Qt.DisplayRole)

        self.update_percentages()

    def add_alternatives(self):

        database = findMainWindow().loader.database

        possibles = find_possible_additional_market_exchanges(self.base_market, database, include_transport=False)

        print(self.model.rowCount())
        self.model.insertRow(self.model.rowCount())
        print(self.model.rowCount())

        new_row = self.model.rowCount()

        for p in possibles:

            to_add = [{
                'Name': p['name'],
                'Location': p['location'],
                'Production': 0,
                'Percentage': 0
            }]

            self.model.df = self.model.df.append(pd.DataFrame(to_add), ignore_index=True)
            self.model.rowsInserted.emit(self.model.index(self.model.rowCount(), 0),
                                         self.model.rowCount(),
                                         self.model.rowCount())
        self.update_percentages()

        recipe_item = {
            'function': 'add_alternative_exchanges',
            'args': [],
            'kwargs': {}
        }
        print(recipe_item)
        self.recipe_section.append(recipe_item)

    def setup_confirmation(self):

        fp = FuturaRecipePrettifier(findMainWindow().loader)

        self.marketLabel.setText("{} ({}) [{}]".format(self.market.market['name'],
                                                       self.market.market['unit'],
                                                       self.market.market['location']))
        confirm_text = ""
        for e in self.recipe_section:
            confirm_text += fp.format(e)
            confirm_text += "\n"

        self.actionLabel.setText(confirm_text)
        print('please confirm')















