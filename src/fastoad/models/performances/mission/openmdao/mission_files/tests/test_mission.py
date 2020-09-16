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
from collections import OrderedDict

from ..mission import Mission

DATA_FOLDER_PATH = pth.join(pth.dirname(__file__), "data")


def test_inputs():
    mission_definition = OrderedDict(
        {
            "phase_definitions": OrderedDict(
                {
                    "initial_climb_phase": OrderedDict(
                        {
                            "engine_setting": "takeoff",
                            "polar": "data:aerodynamics:aircraft:takeoff",
                            "thrust_rate": "data:mission:sizing:climb:thrust_rate",
                            "steps": [
                                OrderedDict(
                                    {
                                        "step": "climb",
                                        "target": OrderedDict(
                                            {
                                                "altitude": OrderedDict(
                                                    {"value": "400", "unit": "ft"}
                                                ),
                                                "equivalent_airspeed": OrderedDict(
                                                    {"value": "constant"}
                                                ),
                                            },
                                        ),
                                    }
                                ),
                                OrderedDict(
                                    {
                                        "step": "acceleration",
                                        "target": OrderedDict(
                                            {
                                                "equivalent_airspeed": "initial_climb:final_equivalent_airspeed",
                                            }
                                        ),
                                    }
                                ),
                                OrderedDict(
                                    {
                                        "step": "climb",
                                        "polar": "data:aerodynamics:aircraft:low_speed",
                                        "target": OrderedDict(
                                            {
                                                "altitude": "initial_climb:final_altitude",
                                                "equivalent_airspeed": OrderedDict(
                                                    {"value": "constant"}
                                                ),
                                            }
                                        ),
                                    }
                                ),
                            ],
                        }
                    ),
                }
            ),
        }
    )

    print(mission_definition)
    mission = Mission(mission_definition)

    mission.find_inputs()

    assert mission._inputs == {
        "data:aerodynamics:aircraft:takeoff:CL": None,
        "data:aerodynamics:aircraft:takeoff:CD": None,
        "data:mission:sizing:climb:thrust_rate": None,
        "data:aerodynamics:aircraft:low_speed:CL": None,
        "data:aerodynamics:aircraft:low_speed:CD": None,
        "initial_climb:final_altitude": "m",
        "initial_climb:final_equivalent_airspeed": "m/s",
    }
