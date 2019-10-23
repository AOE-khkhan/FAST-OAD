"""
    FAST - Copyright (c) 2016 ONERA ISAE
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

import numpy as np
from openmdao.core.explicitcomponent import ExplicitComponent

from fastoad.modules.aerodynamics.constants import POLAR_POINT_COUNT


class InitializeClPolar(ExplicitComponent):

    def initialize(self):
        self.options.declare('low_speed_aero', default=False, types=bool)

    def setup(self):
        self.low_speed_aero = self.options['low_speed_aero']

        self.add_input('kfactors_aero:K_Cl', val=np.nan)
        self.add_input('kfactors_aero:Offset_Cl', val=np.nan)
        self.add_input('kfactors_aero:K_winglet_Cl', val=np.nan)
        self.add_input('kfactors_aero:Offset_winglet_Cl', val=np.nan)

        nans_array = np.full(POLAR_POINT_COUNT, np.nan)
        if self.low_speed_aero:
            self.add_output('cl_low_speed', shape=POLAR_POINT_COUNT)
        else:
            self.add_output('cl_high_speed', shape=POLAR_POINT_COUNT)

    def compute(self, inputs, outputs):
        k_cl = inputs['kfactors_aero:K_Cl']
        offset_cl = inputs['kfactors_aero:Offset_Cl']
        k_winglet_cl = inputs['kfactors_aero:K_winglet_Cl']
        offset_winglet_cl = inputs['kfactors_aero:Offset_winglet_Cl']

        # FIXME: initialization of CL range should be done more directly, without these coefficients
        cl = np.arange(0., 1.5, 0.01) * k_cl * k_winglet_cl + offset_cl + offset_winglet_cl

        if self.low_speed_aero:
            outputs['cl_low_speed'] = cl
        else:
            outputs['cl_high_speed'] = cl
