from futura_ui.app import Application
from PySide2.QtCore import Qt
import pytest


#@pytest.fixture(scope='session', autouse=True)
def test_futura_ui(qtbot):
    app = Application()
    app.show()
    qtbot.addWidget(app)

    assert 1
    #print(app.main_window.left_panel.widget_layout.itemAt(0).widget())
    #qtbot.mouseClick(app.main_window.left_panel.widget_layout.itemAt(0).widget().newButton, Qt.LeftButton)

