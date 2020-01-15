import logging
import wrapt
from .proxy import WurstProcess

from .plugin_loader import load_plugins

# import wurst
import wurst
import futura.wurst_monkeypatch as wmp
#do monkeypatching here

wurst.relink_technosphere_exchanges = wmp.relink_technosphere_exchanges
wurst.transformations.relink_technosphere_exchanges = wmp.relink_technosphere_exchanges
wurst.transformations.geo.relink_technosphere_exchanges = wmp.relink_technosphere_exchanges
wurst.transformations.geo.allocate_inputs = wmp.allocate_inputs

@wrapt.decorator
def return_WurstProcess(wrapped, instance, args, kwargs):
    return WurstProcess(wrapped(*args, **kwargs))


wurst.get_one = return_WurstProcess(wurst.get_one)
wurst.searching.get_one = return_WurstProcess(wurst.searching.get_one)

#create w alias for wurst
w = wurst


# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=r'C:\temp\futura.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger1 = logging.getLogger('futura')


def log(MESSAGE, *args, **kwargs):
    logger1.info(MESSAGE, *args, **kwargs)


def warn(MESSAGE, *args, **kwargs):
    logger1.warning(MESSAGE, *args, **kwargs)


warn('Futura is using a monkeypatched version of Wurst')

load_plugins()
