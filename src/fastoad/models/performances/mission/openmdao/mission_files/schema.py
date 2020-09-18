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
from ...segments.hold import HoldSegment
from ...segments.speed_change import SpeedChangeSegment
from ...segments.taxi import TaxiSegment
from ....mission.segments.altitude_change import AltitudeChangeSegment

# Tags
RANGE_STEP_TAG = "range_step"
SEGMENT_TAG = "segment"
ROUTE_TAG = "route"
PHASE_TAG = "phase"
STEPS_TAG = "steps"
MISSION_DEFINITION_TAG = "mission"
ROUTE_DEFINITIONS_TAG = "route_definitions"
PHASE_DEFINITIONS_TAG = "phase_definitions"


class SegmentNames(Enum):
    ALTITUDE_CHANGE = "altitude_change"
    CRUISE = "cruise"
    SPEED_CHANGE = "speed_change"
    HOLDING = "holding"
    TAXI = "taxi"

    @classmethod
    def string_values(cls):
        return {step.value for step in cls}

    @classmethod
    def get_segment_class(cls, value):
        segments = {
            cls.ALTITUDE_CHANGE.value: AltitudeChangeSegment,
            cls.CRUISE.value: CruiseSegment,
            cls.SPEED_CHANGE.value: SpeedChangeSegment,
            cls.HOLDING.value: HoldSegment,
            cls.TAXI.value: TaxiSegment,
        }
        return segments[value]


# Schemas
TARGET_SCHEMA = MapPattern(
    Str(), Str() | Map({"value": Float() | Str(), Optional("unit", default=None): Str()})
)

BASE_STEP_SCHEMA_DICT = {
    Optional("target", default=None): TARGET_SCHEMA,
    Optional("engine_setting", default=None): Str(),
    Optional("polar", default=None): Str(),
    Optional("thrust_rate", default=None): Float() | Str(),
    Optional("time_step", default=None): Float(),
    Optional("maximum_mach", default=None): Float() | Str(),
}

SEGMENT_SCHEMA_DICT = {SEGMENT_TAG: Str()}
SEGMENT_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

PHASE_SCHEMA_DICT = {Optional(STEPS_TAG, default=None): Seq(Map(SEGMENT_SCHEMA_DICT))}
PHASE_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)


RANGE_STEP_SCHEMA_DICT = {RANGE_STEP_TAG: Str()}
RANGE_STEP_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

ROUTE_SCHEMA_DICT = {"range": Str() | Float(), STEPS_TAG: Seq(Any())}

SCHEMA = Map(
    {
        PHASE_DEFINITIONS_TAG: MapPattern(Str(), Map(PHASE_SCHEMA_DICT)),
        ROUTE_DEFINITIONS_TAG: MapPattern(Str(), Map(ROUTE_SCHEMA_DICT)),
        MISSION_DEFINITION_TAG: Map({"name": Str(), STEPS_TAG: Seq(MapPattern(Str(), Str()))}),
    }
)


def load_mission_file(file_path: str) -> dict:
    with open(file_path) as yaml_file:
        content = load(yaml_file.read(), SCHEMA)

    # for phase_def in content[PHASE_DEFINITIONS_TAG].keys():
    #     for step in content[PHASE_DEFINITIONS_TAG][phase_def][STEPS_TAG]:
    #         Ensure(step.keys()).contains(STEP_TAG)
    #         Ensure(SegmentNames.string_values()).contains(step[STEP_TAG])
    #
    #         if step[STEP_TAG] == SegmentNames.ALTITUDE_CHANGE.value:
    #             step.revalidate(Map(CLIMB_STEP_SCHEMA_DICT))
    #         else:
    #             step.revalidate(Map(STEP_SCHEMA_DICT))

    step_names = set(content[PHASE_DEFINITIONS_TAG].keys())

    for route_def in content[ROUTE_DEFINITIONS_TAG].keys():
        range_step_count = 0
        for step in content[ROUTE_DEFINITIONS_TAG][route_def][STEPS_TAG]:
            # Ensure(step.keys()).contains_one_of([PHASE_TAG, RANGE_STEP_TAG])

            if PHASE_TAG in step:
                step.revalidate(Map({PHASE_TAG: Str()}))
                Ensure(step[PHASE_TAG] in step_names)
            else:
                range_step_count += 1
                step.revalidate(Map(RANGE_STEP_SCHEMA_DICT))
        Ensure(range_step_count).is_less_than_or_equal_to(1)

    for step in content[MISSION_DEFINITION_TAG][STEPS_TAG]:
        step_type, step_name = tuple(*step.items())
        if step_type == PHASE_TAG:
            Ensure(step_name).is_in(content[PHASE_DEFINITIONS_TAG].keys())
        elif step_type == ROUTE_TAG:
            Ensure(step_name).is_in(content[ROUTE_DEFINITIONS_TAG].keys())

    return content.data
