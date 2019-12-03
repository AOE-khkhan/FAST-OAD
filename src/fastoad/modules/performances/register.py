"""
Component registration
"""
#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2019  ONERA/ISAE
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from fastoad.module_management.openmdao_system_factory import OpenMDAOSystemFactory
from fastoad.modules.performances.breguet import BreguetFromOWE
from . import BreguetFromMTOW

OpenMDAOSystemFactory.register_system(BreguetFromMTOW,
                                      'fastoad.performances.breguet.from_mtow')
OpenMDAOSystemFactory.register_system(BreguetFromOWE,
                                      'fastoad.performances.breguet.from_owe')
