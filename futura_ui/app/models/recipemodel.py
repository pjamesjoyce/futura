from PySide2.QtGui import QStandardItemModel, QStandardItem


class RecipeModel(QStandardItemModel):
    def __init__(self):
        super(RecipeModel, self).__init__()
        self.setColumnCount(2)
        self.parentItem = self.invisibleRootItem()

    def parse_recipe(self, recipe):

        self.clear()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['item','detail'])
        self.parentItem = self.invisibleRootItem()

        parentItem = self.parentItem

        def parse(this_dict, parent):
            for k, v in this_dict.items():
                if isinstance(v, dict):
                    item = QStandardItem(str(k))
                    parent.appendRow([item])
                    parse(v, item)

                elif isinstance(v, list):
                    this_item = QStandardItem(str(k))
                    parent.appendRow([this_item])

                    for x in v:
                        if isinstance(x, dict):
                            parse(x, this_item)
                        else:
                            item = QStandardItem(str(k))
                            item_detail = QStandardItem(str(v))
                            this_item.appendRow([item, item_detail])
                else:
                    item = QStandardItem(str(k))
                    item_detail = QStandardItem(str(v))
                    parent.appendRow([item, item_detail])

        parse(recipe, parentItem)
