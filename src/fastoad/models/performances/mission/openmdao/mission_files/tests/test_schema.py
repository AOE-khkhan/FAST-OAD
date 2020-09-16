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
    d = load_mission_file(pth.join(DATA_FOLDER_PATH, "test.yml"))
    assert d == OrderedDict(
        [
            (
                "phase_definitions",
                OrderedDict(
                    [
                        (
                            "initial_climb_phase",
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
                                                    ("step", "climb"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "400."),
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
                                                    ("step", "acceleration"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "250."),
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
                                                    ("step", "climb"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "1500."),
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
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        (
                            "climb_phase",
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
                                                    ("step", "climb"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "10000."),
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
                                                    ("step", "acceleration"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "300."),
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
                                                    ("step", "climb"),
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
                            "descent_phase",
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
                                                    ("step", "descent"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "300"),
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
                                                    ("step", "descent"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "altitude",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "10000."),
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
                                                    ("step", "deceleration"),
                                                    (
                                                        "target",
                                                        OrderedDict(
                                                            [
                                                                (
                                                                    "equivalent_airspeed",
                                                                    OrderedDict(
                                                                        [
                                                                            ("value", "250."),
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
                                                    ("step", "descent"),
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
                                                                            ("value", "1500."),
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
                            "main_route",
                            OrderedDict(
                                [
                                    ("range", "data:TLAR:range"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict([("step", "initial_climb_phase")]),
                                            OrderedDict([("step", "climb_phase")]),
                                            OrderedDict(
                                                [
                                                    ("range_step", "cruise"),
                                                    ("engine_setting", "cruise"),
                                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                                ]
                                            ),
                                            OrderedDict([("step", "descent_phase")]),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        (
                            "diversion_route",
                            OrderedDict(
                                [
                                    ("range", "data:mission:sizing:diversion:distance"),
                                    (
                                        "steps",
                                        [
                                            OrderedDict([("step", "climb_phase")]),
                                            OrderedDict(
                                                [
                                                    ("range_step", "cruise"),
                                                    ("engine_setting", "cruise"),
                                                    ("polar", "data:aerodynamics:aircraft:cruise"),
                                                ]
                                            ),
                                            OrderedDict([("step", "descent_phase")]),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            (
                "flight",
                OrderedDict(
                    [
                        (
                            "steps",
                            [
                                OrderedDict([("step", "main_route")]),
                                OrderedDict([("step", "diversion_route")]),
                            ],
                        )
                    ]
                ),
            ),
        ]
    )
