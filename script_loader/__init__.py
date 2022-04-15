FLAG_HAS_OVODICE = False
try:
    import OlivaDiceCore
    FLAG_HAS_OVODICE = True
except ImportError:
    FLAG_HAS_OVODICE = False

import script_loader.main
import script_loader.script_api
import script_loader.data
import script_loader.other_misc
import script_loader.loader
