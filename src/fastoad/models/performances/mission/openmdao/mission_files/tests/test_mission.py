#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
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

import os.path as pth
from unittest.mock import Mock

import pytest
from scipy.constants import foot

from fastoad.models.propulsion import IPropulsion
from ..mission import Mission
from ....segments.altitude_change import AltitudeChangeSegment
from ....segments.speed_change import SpeedChangeSegment

DATA_FOLDER_PATH = pth.join(pth.dirname(__file__), "data")


def test_inputs():
    mission = Mission(pth.join(DATA_FOLDER_PATH, "phases.yml"), Mock(IPropulsion), 100.0)
    mission.find_inputs()
    assert mission._inputs == {
        "data:TLAR:cruise_mach": None,
        "data:aerodynamics:aircraft:cruise:CD": None,
        "data:aerodynamics:aircraft:cruise:CL": None,
        "data:aerodynamics:aircraft:low_speed:CD": None,
        "data:aerodynamics:aircraft:low_speed:CL": None,
        "data:aerodynamics:aircraft:takeoff:CD": None,
        "data:aerodynamics:aircraft:takeoff:CL": None,
        "data:mission:sizing:climb:thrust_rate": None,
        "data:mission:sizing:descent:thrust_rate": None,
        "initial_climb:final_altitude": "m",
        "initial_climb:final_equivalent_airspeed": "m/s",
    }

    mission = Mission(pth.join(DATA_FOLDER_PATH, "mission.yml"), Mock(IPropulsion), 100.0)
    mission.find_inputs()
    assert mission._inputs == {
        "data:TLAR:cruise_mach": None,
        "data:TLAR:range": "m",
        "data:aerodynamics:aircraft:cruise:CD": None,
        "data:aerodynamics:aircraft:cruise:CL": None,
        "data:aerodynamics:aircraft:takeoff:CD": None,
        "data:aerodynamics:aircraft:takeoff:CL": None,
        "data:mission:sizing:climb:thrust_rate": None,
        "data:mission:sizing:descent:thrust_rate": None,
        "data:mission:sizing:diversion:distance": "m",
    }


def test_build_phase():
    mission = Mission(pth.join(DATA_FOLDER_PATH, "phases.yml"), Mock(IPropulsion), 100.0)
    mission.find_inputs()

    inputs = {
        "data:TLAR:cruise_mach": 0.78,
        "data:aerodynamics:aircraft:cruise:CD": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:cruise:CL": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:low_speed:CD": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:low_speed:CL": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:takeoff:CD": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:takeoff:CL": [0.0, 0.5, 1.0],
        "data:mission:sizing:climb:thrust_rate": 0.9,
        "data:mission:sizing:descent:thrust_rate": 0.5,
        "initial_climb:final_altitude": 500,
        "initial_climb:final_equivalent_airspeed": 130.0,
    }
    mission.build_phases(inputs)

    assert len(mission._phases) == 3
    assert len(mission._phases["initial_climb_phase"].flight_sequence) == 3
    steps = mission._phases["initial_climb_phase"].flight_sequence
    assert isinstance(steps[0], AltitudeChangeSegment)
    assert isinstance(steps[1], SpeedChangeSegment)
    assert isinstance(steps[2], AltitudeChangeSegment)
    assert steps[0].target.altitude == pytest.approx(400 * foot)
    assert steps[0].target.equivalent_airspeed == "constant"
    assert steps[1].target.equivalent_airspeed == "initial_climb:final_equivalent_airspeed"
