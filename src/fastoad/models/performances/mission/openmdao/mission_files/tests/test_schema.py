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

from ..schema import load_mission_file

DATA_FOLDER_PATH = pth.join(pth.dirname(__file__), "data")


def test_schema():
    d = load_mission_file(pth.join(DATA_FOLDER_PATH, "mission.yml"))

    assert d == OrderedDict(
        [
            (
                "phase_definitions",
                OrderedDict(
                    [
                        (
                            "initial_climb",
                            OrderedDict(
                                [
                                    ("engine_setting", "takeoff"),
                                    ("polar", "data:aerodynamics:aircraft:takeoff"),
                                    ("thrust_rate", "data:mission:sizing:climb:thrust_rate"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 400.0),
                                                                            ("unit", "ft"),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "speed_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    "initial_climb:final_equivalent_airspeed",
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "polar",
                                                        "data:aerodynamics:aircraft:low_speed",
                                                    ),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    "initial_climb:final_altitude",
                                                                ),
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        (
                            "climb",
                            OrderedDict(
                                [
                                    ("engine_setting", "climb"),
                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                    ("thrust_rate", "data:mission:sizing:climb:thrust_rate"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 10000.0),
                                                                            ("unit", "ft"),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "speed_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 300.0),
                                                                            ("unit", "kn"),
                                                                        ]
                                                                    ),
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [("value", "optimal")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    ("maximum_mach", "data:TLAR:cruise_mach"),
                                                ]
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        (
                            "descent",
                            OrderedDict(
                                [
                                    ("engine_setting", "idle"),
                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                    ("thrust_rate", "data:mission:sizing:descent:thrust_rate"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 300.0),
                                                                            ("unit", "kn"),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "mach",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 10000.0),
                                                                            ("unit", "ft"),
                                                                        ]
                                                                    ),
                                                                ),
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "speed_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 250.0),
                                                                            ("unit", "kn"),
                                                                        ]
                                                                    ),
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            OrderedDict(
                                                [
                                                    ("step", "altitude_change"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [("value", "constant")]
                                                                    ),
                                                                ),
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", 1500.0),
                                                                            ("unit", "ft"),
                                                                        ]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            (
                "route_definitions",
                OrderedDict(
                    [
                        (
                            "main",
                            OrderedDict(
                                [
                                    ("range", "data:TLAR:range"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict([("step", "initial_climb")]),
                                            OrderedDict([("step", "climb")]),
                                            OrderedDict(
                                                [
                                                    ("range_step", "cruise"),
                                                    ("engine_setting", "cruise"),
                                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                                ]
                                            ),
                                            OrderedDict([("step", "descent")]),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        (
                            "diversion",
                            OrderedDict(
                                [
                                    ("range", "data:mission:sizing:diversion:distance"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict([("step", "climb")]),
                                            OrderedDict(
                                                [
                                                    ("range_step", "cruise"),
                                                    ("engine_setting", "cruise"),
                                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                                ]
                                            ),
                                            OrderedDict([("step", "descent")]),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            (
                "mission",
                OrderedDict(
                    [
                        ("name", "sizing"),
                        (
                            "steps",
                            [
                                OrderedDict([("step", "main")]),
                                OrderedDict([("step", "diversion")]),
                            ],
                        ),
                    ]
                ),
            ),
        ]
    )
