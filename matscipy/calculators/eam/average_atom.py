# -*- coding: utf-8 -*-
# ======================================================================
# matscipy - Python materials science tools
# https://github.com/libAtoms/matscipy
#
# Copyright (2020) Wolfram Nöhring, University of Freiburg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# ======================================================================

from __future__ import division, print_function
from .io import EAMParameters
import numpy as np


def average_potential(
    concentrations,
    parameters,
    F,
    f,
    rep,
    kind="eam/alloy",
    avg_atom="A",
    atomic_number=999,
    crystal_structure="unknown",
    lattice_constant=1.0,
):
    r"""Generate an Average-atom EAM potential

    The Average-atom (A-atom) potential is a mean-field approximation for
    random alloys, see Ref. `1`_. The purpose is to replace the true elements
    by a single fictious element, the A-atom. A configuration of A-atoms
    has approximately the same potential energy as the corresponding random
    alloy configuration. Furthermore, the A-atom configuration has similar 
    average material properties, e.g. similar elastic constants.

    The A-atom potential has standard EAM form, i.e. it can be tabulated
    just like any other EAM potential. The potential functions are simply
    the concentration-weighted averages of the pure element functions.

    In the case of eam/alloy potentials, the new potential functions are 

    .. math::
        
        \phi_{AX}\left(r_{\gamma\delta}\right) 
            &= \sum_{Y}^{N_T} c_{Y}  
            \phi_{YX}\left(r_{\gamma\delta}\right) \quad\text{(pair potential for $AX$-pairs)}, \\
        \phi_{AA}\left(r_{\gamma\delta}\right) 
            &= \sum_{X}^{N_T} c_{X}  
            \phi_{AX}\left(r_{\gamma\delta}\right) \quad\text{(pair potential for $AA$-pairs)}, \\
        U_{A}\left(\rho_\gamma\right)  
            &= \sum_{X}^{N_T}c_{X}U_{X}\left(\rho_\gamma\right) \quad\text{(embedding energy)}, \\
        g_A\left(r_{\gamma\delta}\right) 
            &= \sum_{X}^{N_T}c_X g_X\left(r_{\gamma\delta}\right)\quad\text{(electron density)},\;\text{and}\\
        m_A &= \sum_{X}^{N_T}c_X m_X\quad\text{(mass)}.

    Mind that the pair functions are symmetric, i.e.
    :math:`\phi_{XY}=\phi_{YX}`. In the case of eam/alloy potentials, there is
    one electron density function for each element. Finnis-Sinclair (eam/fs,
    Ref. `2`_) potentials, by contrast, have one electron density function
    per *pair* of elements. The density contributions are not symmetric, i.e.
    :math:`g_{XY}\neq{}g_{YX}`. The potential functions are

    .. math::

        \phi_{AX}\left(r_{\gamma\delta}\right) 
            &= \sum_{Y}^{N_T} c_{Y}  
            \phi_{YX}\left(r_{\gamma\delta}\right) \quad\text{(pair potential for $AX$-pairs)}, \\
        \phi_{AA}\left(r_{\gamma\delta}\right) 
            &= \sum_{X}^{N_T} c_{X}  
            \phi_{AX}\left(r_{\gamma\delta}\right) \quad\text{(pair potential for $AA$-pairs)}, \\
        U_{A}\left(\rho_\gamma\right)  
            &= \sum_{X}^{N_T}c_{X}U_{X}\left(\rho_\gamma\right) \quad\text{(embedding energy)}, \\
        g_{AX}\left(r_{\gamma\delta}\right) 
            &= \sum_{Y}^{N_T}c_Y g_{YX}\left(r_{\gamma\delta}\right)\quad\text{(electron density by $A$ for $X$)},\\
        g_{XA}\left(r_{\gamma\delta}\right) 
            &= \sum_{Y}^{N_T}c_Y g_{XY}\left(r_{\gamma\delta}\right)\quad\text{(electron density by $X$ for $A$)},\\
        g_{AA}\left(r_{\gamma\delta}\right) 
            &= \sum_{X}^{N_T}c_X g_{XA} = \sum_{X}^{N_T}c_T g_{AX}\left(r_{\gamma\delta}\right)\quad\text{(electron density by $A$ for $A$)},\;\text{and}\\
        m_A &= \sum_{X}^{N_T}c_X m_X\quad\text{(mass)}.

    .. note::
        
        The derivation for eam/alloy and eam/fs potentials is mostly the same.
        However, compared to eam/alloy potentials, eam/fs potentials require
        one additional approximation, concerning the Taylor expansion of the
        embedding energy about the configurational average of the electron
        density,

        .. math:: 
            
            U^X\left(\rho_\gamma\right)
            \approx U^X\left(\left\langle\rho_\gamma\right\rangle\right)
            +\frac{\partial U^X}{\partial \rho_\gamma}\bigg\vert_{\left\langle\rho_\gamma\right\rangle}
            \left(\rho_\gamma- \left\langle\rho_\gamma\right\rangle\right) + \dots

        In the case of eam/alloy potentials, the linear term vanishes when taking
        the configurational average :math:`\left\langle\bullet\right\rangle` 
        (on average, deviations from the average electron density are zero).
        However, in the case of eam/fs potentials, the electron density has
        a more complicated form, hence the linear term doesn't vanish 
        upon averaging. Therefore, we need to assume that it is zero, i.e.
        only the leading term of the Taylor series is retained 
        :math:`U^X\left(\rho_\gamma\right)\approx U^X\left(\left\langle\rho_\gamma\right\rangle\right)`.

    .. tip::

        Before using A-atom potentials in production, verify that the potential
        has similar average properties as the true random alloy, e.g. similar
        average lattice parameter, elastic constants, etc.
        


    Parameters
    ----------
    concentrations: array_like
        concentrations of the elements in the A-atom
    parameters: EAMParameters
        EAM potential parameters
    F : array_like
        tabulated embedding energy functionals
    f : array_like
        tabulated electron density functions
    rep : array_like
        tabulated pair potential energy functions
    kind : string
        "eam/alloy" or "eam/fs" are supported 

    Returns
    -------
    parameters : EAMParameters
        EAM potential parameters
    new_F : array_like
        tabulated embedding energy functionals, including A-atom functional
    new_f : array_like
        tabulated electron density functions, including A-atom function(s)
    new_rep : array_like
        tabulated pair potential energy functions, including pairs with A-atom

    Examples
    --------
    >>> from matscipy.calculators.eam import io, average_atom
    >>> source, parameters, F, f, rep = io.read_eam(
    >>>     "ZrCu.onecolumn.eam.alloy"
    >>> )
    >>> concentrations = [0.5, 0.5]
    >>> (new_parameters, new_F, new_f, new_rep) = average_atom.average_potential(
    >>>     concentrations, parameters, F, f, rep
    >>> )
    >>> composition = " ".join(
    >>>     [str(c * 100.0) + "% {0},".format(e) for c, e in zip(concentrations, parameters.symbols)]
    >>> )
    >>> composition = composition.rstrip(",")
    >>> source += ", averaged for composition {0}".format(composition)
    >>> io.write_eam(
    >>>     source,
    >>>     new_parameters,
    >>>     new_F,
    >>>     new_f,
    >>>     new_rep,
    >>>     "ZrCu.onecolumn.averaged.eam.alloy",
    >>>     kind="eam/alloy",
    >>> )

    Read an EAM potential table for two elements in eam/alloy format, and create
    a new table with additional A-atom functions for the equicomposition alloy.

    References
    ----------

    .. [1] Varvenne, C., Luque, A., Nöhring, W. G. & Curtin, W. A. 
       Average-atom interatomic potential for random alloys. 
       Physical Review B 93, 104201 (2016).

    .. [2] Finnis M. W. & Sinclair, J. E. A simple empirical N-body potential 
       for transition metals. Philosophical Magazine A 50, 45 (1984).

    Notes
    -----
    Notation:
     * :math:`N` Number of atoms 
     * :math:`N_T` Number of elements
     * :math:`r_{\nu\mu{}}` Pair distance of atoms :math:`\nu` and :math:`\mu`
     * :math:`\phi_{\nu\mu}(r_{\nu\mu{}})` Pair potential energy of atoms :math:`\nu` and :math:`\mu` 
     * :math:`\rho_{\nu}` Total electron density of atom :math:`\nu`  
     * :math:`U_\nu(\rho_nu)` Embedding energy of atom :math:`\nu` 
     * :math:`g_{\delta}\left(r_{\gamma\delta}\right) \equiv g_{\gamma\delta}` Contribution from atom :math:`\delta` to :math:`\rho_\gamma`
     * :math:`m_\nu` mass of atom :math:`\nu`

    """

    if kind == "eam":
        raise NotImplementedError
    assert np.isclose(np.sum(concentrations), 1)
    symbols = [s for s in parameters.symbols] + [avg_atom]
    atomic_numbers = np.r_[parameters.atomic_numbers, atomic_number]
    atomic_masses = np.r_[
        parameters.atomic_masses, np.average(parameters[2], weights=concentrations)
    ]
    lattice_constants = np.r_[parameters.lattice_constants, lattice_constant]
    crystal_structures = np.r_[
        parameters.crystal_structures, np.array(crystal_structure)
    ]
    new_parameters = EAMParameters(
        symbols,
        atomic_numbers,
        atomic_masses,
        lattice_constants,
        crystal_structures,
        parameters.number_of_density_grid_points,
        parameters.number_of_distance_grid_points,
        parameters.density_grid_spacing,
        parameters.distance_grid_spacing,
        parameters.cutoff,
    )
    # Average embedding energy and electron density functions
    new_F = np.r_[F, np.zeros((1, F.shape[1]), dtype=F.dtype)]
    new_F[-1, :] = np.average(F, axis=0, weights=concentrations)
    if kind == "eam/alloy":
        new_f = np.r_[f, np.zeros((1, f.shape[1]), dtype=f.dtype)]
        new_f[-1, :] = np.average(f, axis=0, weights=concentrations)
    elif kind == "eam/fs":
        new_f = np.concatenate(
            (f, np.zeros((f.shape[0], 1, f.shape[2]), dtype=f.dtype)), axis=1
        )
        new_f = np.concatenate(
            (new_f, np.zeros((1, new_f.shape[1], f.shape[2]), dtype=f.dtype)),
            axis=0,
        )
        # The electron density functions of Finnis-Sinclar potentials
        # form a Nelements x Nelements x Nfunctionvalues array. 
        # In contrast to the array of pair potential functions,
        # the Nfunctionvalues Nelements x Nelements matrices given by 
        # the first two dimensions are not symmetric
        new_f[-1, :-1, :] = np.average(f, axis=0, weights=concentrations)
        new_f[:-1, -1, :] = np.average(f, axis=1, weights=concentrations)
        column = new_f[:-1, -1, :]
        new_f[-1, -1, :] = np.average(column, axis=0, weights=concentrations)
        # row and column averaging should yield the same result
        #row = new_f[-1, :-1, :]
        #print(np.linalg.norm(new_f[-1, -1, :] - np.average(row, axis=0, weights=concentrations)))
    else:
        raise NotImplementedError
    # Average the pair potential
    new_rep = np.concatenate(
        (rep, np.zeros((rep.shape[0], 1, rep.shape[2]), dtype=rep.dtype)), axis=1
    )
    new_rep = np.concatenate(
        (new_rep, np.zeros((1, new_rep.shape[1], rep.shape[2]), dtype=rep.dtype)),
        axis=0,
    )
    # Consider the matrix Vij of pair functions
    # i: rows, each corresponding to an element
    # j: columns, each corresponding to an element
    # Each element corresponds to the function
    # for the atom pair i,j
    #
    # Compute the last row of the new Vij matrix, excluding the
    # value on the diagonal. Each column j corresponds to the
    # interaction of a particular type j with the homogenous material.
    new_rep[-1, :-1, :] = np.average(rep, axis=0, weights=concentrations)
    new_rep[:-1, -1, :] = new_rep[-1, :-1, :]
    # Compute the last potential on the diagonal. This is the
    # interaction of the homogeneous material with itself.
    column = new_rep[:-1, -1, :]
    new_rep[-1, -1, :] = np.average(column, axis=0, weights=concentrations)

    return new_parameters, new_F, new_f, new_rep
