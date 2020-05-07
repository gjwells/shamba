#!/usr/bin/py

"""Module for global variables for all of SHAMBA."""

import os
from time import gmtime,strftime
import uuid


# input and output files for specific project
# change this for specific projects
#BASE_PATH = os.path.expanduser("W:/ShambaDev/shamba_git_repositories/shamba_v1.1/shamba/shamba_stable_1.1/shamba") 
BASE_PATH = os.path.expanduser("D:/sources/python/shamba/shamba") 
PROJ_DIR = os.path.join(BASE_PATH, 'shamba_projects')
# no need to specify SAV, INP, OUT directories if specified in cl file
SAV_DIR = os.path.join(PROJ_DIR, 'default') # overwrite this later
INP_DIR = os.path.join(SAV_DIR, 'input')
OUT_DIR = os.path.join(SAV_DIR, 'output')

# For holding command-line arguments
args = []

# Number of years for model to run and accounting period
# NOTE: change this in main after tree max age data is read
# no need to specify years if specified in cl file
N_YEARS = 30
N_ACCT = 30


# Save the time (that cfg is imported) and generate 
# universally unique identifier (uuid) for the project

# convert seconds since the epoch to an ISO-8601 time in UTC
TIME = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
ID = uuid.uuid4().hex
PROJ_NAME = None
