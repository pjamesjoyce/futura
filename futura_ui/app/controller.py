# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtCore
import os

from .settings import futura_settings # , project_settings
from .signals import signals
from .ui.dialogs.progress import UndefinedProgress

from .wrappers import FuturaGuiLoader

from .utils import findMainWindow
from .ui.dialogs.new_recipe import NewRecipeDialog
from .ui.widgets.filter import FilterListerWidget, parse_filter_widget, FilterListerDialog
from .ui.wizards import RegionalisationWizard

from futura.utils import create_filter_from_description
from futura import w
from futura.regionalisation import create_regional_activities


class Controller(object):
    """The Controller is a central object in the Activity Browser. It groups methods that may be required in different
    parts of the AB to access, modify, or delete:
    - settings
    - projects
    - databases
    - calculation setups
    - activities/exchanges
    It is different from bwutils in that it also contains Qt elements such as dialogs.
    - """


    def __init__(self):
        self.connect_signals()              # connect the signals the app requires - this is what the app does
        self.load_settings()                # load settings
        self.db_wizard = None               # create an attribute for the db_wizard

    def connect_signals(self):
        # Note - these need to be set up in the signals file too

        # Recipes

        signals.new_recipe.connect(self.new_recipe)
        signals.load_recipe.connect(self.load_recipe)
        signals.test_filter.connect(self.test_filter)
        signals.regionalisation_wizard.connect(self.regionalisation_wizard)

    # SETTINGS
    def load_settings(self):
        if futura_settings.settings:
            print("Loading user settings:")
            # self.switch_brightway2_dir_path(dirpath=futura_settings.custom_bw_dir)
            # self.change_project(futura_settings.startup_project)

    # Specific functions to do things go here, within the controller class

    def new_recipe(self):

        new_recipe_dialog = NewRecipeDialog()

        if new_recipe_dialog.exec_():

            print('Creating a new, blank recipe')
            findMainWindow().loader = FuturaGuiLoader()

            name = new_recipe_dialog.name.text()
            ecoinvent_version = new_recipe_dialog.ecoinvent_version.currentText()
            ecoinvent_system_model = new_recipe_dialog.ecoinvent_system_model.currentText()
            description = new_recipe_dialog.description.toPlainText()

            findMainWindow().loader.recipe = {
                'metadata': {
                    'output_database': name,
                    'ecoinvent_version': ecoinvent_version,
                    'ecoinvent_system_model': ecoinvent_system_model,
                    'description': description
                },
            }

            signals.update_recipe.emit()
            signals.show_recipe_actions.emit()

        else:
            print('Cancelling')

    def load_recipe(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None,
                                                            'Choose a recipe file...',
                                                            #os.path.join(os.path.expanduser('~'), 'Documents'),
                                                            r'C:\Users\pjjoyce\Dropbox\00_My_Software',
                                                            "Recipe Files (*.yml *.yaml)")
        print(filename)
        if filename:

            #progress = UndefinedProgress()

            #signals.show_undefined_progress.emit()

            findMainWindow().loader = FuturaGuiLoader(filename, autocreate=True)
            signals.update_recipe.emit()
            signals.show_recipe_actions.emit()

            #signals.close_undefined_progress.emit()

    def test_filter(self):

        x = self.get_filter()

        print(x)

    def get_filter(self):

        filter_dialog = FilterListerDialog()

        if filter_dialog.exec_():
            return parse_filter_widget(filter_dialog.filter_widget)
        else:
            return

    def regionalisation_wizard(self):
        print('Starting the wizard')
        rw = RegionalisationWizard()

        if rw.exec_():
            print('Wizard Complete')
            filter_description = parse_filter_widget(rw.filter_widget)
            print(filter_description)
            this_filter = create_filter_from_description(filter_description)
            db = findMainWindow().loader.database.db
            this_item = w.get_one(db, *this_filter)
            print(this_item)
            create_regional_activities(this_item, ['GB', 'DE'], db)
            no_location_filter_description = [x for x in filter_description if x['args'][0] != 'location']
            no_location_filter = create_filter_from_description(no_location_filter_description)
            result = list(w.get_many(db, *no_location_filter))
            print(result)

        else:
            print('Wizard Cancelled')



