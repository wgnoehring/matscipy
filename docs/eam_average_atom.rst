.. _eam_avg_atom:

Embedding energy of the A-atom for :code:`eam/fs` potentials
============================================================

The average atom (A-atom) is a model for simulating the average behavior of
a random alloy. The A-atom functions for Embedded Atom Method `1`_
potentials were derived in Refs. `2`_ and `3`_. This page deals with the embedding
energy functional of the A-atom. The derivation in the aforementioned references
is repeated for Finnis-Sinclair `4`_ EAM potentials (:code:`eam/fs`).


Total potential energy of a random alloy
----------------------------------------

Consider a random alloy with :math:`{N_a}\geq{}1` atoms and
:math:`{N_t}{}\geq{}1` constituent elements. The set of atomic sites is
:math:`\Omega_a=\left\lbrace{}i\;\vert{}\;i\in\left[1\dots{N_a}\right]\right\rbrace`,
and the set of constituent elements is 
:math:`\Omega_t=\left\lbrace{}X\;\vert{}\;X\in\left[1\dots{N_t}\right]\right\rbrace`.
Each site is occupied by one element drawn from :math:`\Omega_t`. One
specific element distribution can be described by occupation variables

.. math::
    :label: equ:bernoulliprod

    \left\lbrace{}s\right\rbrace \equiv \left\lbrace{}s_i^X \;\vert\; i \in \Omega_a, X\in{}\Omega_t\right\rbrace,


where :math:`s_i^X=1` if site :math:`i` is occupied by element :math:`X` and
:math:`s_i^X=0` otherwise. The :math:`s_i^X` are uncorrelated
Bernoulli random variables with probabilities :math:`\mathrm{Pr}(s_i^X=1)=c^X`,
where :math:`c^X` is the concentration of element :math:`X`. In the following,
:math:`\langle \bullet \rangle` denotes the expectation value. If the occupation
variables at sites :math:`i` and :math:`j` (:math:`i\neq{}j`) are uncorrelated,
then

.. math::
    :label: equ:nocorr

    \left \langle s_i^Xs_j^Y \right \rangle = c^Xc^Y. 

The total energy is

.. math::
   :label: equ:etotal

   E\left( \left\lbrace{}s\right\rbrace, \left\lbrace{}r\right\rbrace  \right) 
   &= 
   \sum_i^{N_a}\sum_X^{{N_t}}s_i^X\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} s_j^Y \phi^{XY}\left(r_{ij}\right) \\
   &+ 
   \sum_i^{N_a}\sum_X^{{N_t}}s_i^X U^{X}\left(\rho_{i}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right)\right), \quad\text{with} \\
   \rho_{i}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right) &= \sum_{j\neq{}i}^{{N_a}}\sum_Y^{N_t}s_j^Y g^{XY}\left(r_{ij}\right),


where :math:`r_{ij}` is the distance between sites :math:`i` and :math:`j`,
:math:`\left\lbrace{}r\right\rbrace\equiv\left\lbrace{}r_{ij}\;\vert{}\;i\in{}\Omega_a,j\in\Omega_a\right\rbrace`
is the set of site distances, 
:math:`\phi^{XY}` is the pair potential function of elements :math:`X` and
:math:`Y` (symmetric, i.e. :math:`\phi^{XY}=\phi^{YX}`), 
:math:`U^{X}` is the embedding energy functional of element
:math:`X`, :math:`\rho_i` is the total electron density of the atom at site
:math:`i`, and :math:`g^{XY}` is the contribution from element :math:`Y` to the
total electron density at site :math:`i` if it is occupied by a :math:`X`-atom.

This form of the total energy can represent both :code:`eam/fs` and :code:`eam/alloy`
potentials. In the case of :code:`eam/fs` potentials, there is one :math:`g^{XY}`
for every possible element pairing :math:`XY`. Generally :math:`g^{XY}\neq{}g^{YX}`
if :math:`X\neq{}Y`. In the case of :code:`eam/alloy` potentials :math:`g^{XY}`
depends only on the element :math:`Y`, hence :math:`g^{XY}\rightarrow{}g^{Y}`,
and accordingly there is one :math:`g^{Y}` per *element*.


Average electron density at site :math:`i`
------------------------------------------

The expression for :math:`\rho_i` in :eq:`equ:etotal` is valid for
the particular case where we know that site :math:`i` is occupied
by element :math:`X`. This information is provided by :math:`s_i^X`
in the sum containing :math:`U^X`. A more general expression is

.. math::
    :label: equ:rhoxunknown

    \rho_i \left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right) = \sum_{j\neq{}i}^{{N_a}}\sum_X^{{N_t}}s_i^X\sum_Y^{{N_t}} s_j^Yg^{XY}\left(r_{ij}\right).

The average of this expression with respect to occupation variables is the 
average electron density at site :math:`i`, 

.. math::
   :label: equ:avgedens

   \bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right) \equiv \left \langle \rho_i \left(\left\lbrace{}r\right\rbrace\right) \right \rangle = \sum_{j\neq{}i}^{{N_a}}\sum_X^{{N_t}}\sum_Y^{{N_t}} c^X c^Y g^{XY}\left(r_{ij}\right),

where :eq:`equ:bernoulliprod` was used.


Average embedding energy 
------------------------

From :eq:`equ:etotal`, the total embedding energy is 

.. math::
    :label: equ:uembed

    E_\mathrm{embed}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right) = \sum_i^{{N_a}}\sum_X^{{N_t}}s_i^X U^X\left(\rho_i\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)\right).

We would like to calculate the expectation value of :eq:`equ:uembed` with
respect to occupation variables,

.. math::
    :label: equ:expvalue

    \left \langle E_\mathrm{embed}\left( \left\lbrace{}s\right\rbrace, \left\lbrace{}r\right\rbrace \right) \right \rangle  = 
    \sum_i^{{N_a}}\sum_X^{{N_t}} 
    \left \langle s_i^X U^X\left(\rho_i\left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)\right) \right \rangle. 


First, we expand the embedding energy functional at each site :math:`i` in a
Taylor series around the corresponding average electron density :math:`\bar{\rho}_i`,

.. math::
    :label: equ:taylorexpansion

    U^X\left(\rho_i\left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)\right) = U^X\left(\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right)+\frac{\partial U^X}{\partial \rho_i}\bigg\vert_{\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)}\left(\rho_i \left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)- \bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right) + \dots, 

where terms of second order and higher are subsequently ignored.


By plugging the leading terms into :eq:`equ:expvalue`, we get

.. math::
    :label: equ:taylorseriesplugged

    \left \langle E_\mathrm{embed}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right) \right \rangle = 
    \sum_i^{{N_a}}\sum_X^{{N_t}} 
    \left \langle s_i^X 
    \left(U^X\left(\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right)+\frac{\partial U^X}{\partial \rho_i}\bigg\vert_{\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)}\left(\rho_i \left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)- \bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right) \right) 
    \right  \rangle. 

The expectation value of a sum of two random variables is the sum of the
respective expectation values. The expectation value of the first term in
equation :eq:`equ:taylorseriesplugged` is

.. math::
    :label: equ:alloyform

    \sum_i^{{N_a}}\sum_X^{{N_t}} 
    \left \langle s_i^X 
    U^X\left(\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right) 
    \right \rangle
    &= 
    \sum_i^{{N_a}}\sum_X^{{N_t}} 
    \left \langle s_i^X \right \rangle
    U^X\left(\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right) 
    \\
    &=\sum_i^{{N_a}}\sum_X^{{N_t}} 
     c^X 
    U^X\left(\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right). 


The average of the second term in :eq:`equ:taylorseriesplugged` is

.. math::
    :label: equ:derivativeterm

    \newcommand{\longderiv}{\frac{\partial U^X}{\partial
    \rho_i}\bigg\vert_{\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)}} 
    &\sum_i^{{N_a}}\sum_X^{{N_t}} 
    \left \langle s_i^X 
    \longderiv
    \left(\rho_i \left(\left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace\right)- \bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)\right)
    \right \rangle \\
    &= 
    \sum_i^{{N_a}}\sum_X^{{N_t}} \left \langle s_i^X \longderiv 
    \left(   \sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} s_j^Yg^{XY}\left(r_{ij}\right) -\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)  \right) \right \rangle \\
    &= 
     \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv  \left \langle 
      s_i^X\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} s_j^Yg^{XY}\left(r_{ij}\right) -s_i^X\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)  \right \rangle  \\ 
    &=
      \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left( \left \langle
      s_i^X\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} s_j^Yg^{XY}\left(r_{ij}\right) \right \rangle-\left \langle s_i^X\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)  \right \rangle     \right) \\
    &= 
    \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left(
     c^X \sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} c^Yg^{XY}\left(r_{ij}\right)- c^X\bar{\rho}_i  \right) \\
    &= 
    \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left(
     c^X \sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} c^Yg^{XY}\left(r_{ij}\right)-c^X
     \sum_{j\neq{}i}^{{N_a}}\sum_Z^{{N_t}}\sum_Y^{{N_t}} c^Z c^Y g^{XY}\left(r_{ij}\right) \right), 


The two terms in the last equation do not cancel, because the second
term has an additional sum over :math:`Z` with weight :math:`c^Z`.
Notice that this is a consequence of the particular form of :code:`eam/fs`,
where the electron density contributions depend on element pairing. 
In the case of :code:`eam/alloy`, the contribution are independent 
of :math:`X` (:math:`g^{XY}\rightarrow{}g^{Y}`), and the average
electron density at site :math:`i` is 
:math:`\bar{\rho}_i=\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}}c^Yg^Y(r_{ij})`.
Therefore, the two terms in the last line of :eq:`equ:derivativeterm`
cancel, and the average embedding energy is :eq:`equ:alloyform`.


Let's manipulate :eq:`equ:derivativeterm` a bit. We can introduce a
dummy sum :math:`\sum_X^{{N_t}}1/{N_t}\equiv{}1` and rearrange

.. math::

    \newcommand{\longderiv}{\frac{\partial U^X}{\partial
    \rho_i}\bigg\vert_{\bar{\rho}_i\left(\left\lbrace{}r\right\rbrace\right)}} 
    &\sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left(
    c^X \sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} c^Yg^{XY}\left(r_{ij}\right)-c^X
    \sum_{j\neq{}i}^{{N_a}}\sum_X^{{N_t}}\sum_Y^{{N_t}} c^X c^Y g^{XY}\left(r_{ij}\right) \right) \\
    &=
    \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left(
    c^X \sum_X^{{N_t}}\frac{1}{{N_t}}\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} c^Yg^{XY}\left(r_{ij}\right)-c^X
    \sum_{j\neq{}i}^{{N_a}}\sum_X^{{N_t}}\sum_Y^{{N_t}} c^X c^Y g^{XY}\left(r_{ij}\right) \right) \\
    &=
    \sum_i^{{N_a}}\sum_X^{{N_t}} \longderiv \left(
    c^X \sum_X^{{N_t}}\frac{1}{{N_t}}\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}} c^Yg^{XY}\left(r_{ij}\right)-c^X
    \sum_Z^{{N_t}}c^Z\sum_{j\neq{}i}^{{N_a}}\sum_Y^{{N_t}}  c^Y g^{ZY}\left(r_{ij}\right) \right).

We see that the two terms will cancel if :math:`c^Z=1/{{N_t}}\;\forall\;Z`
i.e. if the alloy is an equicomposition alloy.

The :code:`eam/fs` A-atom potential implemented in :code:`matscipy` ignores the
term :eq:`equ:derivativeterm`, i.e. the linear term of the Taylor series in
:eq:`equ:taylorexpansion`. Thus, there is an additional approximation relative
to the A-atom for :code:`eam/alloy` potentials, where this term vanishes.


A-atom potential functions
--------------------------

Examining :eq:`equ:avgedens`, we can identify the following electron density functions:

.. math::
    :label: edenscontribs

    g^{AX}(r_{ij}) &= \sum_Y^{{N_t}} c^Y g^{YX}\left(r_{ij}\right),\\
    g^{XA}(r_{ij}) &= \sum_Y^{{N_t}} c^Y g^{XY}\left(r_{ij}\right),\quad\text{and}\\
    g^{AA}(r_{ij}) &= \sum_X^{{N_t}}\sum_Y^{{N_t}} c^X c^Y g^{XY}\left(r_{ij}\right) = \sum_X^{{N_t}} c^X g^{XA}(r_{ij}) = \sum_X^{{N_t}} c^X g^{AX}(r_{ij}).


* :math:`g^{AX}` is the contribution from element :math:`X` to the
  total electron density at site :math:`i` if it is occupied by an :math:`A`-atom.

* :math:`g^{XA}` is the contribution from an :math:`A`-atom to the
  total electron density at site :math:`i` if it is occupied by a :math:`X`-atom.

* :math:`g^{AA}` is the contribution from an :math:`A`-atom to the
  total electron density at site :math:`i` if it is occupied by an :math:`A`-atom.

For a :code:`eam/fs` potential table for :math:`N_t` elements,
the above is a set of :math:`2N_t+1` tables.

The embedding energy functional of the :math:`A`-atom is simply the concentration-weighted
average of the functionals of the elements,

.. math:: 
    :label: aatomembed

    U^{A}\left(\rho_{i}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right)\right) = \sum_X^{{N_t}}c^X 
    U^{X}\left(\rho_{i}\left( \left\lbrace{}s\right\rbrace,\left\lbrace{}r\right\rbrace \right)\right).

This adds one more table to the potential.

The pair potential averages are the same as in the :code:`eam/alloy` case, namely

.. math::
    :label: pairpotentials

    \phi^{AX}(r_{ij}) &= \phi^{XA}(r_{ij}) = \sum_Y^{{N_t}} c^Y \phi^{YX}\left(r_{ij}\right),\\
    \phi^{AA}(r_{ij}) &= \sum_X^{{N_t}}\sum_Y^{{N_t}} c^X c^Y \phi^{XY}\left(r_{ij}\right) = \sum_X^{{N_t}} c^X \phi^{XA}(r_{ij}) = \sum_X^{{N_t}} c^X \phi^{AX}(r_{ij}).

Since the pair potential is symmetric with respect to element pairing, averaging 
a :code:`eam/fs` or :code:`eam/alloy` table adds :math:`N_t+1` unique pair 
functions.


References
----------

.. [1] Daw, M. S. & Baskes, M. I. Semiempirical, Quantum Mechanical 
   Calculation of Hydrogen Embrittlement in Metals. 
   Physical Review Letters 50, 1285–1288 (1983).
  
.. [2] Varvenne, C., Luque, A., Nöhring, W. G. & Curtin, W. A. 
   Average-atom interatomic potential for random alloys. 
   Physical Review B 93, 104201 (2016).

.. [3]  Smith, R.W. & Was, G. S. Application of Molecular Dynamics 
   to the Study of Hydrogen Embrittlement in Ni-Cr-Fe Alloys.
   Physical Review B 40, pp. 10332–36 (1989)

.. [4] Finnis M. W. & Sinclair, J. E. A simple empirical N-body potential 
   for transition metals. Philosophical Magazine A 50, 45 (1984).
