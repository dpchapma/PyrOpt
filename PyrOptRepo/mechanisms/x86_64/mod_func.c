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

    fprintf(stderr," NMDA_CA1_pyr_SC.mod");
    fprintf(stderr," cacum.mod");
    fprintf(stderr," cagk.mod");
    fprintf(stderr," cal2.mod");
    fprintf(stderr," can2.mod");
    fprintf(stderr," cat.mod");
    fprintf(stderr," h.mod");
    fprintf(stderr," kad.mod");
    fprintf(stderr," kaprox.mod");
    fprintf(stderr," kca.mod");
    fprintf(stderr," kdrca1.mod");
    fprintf(stderr," kmb.mod");
    fprintf(stderr," na3.mod");
    fprintf(stderr," vecevent.mod");
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
