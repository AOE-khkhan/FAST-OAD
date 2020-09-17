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

from ..schema import load_mission_file

DATA_FOLDER_PATH = pth.join(pth.dirname(__file__), "data")


def test_schema():
    d = load_mission_file(pth.join(DATA_FOLDER_PATH, "mission.yml"))

    assert d == {
        "phase_definitions": {
            "initial_climb_phase": {
                "engine_setting": "takeoff",
                "polar": "data:aerodynamics:aircraft:takeoff",
                "thrust_rate": "data:mission:sizing:climb:thrust_rate",
                "steps": [
                    {
                        "step": "climb",
                        "target": {
                            "altitude": {"value": 400.0, "unit": "ft"},
                            "equivalent_airspeed": {"value": "constant"},
                        },
                    },
                    {
                        "step": "acceleration",
                        "target": {
                            "equivalent_airspeed": "initial_climb:final_equivalent_airspeed"
                        },
                    },
                    {
                        "step": "climb",
                        "polar": "data:aerodynamics:aircraft:low_speed",
                        "target": {
                            "altitude": "initial_climb:final_altitude",
                            "equivalent_airspeed": {"value": "constant"},
                        },
                    },
                ],
            },
            "climb_phase": {
                "engine_setting": "climb",
                "polar": "data:aerodynamics:aircraft:cruise",
                "thrust_rate": "data:mission:sizing:climb:thrust_rate",
                "steps": [
                    {
                        "step": "climb",
                        "target": {
                            "altitude": {"value": 10000.0, "unit": "ft"},
                            "equivalent_airspeed": {"value": "constant"},
                        },
                    },
                    {
                        "step": "acceleration",
                        "target": {"equivalent_airspeed": {"value": 300.0, "unit": "kn"}},
                    },
                    {
                        "step": "climb",
                        "target": {
                            "equivalent_airspeed": {"value": "constant"},
                            "altitude": {"value": "optimal"},
                        },
                        "maximum_mach": "data:TLAR:cruise_mach",
                    },
                ],
            },
            "descent_phase": {
                "engine_setting": "idle",
                "polar": "data:aerodynamics:aircraft:cruise",
                "thrust_rate": "data:mission:sizing:descent:thrust_rate",
                "steps": [
                    {
                        "step": "descent",
                        "target": {
                            "equivalent_airspeed": {"value": 300.0, "unit": "kn"},
                            "mach": {"value": "constant"},
                        },
                    },
                    {
                        "step": "descent",
                        "target": {
                            "altitude": {"value": 10000.0, "unit": "ft"},
                            "equivalent_airspeed": {"value": "constant"},
                        },
                    },
                    {
                        "step": "deceleration",
                        "target": {"equivalent_airspeed": {"value": 250.0, "unit": "kn"}},
                    },
                    {
                        "step": "descent",
                        "target": {
                            "equivalent_airspeed": {"value": "constant"},
                            "altitude": {"value": 1500.0, "unit": "ft"},
                        },
                    },
                ],
            },
        },
        "route_definitions": {
            "main_route": {
                "range": "data:TLAR:range",
                "steps": [
                    {"step": "initial_climb_phase"},
                    {"step": "climb_phase"},
                    {
                        "range_step": "cruise",
                        "engine_setting": "cruise",
                        "polar": "data:aerodynamics:aircraft:cruise",
                    },
                    {"step": "descent_phase"},
                ],
            },
            "diversion_route": {
                "range": "data:mission:sizing:diversion:distance",
                "steps": [
                    {"step": "climb_phase"},
                    {
                        "range_step": "cruise",
                        "engine_setting": "cruise",
                        "polar": "data:aerodynamics:aircraft:cruise",
                    },
                    {"step": "descent_phase"},
                ],
            },
        },
        "mission": {
            "name": "sizing",
            "steps": [{"step": "main_route"}, {"step": "diversion_route"}],
        },
    }
