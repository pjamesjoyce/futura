from futura.sectors import *
from futura.wrappers import WurstDatabase
import pickle
import brightway2 as bw2

#wd = WurstDatabase('Prospective_LCA_1', 'ecoinvent')
saved_file = r"C:\Users\pjjoyce\Documents\00_HOME\futura\save.p"
wd = pickle.load(open(saved_file, "rb"))

bw2.projects.set_current(wd.project_name)
wd.bwdb = bw2.Database(wd.database_name)

bw_glo_elec = wd.bwdb.search('market group electricity high voltage GLO')[0]

bw_cement_europe = wd.bwdb.search('market portland cement Europe without Switzerland')[0]
bw_cement_US = wd.bwdb.search('market cement Portland US')[0]

ELECTRICITY_TREE = [build_tree(bw_glo_elec, filters=electricity_markets)]
CEMENT_TREE = [build_tree(bw_cement_europe, filters=cement_filter),
               build_tree(bw_cement_US, filters=cement_filter),]


TREE_DATA = {'Electricity': ELECTRICITY_TREE,
             'Cement': CEMENT_TREE,
             'Aluminium': {},
             'Steel': {},
             'Lithium': {},
             'Glass': {}
             }