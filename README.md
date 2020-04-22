## Multiphoton Ionization of SiF<sub>4</sub>

This repository contains all the python scripts to analyze the MPI experiments developed in the lab.

After the experiments we get the oscilloscope traces of the different channels. In particular, we want to analyze one channel, the ion detector signal, which is proportional to the number of ions detected. Also, the pyroelectric detector signal is important because this indicates the energy laser.

Things to do to analyze the data:
* Mass Spec calibration &rarr; $t = \alpha \sqrt{m} + t_{0}$.
A simple idea to do this is to detect the peaks of the SiF<sub>4</sub> radicals'. Perhaps it's possible to establish a more general algorithm.

* Determine laser energy by getting the peak of the pyroelectric signal. It's a GenTec detector.

* Non-linear fit between the ion signal and the laser power. A simple model for this is a power law with a laser saturation power. Something like this.
$N_{\text{ion}} = \frac{N_{0}}{1+(Is/I)^{b}}$

* Develop a model that includes the geometric description of laser shape and the extraction zone.

Summarizing the different files:

* auxiliar.py &rarr; file that contains the functions to use in the main file.
* mpi_analysis.py &rarr; file with the whole analysis.

  
