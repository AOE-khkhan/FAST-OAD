"""
This script reads the 2 column files 'rename_vars.txt' where the the first
column contains old OpenMDAO variable names and the new names.
Replaces old names by new ones in all files of ./src and ./tests.
"""
#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2019  ONERA/ISAE
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

import fileinput
import os
import os.path as pth
import re

import numpy as np

from fastoad.exceptions import XPathError, VariableError
from fastoad.io.xml import OMCustomXmlIO, OMXmlIO
from fastoad.io.xml.openmdao_basic_io import BasicVarXpathTranslator
from fastoad.io.xml.translator import VarXpathTranslator
from tests import root_folder_path

SRC_PATH = pth.join(root_folder_path, 'src')
TEST_PATH = pth.join(root_folder_path, 'tests')
VAR_NAME_FILE = pth.join(pth.dirname(__file__), 'rename_vars.txt')


def build_translator(var_names_match: np.ndarray) -> VarXpathTranslator:
    """
    Builds the translator for reading XMLs with old name and have new OpenMDAO
    var names
    :param var_names_match: Nx2 numpy array with old var names in first column
                            and new names in the second column
    :return: the VarXpathTranslator instance
    """
    xpaths = ['/'.join(var_name.split(':')) for var_name in var_names_match[:, 0]]
    var_names = var_names_match[:, 1]

    translator = SemiBasicVarXpathTranslator()
    translator.set(var_names, xpaths)
    return translator


def convert_xml(file_path: str, translator: VarXpathTranslator):
    """
    Modifies given XML file by translating XPaths according to provided
    translator

    :param file_path:
    :param translator:
    """
    reader = OMCustomXmlIO(file_path)
    reader.set_translator(translator)
    ivc = reader.read()

    OMXmlIO(file_path).write(ivc)


def replace_var_names(file_path, var_names_match):
    """
    Modifies provided text file by modifying old OpenMDAO variable names
    to new ones.

    :param file_path:
    :param var_names_match:
    """
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            new_line = line
            for old_name, new_name in var_names_match:
                new_line = re.sub('(?<!:)\\b%s\\b(?!:)' % old_name, new_name, new_line)
            print(new_line, end='')


class SemiBasicVarXpathTranslator(VarXpathTranslator):
    """
    VarXpathTranslator that processes unknown path or variables as
    in BasicVarXpathTranslator
    """

    def __init__(self, path_separator=':'):
        super().__init__()
        self.basic_translator = BasicVarXpathTranslator(':')

    def get_variable_name(self, xpath: str) -> str:

        try:
            return super().get_variable_name(xpath)
        except XPathError:
            return self.basic_translator.get_variable_name(xpath)

    def get_xpath(self, var_name: str) -> str:
        try:
            return super().get_xpath(var_name)
        except VariableError:
            return self.basic_translator.get_xpath(var_name)


if __name__ == '__main__':

    old_new_names = np.genfromtxt(VAR_NAME_FILE, dtype=str, autostrip=True, deletechars='\n')

    # process XML files
    old_new_translator = build_translator(old_new_names)
    file_list = [
        'tests/integration_tests/oad_process/data/perfo_process_inputs.xml',
        'tests/integration_tests/oad_process/data/propulsion_process_inputs.xml',
        'tests/unit_tests/modules/aerodynamics/data/aerodynamics_inputs.xml',
        'tests/unit_tests/modules/geometry/data/geometry_inputs.xml',
        'tests/unit_tests/modules/geometry/data/geometry_inputs_full.xml',
        'tests/unit_tests/modules/geometry/data/get_cg_inputs.xml',
        'tests/unit_tests/modules/geometry/data/global_geometry_inputs.xml',
        'tests/unit_tests/modules/mass_breakdown/data/mass_breakdown_inputs.xml'
    ]
    for xml_file_path in file_list:
        print('processing %s' % xml_file_path)
        convert_xml(pth.join(root_folder_path, xml_file_path), old_new_translator)

    # replace var names
    for root_path in [SRC_PATH, TEST_PATH]:
        for dir_path, dir_names, file_names in os.walk(root_path):
            for filename in file_names:
                ext = pth.splitext(filename)[1]
                if ext not in ['.pyc', '.exe']:  # avoid processing useless files
                    xml_file_path = pth.join(dir_path, filename)
                    print('processing %s' % xml_file_path)
                    replace_var_names(xml_file_path, old_new_names)