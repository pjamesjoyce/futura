# -*- coding: utf-8 -*-
from PySide2.QtCore import QObject, Signal


class Signals(QObject):
    """ Signals used for the Activity Browser should be defined here.
    While arguments can be passed to signals, it is good practice not to do this if possible. """

    # Change action display
    show_load_actions = Signal()
    show_recipe_actions = Signal()
    update_recipe = Signal()

    # Recipes

    new_recipe = Signal()
    load_recipe = Signal()

    # Progress
    show_undefined_progress = Signal()
    close_undefined_progress = Signal()
    show_defined_progress = Signal()
    close_defined_progress = Signal()
    set_defined_progress_value = Signal(int)

    thread_progress = Signal(int)

    start_status_progress = Signal(int)
    update_status_progress = Signal(int)
    hide_status_progress = Signal()

    change_status_message = Signal(str)
    reset_status_message = Signal()

    # Filters

    test_filter = Signal()

    # Regionalisation

    regionalisation_wizard = Signal()

    # Recipes

    export_recipe = Signal()

    # Technology

    add_technology_file = Signal()




signals = Signals()
