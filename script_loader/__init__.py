""" 
    Script Loader - 轻量级插件托盘 for OlivOS
    Copyright (C) 2022  Rainy Zhou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
