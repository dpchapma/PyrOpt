#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _NMDA_CA1_pyr_SC_reg(void);
extern void _cacum_reg(void);
extern void _cagk_reg(void);
extern void _cal2_reg(void);
extern void _can2_reg(void);
extern void _cat_reg(void);
extern void _h_reg(void);
extern void _kad_reg(void);
extern void _kaprox_reg(void);
extern void _kca_reg(void);
extern void _kdrca1_reg(void);
extern void _kmb_reg(void);
extern void _na3_reg(void);
extern void _vecevent_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," ./mechanisms/NMDA_CA1_pyr_SC.mod");
    fprintf(stderr," ./mechanisms/cacum.mod");
    fprintf(stderr," ./mechanisms/cagk.mod");
    fprintf(stderr," ./mechanisms/cal2.mod");
    fprintf(stderr," ./mechanisms/can2.mod");
    fprintf(stderr," ./mechanisms/cat.mod");
    fprintf(stderr," ./mechanisms/h.mod");
    fprintf(stderr," ./mechanisms/kad.mod");
    fprintf(stderr," ./mechanisms/kaprox.mod");
    fprintf(stderr," ./mechanisms/kca.mod");
    fprintf(stderr," ./mechanisms/kdrca1.mod");
    fprintf(stderr," ./mechanisms/kmb.mod");
    fprintf(stderr," ./mechanisms/na3.mod");
    fprintf(stderr," ./mechanisms/vecevent.mod");
    fprintf(stderr, "\n");
  }
  _NMDA_CA1_pyr_SC_reg();
  _cacum_reg();
  _cagk_reg();
  _cal2_reg();
  _can2_reg();
  _cat_reg();
  _h_reg();
  _kad_reg();
  _kaprox_reg();
  _kca_reg();
  _kdrca1_reg();
  _kmb_reg();
  _na3_reg();
  _vecevent_reg();
}
