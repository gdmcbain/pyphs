# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:29:43 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from .edges import (PHSPort,
                    PHSDissipativeLinear,
                    PHSStorageLinear, PHSStorageNonLinear)
from pyphs.dictionary.tools import symbols, mappars
from pyphs.graphs.netlists import datum
from pyphs import PHSGraph
import sympy as sp


__all__ = ['Source', 'Stiffness', 'Mass', 'Damper', 'Springcubic',
           'Springsat', 'Felt']


class Source(PHSPort):
    """
    Voltage or current source

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        if a single label in nodes, port edge is "datum -> node"; \
else, the edge corresponds to "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'type' : source type in ('force', 'velocity').
        * 'const': if not None, the input will be replaced by the value (subs).
    """
    def __init__(self, label, nodes, **kwargs):
        type_ = kwargs['type']
        type_ = type_.lower()
        assert type_ in ('force', 'velocity')
        if type_ == 'force':
            ctrl = 'e'
        elif type_ == 'velocity':
            ctrl = 'f'
        kwargs.update({'ctrl': ctrl})
        PHSPort.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'type': 'force'}}


class Stiffness(PHSStorageLinear):
    """
    Linear stiffness

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'K' : stiffness value or symbol label or tuple (label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'K'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': False,
                  'ctrl': 'e'}
        PHSStorageLinear.__init__(self, label, nodes, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'K': ('K', 1e3)}}


class Mass(PHSStorageLinear):
    """
    Mass moving in 1D space

    Parameters
    -----------

    label : str
        Mass component label.

    nodes: (str, )
        Edge is `datum -> nodes[0]`.

    kwargs: dic with following `keys: values`:

        * `M` : Mass `value` or symbol `Mlabel` or tuple `(Mlabel, value)`.
    """
    def __init__(self, label, nodes, **kwargs):
        par_name = 'M'
        par_val = kwargs[par_name]
        kwargs = {'name': par_name,
                  'value': par_val,
                  'inv_coeff': True,
                  'ctrl': 'f'}
        PHSStorageLinear.__init__(self, label, (datum, nodes[0]), **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('M'),
                'arguments': {'M': ('M', 1e-2)}}


class Damper(PHSDissipativeLinear):
    """
    Linear damper (unconstrained control)

    Parameters
    -----------

    label : str, port label.

    nodes: tuple of nodes labels

        Edge is "nodes[0] -> nodes[1]".

    kwargs: dic with following "keys:values"

        * 'A' : Damping coefficient or symbol label (string) or tuple \
(label, value).
    """
    def __init__(self, label, nodes, **kwargs):
        if kwargs['A'] is None:
            coeff = 0.
        else:
            coeff = kwargs['A']
        PHSDissipativeLinear.__init__(self, label, nodes, coeff=coeff,
                                      inv_coeff=True)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'A': ('A', 1.)}}


class Springcubic(PHSStorageNonLinear):
    """
    Spring with cubic nonlinearity F(q)=K0*(q + K2*q**3)

    Usage
    -----

    mechanics.springcubic label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity \
'v') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'K0': Stiffness (N/m)
         * 'K2': Nonlinear contribution (dimensionless unit)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['K0', 'K2']
        for par in pars:
            assert par in kwargs.keys()
        K0, K2 = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        H = K0*x*(x + K2*x**3/2)/2
        N1, N2 = nodes

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        PHSStorageNonLinear.__init__(self, label, [edge],
                                     x, H, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'K0': ('K0', 1e3),
                              'K2': ('K2', 1e3)}}


class Springsat(PHSStorageNonLinear):
    """
    Spring with saturating nonlinearity F(q)=K0*(q + Ksat*c(q)) with
    sat(q) = (4/(4-pi))*(tan(pi*q/(2*qsat))-(pi*q/(2*qsat)))

    Usage
    -----

    mechanics.springsat label nodes: **kwargs

    Parameters:
    -----------

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity \
'v') is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

         * 'K0': Stiffness (N/m)
         * 'Ksat': Nonlinear contribution (dimensionless unit)
         * 'xsat': Saturating position (m)
    """
    def __init__(self, label, nodes, **kwargs):
        # parameters
        pars = ['K0', 'Ksat', 'xsat']
        for par in pars:
            assert par in kwargs.keys()
        K0, Ksat, xsat = symbols(pars)
        # state  variable
        x = symbols("x"+label)
        # storage funcion
        Hlin = x**2/2
        t1 = sp.pi*x/(2*xsat)
        c1 = (8*xsat/(sp.pi*(4-sp.pi)))
        Hsat = c1 * (sp.log(sp.cos(t1)) + (t1**2)/2.)
        H = K0*(Hlin - Ksat*Hsat)
        N1, N2 = nodes

        # edge data
        data = {'label': x,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}

        # edge
        edge = (N1, N2, data)

        # init component
        PHSStorageNonLinear.__init__(self, label, [edge],
                                     x, H, **kwargs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'K0': ('K0', 1e3),
                              'Ksat': ('Ksat', 1e3),
                              'xsat': ('xsat', 1e-2)}}


class Felt(PHSGraph):
    """
    Piano hammer felt
    ==================


    Usage
    -----

    mechanics.felt label nodes: **kwargs

    Parameters:
    -----------

    label : str
        Felt label.

    nodes : (N1, N2)
        tuple of nodes labels (int or string). The edge (ie. the velocity 'v')
        is directed from N1 to N2.

    kwargs : dictionary with following "key: value"

        * 'L': [m] Height of the felt at rest (1.5cm),
        * 'K': [N/m] Stiffness of the felt (5e5),
        * 'A': [N.s/m] Felt damping coefficient (1e2),
        * 'B': [d.u] Hysteresis coefficient for the felt (2.5),

    """
    def __init__(self, label, nodes, **kwargs):
        PHSGraph.__init__(self, label=label)
        dic = {'A': 1e2,  # [N.s/m] Felt damping coefficient
               'B': 2.5,  # [#] Hysteresis coefficient for the felt
               'K': 5e5,  # [N/m] Stiffness of the felt
               'L': 1.5*1e-2,  # [m] Height of the felt at rest
               }
        dic.update(kwargs)
        dicpars, subs = mappars(self, **dic)
        # parameters
        pars = ['L', 'K', 'A', 'B']
        L, K, A, B = symbols(pars)

        xnl = symbols('q'+label)
        hnl = sp.Piecewise((0., xnl <= 0.), ((L*K/(B+1))*(xnl/L)**(B+1), True))
        hnl = hnl.subs(dicpars).simplify()
        # edge data
        data = {'label': xnl,
                'type': 'storage',
                'ctrl': 'e',
                'link': None}
        self.add_edges_from([(nodes[0], nodes[1], data), ])
        self.core.add_storages(xnl, hnl)
        r = sp.Piecewise((0., xnl <= 0.), ((A * L/B)*(xnl/L)**(B-1), True)) # JSV eq (13)
        r = r.subs(dicpars).simplify()
        wnl = symbols('dtq'+label)
        # edge data
        data = {'label': wnl,
                'type': 'dissipative',
                'ctrl': 'e',
                'link': None}
        self.add_edges_from([(nodes[0], nodes[1], data), ])
        self.core.add_dissipations(wnl, r*wnl)
        self.core.subs.update(subs)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {'L': ('L', 1.5e-2),
                              'K': ('K', 5e5),
                              'A': ('A', 1e2),
                              'B': ('B', 2.5)}}
