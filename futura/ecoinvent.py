from bw2data import projects, databases


def check_database(project_name, database):

    if project_name in projects:
        current = projects.current
        projects.set_current(project_name)
        check = database in databases
        projects.set_current(current)

        return check

    else:
        return False
