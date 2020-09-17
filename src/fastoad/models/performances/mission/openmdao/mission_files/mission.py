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

from typing import Mapping, Union

import openmdao.api as om

from .schema import (
    PHASE_DEFINITIONS_TAG,
    STEPS_TAG,
    BaseStepNames,
    STEP_TAG,
    load_mission_file,
)
from ....mission.base import FlightSequence

BASE_UNITS = {"altitude": "m", "true_airspeed": "m/s", "equivalent_airspeed": "m/s", "range": "m"}


class Mission:
    def __init__(self, mission_definition: Union[dict, str]):
        self._input_map = {}
        if isinstance(mission_definition, str):
            self._mission_definition = load_mission_file(mission_definition)
        else:
            self._mission_definition = mission_definition
        self._inputs = {}
        self._phases = {}
        self._routes = {}
        self._flight = []

    def find_inputs(self, struct=None):
        if not struct:
            struct = self._mission_definition

        if isinstance(struct, dict):
            for key, value in struct.items():
                if isinstance(value, str) and ":" in value:
                    if key == "polar":
                        struct[key] = {"CL": value + ":CL", "CD": value + ":CD"}
                        self.find_inputs(struct[key])
                    else:
                        self._inputs[value] = BASE_UNITS.get(key)
                elif isinstance(value, dict) or isinstance(value, list):
                    self.find_inputs(value)
        elif isinstance(struct, list):
            for value in struct:
                self.find_inputs(value)

    def build_phases(self, inputs: Mapping):
        for phase_name, definition in self._mission_definition[PHASE_DEFINITIONS_TAG].items():
            phase = FlightSequence()
            kwargs = {name: value for name, value in definition.items() if name != STEPS_TAG}

            for step_definition in definition[STEPS_TAG]:
                segment_class = BaseStepNames.get_segment_class(step_definition[STEP_TAG])
                step_kwargs = kwargs.copy()
                step_kwargs.update(
                    {name: value for name, value in step_definition.items() if name != STEP_TAG}
                )

                for key, value in step_kwargs.items():
                    if isinstance(value, dict) and "value" in value:
                        step_kwargs[key] = om.convert_units(
                            value["value"], value.get("unit"), BASE_UNITS.get(key)
                        )
                    elif isinstance(value, str) and ":" in value:
                        step_kwargs[key] = inputs[value]

                segment = segment_class(**step_kwargs)
                phase.flight_sequence.append(segment)
            self._phases[phase_name] = phase

    def build_routes(self):
        pass

    def build_mission(self):
        pass
