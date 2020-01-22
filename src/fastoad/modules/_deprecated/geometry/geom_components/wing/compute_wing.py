"""
    Estimation of wing geometry
"""

#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA/ISAE
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

from openmdao.api import Group

from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeB50
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeCLalpha
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeL1AndL4Wing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeL2AndL3Wing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeMACWing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeMFW
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeSweepWing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeToCWing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeWetAreaWing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeXWing
from fastoad.modules._deprecated.geometry.geom_components.wing.components import ComputeYWing


class ComputeWingGeometry(Group):
    # TODO: Document equations. Cite sources
    """ Wing geometry estimation """

    def setup(self):
        self.add_subsystem('y_wing', ComputeYWing(), promotes=['*'])
        self.add_subsystem('l14_wing',
                           ComputeL1AndL4Wing(), promotes=['*'])
        self.add_subsystem('l2l3_wing',
                           ComputeL2AndL3Wing(), promotes=['*'])
        self.add_subsystem('x_wing', ComputeXWing(), promotes=['*'])
        self.add_subsystem('mac_wing', ComputeMACWing(), promotes=['*'])
        self.add_subsystem('b50_wing', ComputeB50(), promotes=['*'])
        self.add_subsystem('sweep_wing',
                           ComputeSweepWing(), promotes=['*'])
        self.add_subsystem('toc_wing', ComputeToCWing(), promotes=['*'])
        self.add_subsystem('wetarea_wing',
                           ComputeWetAreaWing(), promotes=['*'])
        self.add_subsystem('clapha_wing', ComputeCLalpha(), promotes=['*'])
        self.add_subsystem('mfw', ComputeMFW(), promotes=['*'])