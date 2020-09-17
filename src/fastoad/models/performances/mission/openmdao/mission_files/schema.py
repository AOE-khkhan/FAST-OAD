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

from enum import Enum

from ensure import Ensure
from strictyaml import load, Map, MapPattern, Optional, Str, Float, Seq, Any

from ...segments.cruise import CruiseSegment
from ...segments.speed_change import SpeedChangeSegment
from ....mission.segments.altitude_change import AltitudeChangeSegment

RANGE_STEP_TAG = "range_step"
STEPS_TAG = "steps"
STEP_TAG = "step"
FLIGHT_DEFINITION_TAG = "flight"
ROUTE_DEFINITIONS_TAG = "route_definitions"
PHASE_DEFINITIONS_TAG = "phase_definitions"


class BaseStepNames(Enum):
    CLIMB = "climb"
    CRUISE = "cruise"
    DESCENT = "descent"
    ACCELERATION = "acceleration"
    DECELERATION = "deceleration"

    @classmethod
    def string_values(cls):
        return {step.value for step in cls}

    @classmethod
    def get_segment_class(cls, value):
        segments = {
            cls.CLIMB.value: AltitudeChangeSegment,
            cls.DESCENT.value: AltitudeChangeSegment,
            cls.CRUISE.value: CruiseSegment,
            cls.ACCELERATION.value: SpeedChangeSegment,
            cls.DECELERATION.value: SpeedChangeSegment,
        }
        return segments[value]


TARGET_SCHEMA = MapPattern(
    Str(), Str() | Map({"value": Float() | Str(), Optional("unit", default=None): Str()})
)

BASE_STEP_SCHEMA_DICT = {
    Optional("target", default=None): TARGET_SCHEMA,
    Optional("engine_setting", default=None): Str(),
    Optional("polar", default=None): Str(),
    Optional("thrust_rate", default=None): Str() | Float(),
    Optional("time_step", default=None): Float(),
    Optional("steps", default=None): Seq(Any()),
}

STEP_SCHEMA_DICT = {STEP_TAG: Str()}
STEP_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

RANGE_STEP_SCHEMA_DICT = {RANGE_STEP_TAG: Str()}
RANGE_STEP_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

CLIMB_STEP_SCHEMA_DICT = {Optional("maximum_mach", default=None): Str() | Float()}
CLIMB_STEP_SCHEMA_DICT.update(STEP_SCHEMA_DICT)

ROUTE_SCHEMA_DICT = {"range": Str() | Float(), STEPS_TAG: Seq(Any())}

SCHEMA = Map(
    {
        PHASE_DEFINITIONS_TAG: MapPattern(Str(), Map(BASE_STEP_SCHEMA_DICT)),
        ROUTE_DEFINITIONS_TAG: MapPattern(Str(), Map(ROUTE_SCHEMA_DICT)),
        FLIGHT_DEFINITION_TAG: Map({STEPS_TAG: Seq(Map({STEP_TAG: Str()}))}),
    }
)


def load_mission_file(file_path: str) -> dict:
    with open(file_path) as yaml_file:
        content = load(yaml_file.read(), SCHEMA)

    for phase_def in content[PHASE_DEFINITIONS_TAG].keys():
        for step in content[PHASE_DEFINITIONS_TAG][phase_def][STEPS_TAG]:
            Ensure(step.keys()).contains(STEP_TAG)
            Ensure(BaseStepNames.string_values()).contains(step[STEP_TAG])

            if step[STEP_TAG] != "climb":
                step.revalidate(Map(STEP_SCHEMA_DICT))
            else:
                step.revalidate(Map(CLIMB_STEP_SCHEMA_DICT))

    step_names = BaseStepNames.string_values() | set(content[PHASE_DEFINITIONS_TAG].keys())

    for route_def in content[ROUTE_DEFINITIONS_TAG].keys():
        range_step_count = 0
        for step in content[ROUTE_DEFINITIONS_TAG][route_def][STEPS_TAG]:
            Ensure(step.keys()).contains_one_of([STEP_TAG, RANGE_STEP_TAG])

            if STEP_TAG in step:
                step.revalidate(Map({STEP_TAG: Str()}))
                Ensure(step[STEP_TAG] in step_names)
            else:
                range_step_count += 1
                step.revalidate(Map(RANGE_STEP_SCHEMA_DICT))
        Ensure(range_step_count).equals(1)

    flight_routes = [step[STEP_TAG] for step in content[FLIGHT_DEFINITION_TAG][STEPS_TAG]]
    Ensure(flight_routes).contains_only(content[ROUTE_DEFINITIONS_TAG].keys())

    return content.data
