from eidl import EcoinventDownloader
from .storage import storage
import brightway2 as bw2


def check_database(project_name, database):

    if project_name in bw2.projects:
        current = bw2.projects.current
        bw2.projects.set_current(project_name)
        check = database in bw2.databases
        bw2.projects.set_current(current)

        return check

    else:
        return False
