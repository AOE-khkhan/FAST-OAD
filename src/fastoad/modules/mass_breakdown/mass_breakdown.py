"""
Main components for mass breakdown
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

import openmdao.api as om

from fastoad.modules.mass_breakdown.a_airframe import WingWeight, FuselageWeight, EmpennageWeight, \
    FlightControlsWeight, LandingGearWeight, PylonsWeight, PaintWeight
from fastoad.modules.mass_breakdown.b_propulsion import EngineWeight, FuelLinesWeight, \
    UnconsumablesWeight
from fastoad.modules.mass_breakdown.c_systems import PowerSystemsWeight, LifeSupportSystemsWeight, \
    NavigationSystemsWeight, TransmissionSystemsWeight, FixedOperationalSystemsWeight, \
    FlightKitWeight
from fastoad.modules.mass_breakdown.cs25 import Loads
from fastoad.modules.mass_breakdown.d_furniture import CargoConfigurationWeight, \
    PassengerSeatsWeight, FoodWaterWeight, SecurityKitWeight, ToiletsWeight
from fastoad.modules.mass_breakdown.e_crew import CrewWeight
from fastoad.modules.mass_breakdown.options import OpenMdaoOptionDispatcherGroup, \
    ENGINE_LOCATION_OPTION, TAIL_TYPE_OPTION, AIRCRAFT_TYPE_OPTION
from fastoad.modules.mass_breakdown.update_mlw_and_mzfw import UpdateMLWandMZFW


class MassBreakdown(OpenMdaoOptionDispatcherGroup):
    """
    The top group for solving mass breakdown
    """

    def initialize(self):
        # TODO: Manage options through constants or enums
        self.options.declare(ENGINE_LOCATION_OPTION, types=float, default=1.0)
        self.options.declare(TAIL_TYPE_OPTION, types=float, default=0.)
        self.options.declare(AIRCRAFT_TYPE_OPTION, types=float, default=2.0)

    def setup(self):
        self.add_subsystem('owe', OperatingWeightEmpty(), promotes=['*'])
        self.add_subsystem('update_mzfw_and_mlw', UpdateMLWandMZFW(), promotes=['*'])

    def configure(self):
        super(MassBreakdown, self).configure()

        # Solvers setup
        self.nonlinear_solver = om.NonlinearBlockGS()
        self.nonlinear_solver.options['iprint'] = 0
        self.nonlinear_solver.options['maxiter'] = 50
        self.linear_solver = om.LinearBlockGS()
        self.linear_solver.options['iprint'] = 0


class OperatingWeightEmpty(OpenMdaoOptionDispatcherGroup):
    """ Operating Empty Weight (OEW) estimation

    This group aggregates weight from all components of the aircraft.
    """

    def initialize(self):
        # TODO: Manage options through constants or enums
        self.options.declare(ENGINE_LOCATION_OPTION, types=float, default=1.0)
        self.options.declare(TAIL_TYPE_OPTION, types=float, default=0.)
        self.options.declare(AIRCRAFT_TYPE_OPTION, types=float, default=2.0)

    def setup(self):
        # Airframe
        self.add_subsystem('loads', Loads(), promotes=['*'])
        self.add_subsystem('wing_weight', WingWeight(), promotes=['*'])
        self.add_subsystem('fuselage_weight', FuselageWeight(), promotes=['*'])
        self.add_subsystem('empennage_weight', EmpennageWeight(), promotes=['*'])
        self.add_subsystem('flight_controls_weight', FlightControlsWeight(), promotes=['*'])
        self.add_subsystem('landing_gear_weight', LandingGearWeight(), promotes=['*'])
        # Engine have to be computed before pylons
        self.add_subsystem('engines_weight', EngineWeight(), promotes=['*'])
        self.add_subsystem('pylons_weight', PylonsWeight(), promotes=['*'])
        self.add_subsystem('paint_weight', PaintWeight(), promotes=['*'])
        # Propulsion
        self.add_subsystem('fuel_lines_weight', FuelLinesWeight(), promotes=['*'])
        self.add_subsystem('unconsumables_weight', UnconsumablesWeight(), promotes=['*'])
        # Systems
        self.add_subsystem('power_systems_weight', PowerSystemsWeight(), promotes=['*'])
        self.add_subsystem('life_support_systems_weight', LifeSupportSystemsWeight(),
                           promotes=['*'])
        self.add_subsystem('navigation_systems_weight', NavigationSystemsWeight(), promotes=['*'])
        self.add_subsystem('transmission_systems_weight', TransmissionSystemsWeight(),
                           promotes=['*'])
        self.add_subsystem('fixed_operational_systems_weight', FixedOperationalSystemsWeight(),
                           promotes=['*'])
        self.add_subsystem('flight_kit_weight', FlightKitWeight(), promotes=['*'])
        # Cargo and furniture
        self.add_subsystem('cargo_configuration_weight', CargoConfigurationWeight(), promotes=['*'])
        self.add_subsystem('passenger_seats_weight', PassengerSeatsWeight(), promotes=['*'])
        self.add_subsystem('food_water_weight', FoodWaterWeight(), promotes=['*'])
        self.add_subsystem('security_kit_weight', SecurityKitWeight(), promotes=['*'])
        self.add_subsystem('toilets_weight', ToiletsWeight(), promotes=['*'])
        # Crew
        self.add_subsystem('crew_weight', CrewWeight(), promotes=['*'])

        # Make additions
        self.add_subsystem('airframe_weight_sum',
                           om.AddSubtractComp('weight:airframe:mass',
                                              ['weight:airframe:wing:mass',
                                               'weight:airframe:fuselage:mass',
                                               'weight:airframe:tail_plane:horizontal:mass',
                                               'weight:airframe:tail_plane:vertical:mass',
                                               'weight:airframe:flight_controls:mass',
                                               'weight:airframe:landing_gear:main:mass',
                                               'weight:airframe:landing_gear:front:mass',
                                               'weight:airframe:pylon:mass',
                                               'weight:airframe:paint:mass'],
                                              units='kg',
                                              desc='Mass of airframe'),
                           promotes=['*']
                           )

        self.add_subsystem('propulsion_weight_sum',
                           om.AddSubtractComp('weight:propulsion:mass',
                                              ['weight:propulsion:engine:mass',
                                               'weight:propulsion:fuel_lines:mass',
                                               'weight:propulsion:unconsumables:mass'],
                                              units='kg',
                                              desc='Mass of the propulsion system'),
                           promotes=['*']
                           )

        self.add_subsystem('systems_weight_sum',
                           om.AddSubtractComp('weight:systems:mass',
                                              ['weight:systems:power:auxiliary_power_unit:mass',
                                               'weight:systems:power:electric_systems:mass',
                                               'weight:systems:power:hydraulic_systems:mass',
                                               'weight:systems:life_support:insulation:mass',
                                               'weight:systems:life_support:air_conditioning:mass',
                                               'weight:systems:life_support:de-icing:mass',
                                               'weight:systems:life_support:cabin_lighting:mass',
                                               'weight:systems:life_support:seats_crew_accomodation:mass',
                                               'weight:systems:life_support:oxygen:mass',
                                               'weight:systems:life_support:safety_equipment:mass',
                                               'weight:systems:navigation:mass',
                                               'weight:systems:transmission:mass',
                                               'weight:systems:operational:radar:mass',
                                               'weight:systems:operational:cargo_hold:mass',
                                               'weight:systems:flight_kit:mass'],
                                              units='kg',
                                              desc='Mass of aircraft systems'),
                           promotes=['*']
                           )

        self.add_subsystem('furniture_weight_sum',
                           om.AddSubtractComp('weight:furniture:mass',
                                              ['weight:furniture:cargo_configuration:mass',
                                               'weight:furniture:passenger_seats:mass',
                                               'weight:furniture:food_water:mass',
                                               'weight:furniture:security_kit:mass',
                                               'weight:furniture:toilets:mass'],
                                              units='kg',
                                              desc='Mass of aircraft furniture'),
                           promotes=['*']
                           )

        self.add_subsystem('OWE_sum',
                           om.AddSubtractComp('weight:aircraft:OWE',
                                              ['weight:airframe:mass',
                                               'weight:propulsion:mass',
                                               'weight:systems:mass',
                                               'weight:furniture:mass',
                                               'weight:crew:mass'],
                                              units='kg',
                                              desc='Mass of crew'),
                           promotes=['*']
                           )
