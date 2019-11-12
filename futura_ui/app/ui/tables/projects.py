# -*- coding: utf-8 -*-
#from bw2data import projects
import brightway2 as bw
from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import QThread
from ...signals import signals


class ProjectListWidget(QComboBox):
    def __init__(self):
        super(ProjectListWidget, self).__init__()

        self.connect_signals()
        self.project_names = None
        self.sync()
        self.databases = {}
        for obj in self.project_names:
            bw.projects.set_current(obj, update=False, writable=False)
            self.databases[obj] = [x for x in bw.databases]

    def connect_signals(self):

        self.activated.connect(self.on_activated)
        #self.currentIndexChanged.connect(self.on_activated)
        # signals.project_selected.connect(self.sync)
        # signals.projects_changed.connect(self.sync)

    def sync(self):
        self.clear()
        self.project_names = sorted([project.name for project in bw.projects])
        self.addItems(self.project_names)
        index = self.project_names.index(bw.projects.current)
        self.setCurrentIndex(index)

    def on_activated(self, index):
        #pass
        project = self.project_names[index]
        print(project)
        print(self.databases[project])
        #bw.projects.set_current(self.project_names[index], update=False, writable=False)

        signals.change_project.emit(self.project_names[index])
