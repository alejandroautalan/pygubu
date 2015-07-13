import sys
import importlib
import logging
import argparse

# Setup logging level
parser = argparse.ArgumentParser()
parser.add_argument('filename', nargs='?')
parser.add_argument('--loglevel')
args = parser.parse_args()

loglevel = str(args.loglevel).upper()
loglevel = getattr(logging, loglevel, logging.WARNING)
logging.basicConfig(level=loglevel)
logger = logging.getLogger(__name__)


def check_dependency(modulename, version, help_msg=None):
    try:
        module = importlib.import_module(modulename)        
        module_version = "<unknown>"
        for attr in ('version', '__version__', 'ver', 'PYQT_VERSION_STR'):
            v = getattr(module, attr, None)
            if v is not None:
                module_version = v
        msg = "Module {0} imported ok, version {1}"
        logger.info(msg.format(modulename, module_version))
    except ImportError as e:
        msg = """I can't import module "{module}". You need to have installed '{module}' version {version} or higher. {help}"""
        if help_msg is None:
            help_msg = ''
        msg = msg.format(module=modulename, version=version, help=help_msg)
        logger.error(msg)
        sys.exit(-1)

#
# Dependency check
#
help = "Hint, If your are using Debian, install package python3-appdirs."
if sys.version_info < (3,):
    help = "Hint, If your are using Debian, install package python-appdirs."

check_dependency('appdirs', '1.3', help)

