# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines functions that yield lammps workflows
"""

from fireworks import Workflow, Firework

from pymatgen.io.lammps.input import DictLammpsInput

from atomate.lammps.firetasks.write_inputs import WriteLammpsFromIOSet
from atomate.lammps.firetasks.run_calc import RunLammpsDirect
from atomate.lammps.firetasks.parse_outputs import  LammpsToDBTask


__author__ = 'Kiran Mathew'
__email__ = "kmathew@lbl.gov"


# TODO: @matk86 - It is better if you can have a Fireworks module that includes packmol and
# lammps Fireworks. I understand the firework definitions are simple, but it will be easier for
# people to find the Fireworks there since it will be a familiar subpackage structure.
# It should be an easy mod and shouldn't get in the way much. -computron

def get_wf(job_name, lammps_input_set, input_filename="lammps.inp", lammps_bin="lammps",
           db_file=None, dry_run=False):
    """
    Returns workflow that writes lammps input/data files, runs lammps and inserts to DB.

    Args:
        job_name: job name
        lammps_input_set (DictLammpsInput): lammps input
        input_filename (string): input file name
        lammps_bin (string): path to the lammps binary
        db_file (string): path to the db file
        dry_run (bool): for test purposes, decides whether or not to run the lammps binary
            with the input file.

    Returns:
        Workflow

    """
    task1 = WriteLammpsFromIOSet(lammps_input_set=lammps_input_set, input_file=input_filename)
    if dry_run:
        lammps_cmd = lammps_bin
    else:
        lammps_cmd = lammps_bin + " -in " + input_filename
    task2 = RunLammpsDirect(lammps_cmd=lammps_cmd)
    task3 = LammpsToDBTask(lammps_input=lammps_input_set, db_file=db_file)
    fw1 = Firework([task1, task2, task3], name=job_name)
    return Workflow([fw1], name=job_name)
