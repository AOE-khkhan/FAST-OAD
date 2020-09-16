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

from collections import OrderedDict
from typing import List

from ensure import Ensure
from strictyaml import load, Map, MapPattern, Optional, Str, Float, Seq, Any

from fastoad.utils.strings import fieldify

BASE_STEP_NAMES = {"climb", "cruise", "descent", "acceleration", "deceleration"}

TARGET_SCHEMA = MapPattern(
    Str(), Map({"value": Str() | Float(), Optional("unit", default=None): Str()})
)

BASE_STEP_SCHEMA_DICT = {
    Optional("target", default=None): TARGET_SCHEMA,
    Optional("engine setting", default=None): Str(),
    Optional("polar", default=None): Str(),
    Optional("thrust rate", default=None): Str() | Float(),
    Optional("time step", default=None): Str() | Float(),
    Optional("steps", default=None): Seq(Any()),
}

STEP_SCHEMA_DICT = {"step": Str()}
STEP_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

RANGE_STEP_SCHEMA_DICT = {"range step": Str()}
RANGE_STEP_SCHEMA_DICT.update(BASE_STEP_SCHEMA_DICT)

CLIMB_STEP_SCHEMA_DICT = {Optional("maximum mach", default=None): Str() | Float()}
CLIMB_STEP_SCHEMA_DICT.update(STEP_SCHEMA_DICT)

ROUTE_SCHEMA_DICT = {"range": Str() | Float(), "steps": Seq(Any())}

SCHEMA = Map(
    {
        "phase definitions": MapPattern(Str(), Map(BASE_STEP_SCHEMA_DICT)),
        "route definitions": MapPattern(Str(), Map(ROUTE_SCHEMA_DICT)),
        "flight": Map({"steps": Seq(Map({"step": Str()}))}),
    }
)


def load_mission_file(file_path: str) -> dict:
    with open(file_path) as yaml_file:
        content = load(yaml_file.read(), SCHEMA)

    for phase_def in content["phase definitions"].keys():
        for step in content["phase definitions"][phase_def]["steps"]:
            Ensure(step.keys()).contains("step")
            Ensure(BASE_STEP_NAMES).contains(step["step"])

            if step["step"] != "climb":
                step.revalidate(Map(STEP_SCHEMA_DICT))
            else:
                step.revalidate(Map(CLIMB_STEP_SCHEMA_DICT))

    step_names = BASE_STEP_NAMES | set(content["phase definitions"].keys())

    for route_def in content["route definitions"].keys():
        range_step_count = 0
        for step in content["route definitions"][route_def]["steps"]:
            Ensure(step.keys()).contains_one_of(["step", "range step"])

            if "step" in step:
                step.revalidate(Map({"step": Str()}))
                Ensure(step["step"] in step_names)
            else:
                range_step_count += 1
                step.revalidate(Map(RANGE_STEP_SCHEMA_DICT))
        Ensure(range_step_count).equals(1)

    flight_routes = [step["step"] for step in content["flight"]["steps"]]
    Ensure(flight_routes).contains_only(content["route definitions"].keys())

    return _fieldify_dict(content.data)


def _fieldify_dict(my_dict: dict) -> dict:
    new_dict = OrderedDict()
    for key, val in my_dict.items():
        if isinstance(key, str):
            new_key = fieldify(key)
        else:
            new_key = key
        new_val = _fieldify_value(val)
        new_dict[new_key] = new_val
    return new_dict


def _fieldify_list(my_list: List) -> List:
    return [_fieldify_value(val) for val in my_list]


def _fieldify_value(val):
    if isinstance(val, str):
        new_val = fieldify(val)
    elif isinstance(val, dict):
        new_val = _fieldify_dict(val)
    elif isinstance(val, list):
        new_val = _fieldify_list(val)
    else:
        new_val = val
    return new_val
