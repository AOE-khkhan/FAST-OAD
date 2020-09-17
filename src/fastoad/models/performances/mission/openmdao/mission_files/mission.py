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

from fastoad.base.flight_point import FlightPoint
from fastoad.models.propulsion import IPropulsion
from .schema import (
    PHASE_DEFINITIONS_TAG,
    ROUTE_DEFINITIONS_TAG,
    STEP_TAG,
    STEPS_TAG,
    BaseStepNames,
    load_mission_file,
    RANGE_STEP_TAG,
    MISSION_DEFINITION_TAG,
)
from ...flight.base import RangedFlight, SimpleFlight
from ....mission.base import FlightSequence

BASE_UNITS = {"altitude": "m", "true_airspeed": "m/s", "equivalent_airspeed": "m/s", "range": "m"}


class Mission:
    def __init__(
        self, mission_definition: Union[dict, str], propulsion: IPropulsion, reference_area: float
    ):
        self._base_kwargs = {"reference_area": reference_area, "propulsion": propulsion}
        self._input_map = {}

        if isinstance(mission_definition, str):
            self._mission_definition = load_mission_file(mission_definition)
        else:
            self._mission_definition = mission_definition
        self._inputs = {}
        self._outputs = {}
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

    def find_outputs(self):
        mission_name = self._mission_definition[MISSION_DEFINITION_TAG]["name"]
        for route_name, definition in self._mission_definition[ROUTE_DEFINITIONS_TAG].items():
            for step_definition in definition[STEPS_TAG]:
                if STEP_TAG in step_definition:
                    phase_name = step_definition[STEP_TAG]
                else:
                    phase_name = "cruise"
                var_name_root = "data:mission:%s:%s:%s:" % (mission_name, route_name, phase_name)
                self._outputs[var_name_root + "duration"] = "s"
                self._outputs[var_name_root + "fuel"] = "kg"
                self._outputs[var_name_root + "distance"] = "m"

    def build_phases(self, inputs: Mapping):
        for phase_name, definition in self._mission_definition[PHASE_DEFINITIONS_TAG].items():
            phase = FlightSequence()
            kwargs = {name: value for name, value in definition.items() if name != STEPS_TAG}
            kwargs["name"] = phase_name

            for step_definition in definition[STEPS_TAG]:
                segment_class = BaseStepNames.get_segment_class(step_definition[STEP_TAG])
                step_kwargs = kwargs.copy()
                step_kwargs.update(
                    {name: value for name, value in step_definition.items() if name != STEP_TAG}
                )
                step_kwargs.update(self._base_kwargs)

                for key, value in step_kwargs.items():
                    if key == "target":
                        for target_key, target_value in value.items():
                            if isinstance(target_value, dict) and "value" in target_value:
                                value[target_key] = om.convert_units(
                                    target_value["value"],
                                    target_value.get("unit"),
                                    BASE_UNITS.get(target_key),
                                )
                        step_kwargs[key] = FlightPoint(**value)
                    elif isinstance(value, str) and ":" in value:
                        step_kwargs[key] = inputs[value]
                    else:
                        step_kwargs[key] = value

                segment = segment_class(**step_kwargs)
                phase.flight_sequence.append(segment)
            self._phases[phase_name] = phase

    def build_routes(self, inputs):
        for route_name, definition in self._mission_definition[ROUTE_DEFINITIONS_TAG].items():
            climb_phases = []
            descent_phases = []
            climb = True
            for step_definition in definition[STEPS_TAG]:
                if STEP_TAG in step_definition:
                    if climb:
                        climb_phases.append(self._phases[step_definition[STEP_TAG]])
                    else:
                        descent_phases.append(self._phases[step_definition[STEP_TAG]])
                else:
                    # Schema ensures there is one and only one RANGE_STEP_TAG
                    cruise_phase = self._phases[step_definition[RANGE_STEP_TAG]]

            sequence = SimpleFlight(0.0, climb_phases, cruise_phase, descent_phases)
            flight_range = definition["range"]
            if isinstance(flight_range, str):
                flight_range = inputs[definition["range"]]
            self._routes[route_name] = RangedFlight(sequence, flight_range)

    def build_mission(self):
        pass
