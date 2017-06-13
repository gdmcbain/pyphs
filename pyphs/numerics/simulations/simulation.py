# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.config import simulations
from ..cpp.simu2cpp import simu2cpp, main_path
from ..cpp.numcore2cpp import numcore2cpp
from .. import PHSNumericalCore
from .data import PHSData
from pyphs.misc.io import dump_files, with_files
import subprocess
import progressbar
import time
import os
import sys
import numpy as np


class PHSSimulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, core, config=None):
        """
        Parameters
        -----------

        config : dic of configuration options

            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
              'path': None,         # Path to the results folder
              'pbar': True,         # Display a progress bar
              'timer': False,       # Display minimal timing infos
              'lang': 'c++',        # Language in {'python', 'c++'}
              'script': None,       # Call to C++ compiler and exec binary
              'eigen': None,        # Path to Eigen C++ library
              # Options for the data reader. The data are read from index imin
              # to index imax, rendering one element out of the number decim
              'load': {'imin': None,
                       'imax': None,
                       'decim': None}
        """

        # init config with standard configuration options
        self.config = simulations.copy()

        # update with provided opts
        if config is None:
            config = {}
        self.config.update(config)

        if self.config['path'] is None:
            self.config['path'] = os.getcwd()
        
        if not os.path.exists(self.config['path']):
            os.mkdir(self.config['path'])

        # store PHSCore
        setattr(self, '_core', core.__deepcopy__())

        assert self.config['lang'] in ['c++', 'python']
        setattr(self, 'nums', PHSNumericalCore(self._core, config=self.config))

        if self.config['lang'] == 'c++':
            objlabel = self.nums.label.upper()
            self.cpp_path = os.path.join(main_path(self), objlabel.lower())
            self.src_path = os.path.join(self.cpp_path, 'src')
            if not os.path.exists(self.src_path):
                os.mkdir(self.cpp_path)
            if not os.path.exists(self.cpp_path):
                os.mkdir(self.src_path)
            numcore2cpp(self.nums, objlabel=objlabel, path=self.src_path,
                        eigen_path=self.config['eigen'])

###############################################################################

    def init(self, nt=None, u=None, p=None, x0=None, dx0=None, w0=None):
        """
    init
    ****

    Initialize simulation data.

    Parameters
    ----------

    u: iterable or None, optional
        Input sequence wich elements are arrays with shape (core.dims.y(), ).
        If the lenght nt of the sequence is known (e.g. sequ is a list), the
        number of simulation time steps is set to nt. If None, a sequence with
        length nt of zeros with appropriate shape is used (default).

    p: iterable or None, optional
        Input sequence wich elements are arrays with shape (core.dims.p(), ).
        If (i) the lenght of sequ is not known, and (ii) the length nt of seqp
        is known (e.g. seqp is a list), the number of simulation time steps is
        set to nt=len(seqp). If None, a sequence with length nt of zeros with
        appropriate shape is used (default).

    x0: array of float or None, optional
        State vector initialisation value. If None, an array of zeros with
        appropriate shape is used (default).

    nt: int or None:
        Number of time steps. If None, the lenght of either sequ or seqp must
        be known (i.e. they are not either generators or None).

        """
        self.data = PHSData(self.nums.method, self.config)
        if x0 is None:
            x0 = np.zeros(self.nums.method.dims.x())
        self.nums.set_x(x0)
        if dx0 is None:
            dx0 = np.zeros(self.nums.method.dims.x())
        self.nums.set_dx(dx0)
        if w0 is None:
            w0 = np.zeros(self.nums.method.dims.w())
        self.nums.set_w(w0)
        self.data.init_data(u, p, x0, nt)

    def process(self):
        """
        Process simulation for all time steps.

        Usage
        -----
        After initialization of a PHSSimulation object `simu.init`:

        .. code:: simu.process()

        """
        print('Process...')
        if self.config['timer']:
            tstart = time.time()

        # language is 'py' or 'cpp'
        if not self.config['lang'] in ('c++', 'python'):
            text = 'Unknown language {}.'.format(self.config['language'])
            raise NameError(text)

        if self.config['lang'] == 'c++':
            self._process_cpp()

        elif self.config['lang'] == 'python':
            self._process_py()

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:

            t_total = tstop-tstart
            print('Total time: {}s'.format(tstop-tstart, 'f'))

            string = 'Total time w.r.t number of iterations: {}s'
            time_it = (t_total/float(self.data.config['nt']))
            print(string.format(time_it))

        print('Simulation: Done')

    def _init_pb(self):
        pb_widgets = ['\n', 'Simulation: ',
                      progressbar.Percentage(), ' ',
                      progressbar.Bar(), ' ',
                      progressbar.ETA()
                      ]
        self._pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                             maxval=self.data.config['nt'])
        self._pbar.start()

    def _update_pb(self):
        self._pbar.update(self.n)

    def _close_pb(self):
        self._pbar.finish()

    def _process_py(self):

        # get generators of u and p
        data = self.data
        load = {'imin': 0, 'imax': None, 'decim': 1}
        seq_u = data.u(**load)
        seq_p = data.p(**load)

        path = os.path.join(self.config['path'], 'data')
        list_of_files = list(self.config['files'])

        def process(files):
            if self.config['pbar']:
                self._init_pb()

            # init time step
            self.n = 0

            # process
            for (u, p) in zip(seq_u, seq_p):
                # update numerics
                self.nums.update(u=u, p=p)

                # write to files
                dump_files(self.nums, files)

                self.n += 1

                # update progressbar
                if self.config['pbar']:
                    self._update_pb()

            if self.config['pbar']:
                self._close_pb()

            time.sleep(0.1)

        with_files(path, list_of_files, process)
        # close_files(files)

    def _process_cpp(self):

        # build simu.cpp
        simu2cpp(self)

        # go to build folder
        os.chdir(self.cpp_path)

        # execute the bash script
        self.system_call('./run.sh')

    @staticmethod
    def system_call(cmd):
        """
        Execute a system command.

        Parameter
        ---------

        cmd : list
            List of arguments.

        Example
        -------
        Change directory with
        cmd = ['cd', './my/folder']
        system_call(cmd)
        """
        system_call(cmd)

    @staticmethod
    def execute_bash(text):
        """
        Execute a bash script, ignoring lines starting with #

        Parameter
        ---------

        text : str
            Bash script content. Execution of each line iteratively.
        """
        execute_bash(text)


def system_call(cmd):
    """
    Execute a system command.

    Parameter
    ---------

    cmd : list
        List of arguments.

    Example
    -------

    Change directory with

    >>> cmd = ['cd', './my/folder']
    >>> system_call(cmd)

    """
    if sys.platform.startswith('win'):
        shell = True
    else:
        shell = True
    print(cmd)
    p = subprocess.Popen(cmd, shell=shell,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line.decode()),


def execute_bash(text):
    """
    Execute a bash script, ignoring lines starting with #

    Parameter
    ---------

    text : str
        Bash script content. Execution of each line iteratively.
    """
    for line in text.splitlines():
        if line.startswith('#') or len(line) == 0:
            pass
        else:
            system_call(line.split())
