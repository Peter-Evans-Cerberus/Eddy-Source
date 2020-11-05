#!/usr/bin/env python3
# Peter Evans
# Cerberus Nuclear Ltd

"""This module contains all the code relating to SCALE mixtures."""
# import from standard library:
import re
# local imports:
from . import scale_global_variables as gv


class Mixture:
    """Each mixture in the SCALE case is represented by a Mixture object"""
    def __init__(self, data):
        self.number = data[0].split()[2]
        self.density = data[0].split()[5]
        try:
            self.temperature = data[0].split()[8] + 'K'
        except IndexError:
            self.temperature = "Not given in output file"
        self.isotopes = {}
        for line in data[2:]:
            nuclide = line.split()[0]
            self.isotopes[nuclide] = {}
            self.isotopes[nuclide]['nuclide'] = int(nuclide)
            self.isotopes[nuclide]['atom-density'] = float(line.split()[1])
            self.isotopes[nuclide]['weight fraction'] = float(line.split()[2])
            self.isotopes[nuclide]['z-number'] = int(line.split()[3])
            self.isotopes[nuclide]['atomic weight'] = float(line.split()[4])
            self.isotopes[nuclide]['title'] = line.split()[5].capitalize()
            self.isotopes[nuclide]['temperature'] = float(line.split()[6])
        gv.mixture_list.append(self)


def get_mixture_data(output_data):
    """Get the part of the SCALE output concerning mixtures

    Args:
        output_data (list): The SCALE output data

    Returns:
        The lines from output_data concerning mixtures
    """
    pattern_mix = re.compile(r'^\s*mixing table\s+')
    for n, line in enumerate(output_data):
        if pattern_mix.match(line):
            for m, other_line in enumerate(output_data[n+1:], start=n+1):
                if "Cross section" in other_line or "***********" in other_line:
                    return output_data[n:m]


def create_mixtures(mix_data):
    """Create Mixture objects from the SCALE output data

    Args:
        mix_data (list): The lines from output_data concerning mixtures

    Returns:
        None, but creates Mixture objects
    """
    for n, line in enumerate(mix_data):
        if "mixture = " in line:
            for m, other_line in enumerate(mix_data[n+1:], start=n+1):
                if other_line == "\n":
                    mix = mix_data[n:m]
                    Mixture(mix)
                    break
