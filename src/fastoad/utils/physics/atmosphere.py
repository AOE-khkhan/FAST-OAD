"""
Simple implementation of International Standard Atmosphere
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

from numbers import Number
from typing import Union, Sequence

import numpy as np
from scipy.constants import atmosphere, R

AIR_MOLAR_MASS = 28.9647e-3
AIR_GAS_CONSTANT = R / AIR_MOLAR_MASS
SEA_LEVEL_PRESSURE = atmosphere
SEA_LEVEL_TEMPERATURE = 288.15
TROPOPAUSE = 11000


class Atmosphere:
    """
    Simple implementation of International Standard Atmosphere
    for troposphere and stratosphere.

    Atmosphere properties a provided in the same "shape" as provided
    altitude:
     - if altitude is given as a float, returned values will be floats
     - if altitude is given as a sequence (list, 1D numpy array, ...), returned
       values will be 1D numpy arrays
     - if altitude is given as nD numpy array, returned values will be nD numpy
       arrays

    Usage:

    .. code-block::

        >>> pressure = Atmosphere(30000).pressure # pressure at 30,000 feet, dISA = 0 K
        >>> density = Atmosphere(5000, 10).density # density at 5,000 feet, dISA = 10 K


        >>> atm = Atmosphere(np.arange(0,10001,1000, 15)) # init for alt. 0 to 10,000, dISA = 15K
        >>> temperatures = atm.pressure # pressures for all defined altitudes
        >>> viscosities = atm.kinematic_viscosity # viscosities for all defined altitudes

    :param altitude: altitude in foots
    :param delta_t: temperature increment applied to whole temperature profile
    """

    # pylint: disable=too-many-instance-attributes  # Needed for avoiding redoing computations
    def __init__(self, altitude: Union[float, Sequence], delta_t: float = 0.):

        self._delta_t = delta_t

        # Floats will be provided as output if altitude is a scalar
        self._float_expected = isinstance(altitude, Number)

        # For convenience, let's have altitude as numpy arrays in all cases
        if not isinstance(altitude, np.ndarray):
            self._altitude = np.array(altitude)
        else:
            self._altitude = altitude

        self._out_shape = self._altitude.shape

        # Sets indices for tropopause
        self._idx_tropo = self._altitude < TROPOPAUSE
        self._idx_strato = self._altitude >= TROPOPAUSE

        # Outputs
        self._temperature = None
        self._pressure = None
        self._density = None
        self._speed_of_sound = None
        self._kinematic_viscosity = None

    @property
    def temperature(self):
        """ Temperature in K """
        if self._temperature is None:
            self._temperature = np.zeros(self._out_shape)
            self._temperature[self._idx_tropo] = SEA_LEVEL_TEMPERATURE - 0.0065 \
                                                 * self._altitude[self._idx_tropo] \
                                                 + self._delta_t
            self._temperature[self._idx_strato] = 216.65 + self._delta_t
        return self._return_value(self._temperature)

    @property
    def pressure(self):
        """ Pressure in Pa """
        if self._pressure is None:
            self._pressure = np.zeros(self._out_shape)
            self._pressure[self._idx_tropo] = \
                SEA_LEVEL_PRESSURE * (1 -
                                      (self._altitude[self._idx_tropo] / 44330.78)) ** 5.25587611
            self._pressure[self._idx_strato] = \
                22632 * 2.718281 ** (1.7345725 - 0.0001576883 * self._altitude[self._idx_strato])
        return self._return_value(self._pressure)

    @property
    def density(self):
        """ Density in kg/m3 """
        if self._density is None:
            self._density = self.pressure / AIR_GAS_CONSTANT / self.temperature
        return self._return_value(self._density)

    @property
    def speed_of_sound(self):
        """ Speed of sound in m/s """
        if self._speed_of_sound is None:
            self._speed_of_sound = (1.4 * AIR_GAS_CONSTANT * self.temperature) ** 0.5
        return self._return_value(self._speed_of_sound)

    @property
    def kinematic_viscosity(self):
        """ Kinematic viscosity in m2/s """
        if self._kinematic_viscosity is None:
            self._kinematic_viscosity = ((0.000017894 *
                                          (self.temperature / SEA_LEVEL_TEMPERATURE) ** (3 / 2))
                                         * ((SEA_LEVEL_TEMPERATURE + 110.4) /
                                             (self.temperature + 110.4))
                                         ) / self.density
        return self._return_value(self._kinematic_viscosity)

    def get_unitary_reynolds(self, mach):
        """
        :param mach: Mach number
        :return: Unitary Reynolds number in 1/m
        """
        return mach * self.speed_of_sound / self.kinematic_viscosity

    def _return_value(self, value):
        """
        :returns: a float when needed. Otherwise, returns the value itself.
        """
        if self._float_expected:
            return float(value)

        return value
