# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:50:30 2016

@author: Falaize
"""


def add_path():
    """
    add pypHs path to sys path
    """
    import sys
    # path to pyphs
    pypHs_path = "/Users/Falaize/Documents/DEV/python/pypHs/"
    # add path
    sys.path.append(pypHs_path)


def workingdirectory():
    return '/Users/Falaize/Documents/DEV/python/pyphs/tests'


def label():
    """
    System's netlist and folder label
    """
    return "BJTAMP"


def netlist_filename():
    import os
    return workingdirectory() + os.sep + label() + '.net'


def samplerate():
    """
    global sample rate
    """
    return 192e3


def write_netlist(Cin=10e-6, Cout=10e-6, Is=1e-14, Vt=26e-3,
                  betaR=4, betaF=300, mu=1.1, Rb=20, Rc=0.1, Re=0.1, Rbc=270e3,
                  Rcd=1e3):
    """
    Write netlist for RLC circuit
    """
    from pyphs.graphs.netlists import Netlist

    netlist = Netlist()

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # capacitor Cin
    capacitorCin = {'dictionary': 'electronics',
                    'component': 'capacitor',
                    'label': 'Cin',
                    'nodes': ('A', 'B'),
                    'arguments': {'C': ('Cin', Cin)}}
    netlist.add_line(capacitorCin)

    # resistor BC
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'Rbc',
                  'nodes': ('B', 'C'),
                  'arguments': {'R': ('Rcd', Rbc)}}
    netlist.add_line(resistance)

    # bjt
    bjt = {'dictionary': 'electronics',
           'component': 'bjt',
           'label': 'BJT',
           'nodes': ('B', 'C', datum),
           'arguments': {'Is': ('Is', Is),
                         'Vt': ('Vt', Vt),
                         'betaR': ('betaR', betaR),
                         'betaF': ('betaF', betaF),
                         'mu': ('mu', mu),
                         'Rb': ('Rb', Rb),
                         'Rc': ('Rc', Rc),
                         'Re': ('Re', Re)}}
    netlist.add_line(bjt)

    # resistor CD
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'Rcd',
                  'nodes': ('C', 'D'),
                  'arguments': {'R': ('Rcd', Rcd)}}
    netlist.add_line(resistance)

    # VCC voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'VCC',
              'nodes': ('D', datum),
              'arguments': {'type': "'voltage'"}}
    netlist.add_line(source)

    # capacitor Cout
    capacitorCout = {'dictionary': 'electronics',
                     'component': 'capacitor',
                     'label': 'Cout',
                     'nodes': ('C', 'F'),
                     'arguments': {'C': ('Cout', Cout)}}
    netlist.add_line(capacitorCout)

    # output (0A current as input)
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'OUT',
              'nodes': ('F', datum),
              'arguments': {'type': "'current'"}}
    netlist.add_line(source)

    netlist.write(filename=netlist_filename())


def init_phs():
    # import pHobj
    from pyphs import PortHamiltonianObject
    import os
    phs = PortHamiltonianObject(label=label(),
                                path=workingdirectory() + os.sep + label())
    return phs


def build_graph(phs):
    phs.build_from_netlist(netlist_filename())


def input_sequence(amp=2, f0=1e3):
    from pyphs.misc.signals.synthesis import signalgenerator
    fs = samplerate()
    nsin = int(10.*fs/f0)
    ndeb = int(1*fs)
    SigIn = signalgenerator(which="sin", n=nsin, ramp_on=False,
                            A=amp, f0=f0, fs=fs, ndeb=ndeb, attack_ratio=1)

    def genu():
        for el in SigIn:
            yield [el, 9., 0.]

    return genu(), ndeb+nsin


def simulation(phs, sequ, nt):
    config = {'fs': samplerate(),
              'split': True}
    phs.build_simulation(config=config, sequ=sequ, nt=nt)
    phs.run_simulation()
    phs.plot_powerBal()
    phs.plot_powerBal(imin=int(1*samplerate()))
    phs.plot_variables([('u', 0), ('yd', 2)])
    phs.plot_variables([('u', 0), ('yd', 2)], imin=int(1*samplerate()))


if __name__ is '__main__':
    add_path()
    phs = init_phs()
    write_netlist()
    build_graph(phs)
    from pyphs.symbolics.structures.tools import move_port
    move_port(phs, phs.symbs.u.index(phs.symbols('uIN')), 0)
    move_port(phs, phs.symbs.u.index(phs.symbols('uOUT')), 2)
    sequ, nt = input_sequence()
    phs.export_latex()
    simulation(phs, sequ, nt)
