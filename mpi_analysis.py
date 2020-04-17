## Script to analyze Spectrum data

import numpy as np
import matplotlib.pyplot as plt
import auxiliar as aux
import os
from scipy.signal import find_peaks
from scipy import optimize
from scipy.io import loadmat
from scipy.io import savemat
