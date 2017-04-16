/*
    Copyright or (c) or Copr. Project-Team S3 (Sound Signals and Systems) and
    Analysis/Synthesis team, Laboratory of Sciences and Technologies of Music and
    Sound (UMR 9912), IRCAM-CNRS-UPMC, 1 place Igor Stravinsky, F-75004 Paris
    * contributors : Antoine Falaize, Thomas Helie,
    * corresponding contributor: antoine.falaize@ircam.fr
    * date: 2016/12/31 12:47:34

    This has been geerated by PyPHS which purpose is to generate C++
    code for the simulation of multiphysics system described by graph structures.

    This software is governed by the CeCILL-B license under French law and
    abiding by the rules of distribution of free software.  You can  use,
    modify and/ or redistribute the software under the terms of the CeCILL-B
    license as circulated by CEA, CNRS and INRIA at the following URL
    "http://www.cecill.info".

    As a counterpart to the access to the source code and  rights to copy,
    modify and redistribute granted by the license, users are provided only
    with a limited warranty  and the software's author,  the holder of the
    economic rights, and the successive licensors  have only  limited liability.

    In this respect, the user's attention is drawn to the risks associated
    with loading,  using,  modifying and/or developing or reproducing the
    software by the user in light of its specific status of free software,
    that may mean  that it is complicated to manipulate,  and  that  also
    therefore means  that it is reserved for developers  and  experienced
    professionals having in-depth computer knowledge. Users are therefore
    encouraged to load and test the software's suitability as regards their
    requirements in conditions enabling the security of their systems and/or
    data to be ensured and,  more generally, to use and operate it in the
    same conditions as regards security.

    The fact that you are presently reading this means that you have had
    knowledge of the CeCILL-B license and that you accept its terms.

    Created on 2016/12/31 12:47:34

    author: Antoine Falaize


===========================================================================

    This file was automatically generated by PyPHS, date 2017/04/16 12:14:17.

    It contains the code for the simulation of system 'CORE'.

===========================================================================
*/


#ifndef CORE_H
#define CORE_H

#include "iostream"
#include "vector"
#include "math.h"

# include "data.h"

#include </Users/Falaize/Documents/DEV/c++/bibliotheques/eigen/Eigen/Dense>

using namespace std;
using namespace Eigen;

class CORE {

// PUBLIC    
    public:
    void update(vector<double> &, vector<double> &);
    
    // Acessors to Arguments, return vector<double>
    
    vector<double> x_vector() const;
    vector<double> xl_vector() const;
    vector<double> xnl_vector() const;
    vector<double> dx_vector() const;
    vector<double> dxl_vector() const;
    vector<double> dxnl_vector() const;
    vector<double> w_vector() const;
    vector<double> wl_vector() const;
    vector<double> wnl_vector() const;
    vector<double> u_vector() const;
    vector<double> p_vector() const;
    vector<double> v_vector() const;
    vector<double> vl_vector() const;
    vector<double> vnl_vector() const;
    
    // Acessors to Arguments, return Matrix<double, n, m>
    
    Matrix<double, 12, 1> x() const;
    Matrix<double, 11, 1> xl() const;
    Matrix<double, 1, 1> xnl() const;
    Matrix<double, 12, 1> dx() const;
    Matrix<double, 11, 1> dxl() const;
    Matrix<double, 1, 1> dxnl() const;
    Matrix<double, 0, 0> w() const;
    Matrix<double, 0, 0> wl() const;
    Matrix<double, 0, 0> wnl() const;
    Matrix<double, 1, 1> u() const;
    Matrix<double, 0, 0> p() const;
    Matrix<double, 12, 1> v() const;
    Matrix<double, 11, 1> vl() const;
    Matrix<double, 1, 1> vnl() const;
    
    // Mutators for Arguments, type = vector<double>
    
    void set_x(vector<double> &);
    void set_xl(vector<double> &);
    void set_xnl(vector<double> &);
    void set_dx(vector<double> &);
    void set_dxl(vector<double> &);
    void set_dxnl(vector<double> &);
    void set_w(vector<double> &);
    void set_wl(vector<double> &);
    void set_wnl(vector<double> &);
    void set_u(vector<double> &);
    void set_p(vector<double> &);
    void set_v(vector<double> &);
    void set_vl(vector<double> &);
    void set_vnl(vector<double> &);
    
    // Mutators for Arguments, type = Matrix<double, n, m>
    
    void set_x(Matrix<double, 12, 1> &);
    void set_xl(Matrix<double, 11, 1> &);
    void set_xnl(Matrix<double, 1, 1> &);
    void set_dx(Matrix<double, 12, 1> &);
    void set_dxl(Matrix<double, 11, 1> &);
    void set_dxnl(Matrix<double, 1, 1> &);
    void set_w(Matrix<double, 0, 0> &);
    void set_wl(Matrix<double, 0, 0> &);
    void set_wnl(Matrix<double, 0, 0> &);
    void set_u(Matrix<double, 1, 1> &);
    void set_p(Matrix<double, 0, 0> &);
    void set_v(Matrix<double, 12, 1> &);
    void set_vl(Matrix<double, 11, 1> &);
    void set_vnl(Matrix<double, 1, 1> &);
    
    // Functions Results Accessors
    
    Matrix<double, 11, 11> jacFll() const;
    Matrix<double, 1, 11> jacFnll() const;
    Matrix<double, 11, 1> Gl() const;
    Matrix<double, 1, 1> Gnl() const;
    Matrix<double, 11, 1> jacGlnl() const;
    Matrix<double, 1, 1> jacGnlnl() const;
    Matrix<double, 12, 1> dxH() const;
    Matrix<double, 0, 0> z() const;
    Matrix<double, 1, 1> y() const;
    
    // Functions Results Accessors
    
    vector<double> jacFll_vector() const;
    vector<double> jacFnll_vector() const;
    vector<double> Gl_vector() const;
    vector<double> Gnl_vector() const;
    vector<double> jacGlnl_vector() const;
    vector<double> jacGnlnl_vector() const;
    vector<double> dxH_vector() const;
    vector<double> z_vector() const;
    vector<double> y_vector() const;
    
    // Oprations Results Accessors
    
    Matrix<double, 12, 1> ud_x() const;
    Matrix<double, 11, 11> ijacFll() const;
    Matrix<double, 11, 1> ud_vl() const;
    Matrix<double, 1, 1> save_Fnl() const;
    double res_Fnl() const;
    Matrix<double, 1, 1> Fnl() const;
    Matrix<double, 1, 1> jacFnl() const;
    Matrix<double, 1, 1> ijacFnl() const;
    Matrix<double, 1, 1> ud_vnl() const;
    double step_Fnl() const;
    
    // Oprations Results Accessors
    
    vector<double> ud_x_vector() const;
    vector<double> ud_vl_vector() const;
    vector<double> save_Fnl_vector() const;
    vector<double> Fnl_vector() const;
    vector<double> ud_vnl_vector() const;
    
    // Default Constructor
    
    CORE();
    
    // Constructor with vector state initalization
    
    CORE(vector<double> &);
    
    // Constructor with matrix state initalization
    
    CORE(Matrix<double, 12, 1> &);
    
    // Default Destructor
    
    ~CORE();


// PRIVATE    
    private:
    
    // Parameters
    
    const unsigned int subs_ref = 0;
    
    const double * beamK2 = & subs[subs_ref][0];
    const double * beamM4 = & subs[subs_ref][1];
    const double * A = & subs[subs_ref][2];
    const double * beamM3 = & subs[subs_ref][3];
    const double * beamalpha2 = & subs[subs_ref][4];
    const double * beamalpha3 = & subs[subs_ref][5];
    const double * beamM2 = & subs[subs_ref][6];
    const double * beamalpha4 = & subs[subs_ref][7];
    const double * beamM0 = & subs[subs_ref][8];
    const double * beamK1 = & subs[subs_ref][9];
    const double * K = & subs[subs_ref][10];
    const double * M = & subs[subs_ref][11];
    const double * L = & subs[subs_ref][12];
    const double * beamalpha0 = & subs[subs_ref][13];
    const double * beamA2 = & subs[subs_ref][14];
    const double * beamK0 = & subs[subs_ref][15];
    const double * f_s = & subs[subs_ref][16];
    const double * beamA4 = & subs[subs_ref][17];
    const double * beamM1 = & subs[subs_ref][18];
    const double * beamA3 = & subs[subs_ref][19];
    const double * beamA0 = & subs[subs_ref][20];
    const double * B = & subs[subs_ref][21];
    const double * beamA1 = & subs[subs_ref][22];
    const double * beamK4 = & subs[subs_ref][23];
    const double * beamK3 = & subs[subs_ref][24];
    const double * beamalpha1 = & subs[subs_ref][25];
    
    // Arguments
    
    Matrix<double, 25, 1> args;
    
    double * xbeamK4 = & args(0, 0);
    double * xbeamK3 = & args(1, 0);
    double * xbeamK2 = & args(2, 0);
    double * xbeamK1 = & args(3, 0);
    double * xbeamK0 = & args(4, 0);
    double * xbeamM0 = & args(5, 0);
    double * xbeamM1 = & args(6, 0);
    double * xbeamM2 = & args(7, 0);
    double * xbeamM3 = & args(8, 0);
    double * xbeamM4 = & args(9, 0);
    double * xmass = & args(10, 0);
    double * qfelt = & args(11, 0);
    double * dxbeamK4 = & args(12, 0);
    double * dxbeamK3 = & args(13, 0);
    double * dxbeamK2 = & args(14, 0);
    double * dxbeamK1 = & args(15, 0);
    double * dxbeamK0 = & args(16, 0);
    double * dxbeamM0 = & args(17, 0);
    double * dxbeamM1 = & args(18, 0);
    double * dxbeamM2 = & args(19, 0);
    double * dxbeamM3 = & args(20, 0);
    double * dxbeamM4 = & args(21, 0);
    double * dxmass = & args(22, 0);
    double * dqfelt = & args(23, 0);
    double * uinput = & args(24, 0);
    
    // Functions Results Definitions
    
    Matrix<double, 11, 11> _jacFll;
    Matrix<double, 1, 11> _jacFnll;
    Matrix<double, 11, 1> _Gl;
    Matrix<double, 1, 1> _Gnl;
    Matrix<double, 11, 1> _jacGlnl;
    Matrix<double, 1, 1> _jacGnlnl;
    Matrix<double, 12, 1> _dxH;
    Matrix<double, 0, 0> _z;
    Matrix<double, 1, 1> _y;
    
    // Functions Results Updates
    
    void jacFll_update();
    void jacFnll_update();
    void Gl_update();
    void Gnl_update();
    void jacGlnl_update();
    void jacGnlnl_update();
    void dxH_update();
    void z_update();
    void y_update();
    
    // Operations Results Definition
    
    Matrix<double, 12, 1> _ud_x;
    Matrix<double, 11, 11> _ijacFll;
    Matrix<double, 11, 1> _ud_vl;
    Matrix<double, 1, 1> _save_Fnl;
    double _res_Fnl;
    Matrix<double, 1, 1> _Fnl;
    Matrix<double, 1, 1> _jacFnl;
    Matrix<double, 1, 1> _ijacFnl;
    Matrix<double, 1, 1> _ud_vnl;
    double _step_Fnl;
    
    // Oprations Results Updates
    
    void ud_x_update();
    void ijacFll_update();
    void ud_vl_update();
    void save_Fnl_update();
    void res_Fnl_update();
    void Fnl_update();
    void jacFnl_update();
    void ijacFnl_update();
    void ud_vnl_update();
    void step_Fnl_update();
    
    // Initialization
    
    void init();
};

#endif /* CORE_H */
