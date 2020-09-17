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

from ..mission import Mission

DATA_FOLDER_PATH = pth.join(pth.dirname(__file__), "data")


def test_inputs():
    mission = Mission(pth.join(DATA_FOLDER_PATH, "phases.yml"))
    mission.find_inputs()
    assert mission._inputs == {
        "data:aerodynamics:aircraft:low_speed:CD": None,
        "data:aerodynamics:aircraft:low_speed:CL": None,
        "data:aerodynamics:aircraft:takeoff:CD": None,
        "data:aerodynamics:aircraft:takeoff:CL": None,
        "data:mission:sizing:climb:thrust_rate": None,
        "initial_climb:final_altitude": "m",
        "initial_climb:final_equivalent_airspeed": "m/s",
    }

    mission = Mission(pth.join(DATA_FOLDER_PATH, "mission.yml"))
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
    mission = Mission(pth.join(DATA_FOLDER_PATH, "phases.yml"))
    mission.find_inputs()

    inputs = {
        "data:aerodynamics:aircraft:low_speed:CD": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:low_speed:CL": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:takeoff:CD": [0.0, 0.5, 1.0],
        "data:aerodynamics:aircraft:takeoff:CL": [0.0, 0.5, 1.0],
        "data:mission:sizing:climb:thrust_rate": 0.6,
        "initial_climb:final_altitude": 500,
        "initial_climb:final_equivalent_airspeed": 130.0,
    }
    mission.build_phases(inputs)
