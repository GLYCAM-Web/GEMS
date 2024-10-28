# Glycan Prep and Minimization

This directory contains files relevant to normal builds using the new
versions of the online tools at GLYCAM-Web.  The new versions will go
live during March of 2021.  If your glycan was built after this time,
you should be able to find build info for it in this repo.

## The general build process is as follows

1. GEMS and GMML build the initial glycan structure as an OFF file.
   As part of the build process, major clashes between glycan branches
   are resolved.
2. AMBER PRMTOP and INPCRD files are generated from that OFF file
   using tleap (gas-phase).
3. The structure is minimized in the gas-phase using a dielectric 
   appropriate to water.
4. CPPTRAJ and tleap are used to make two sets of PRMTOP and INPCRD 
   files from the gas-phase minimization output.  One set is solvated 
   with TIP3P waters, and the other, with TIP5P.
5. The waters and the glycan's hydrogens are then minimized.  First
   TIP3P, then TIP5P.
6. The resulting files, as well as all scripts used to generate them, 
   are offered for download on the site.


Required input:  structure.off

Control script:  Minimize.bash

structure.off : 
    This file should contain a glycan in a reasonable geometry with any
    major clashes resolved.  This corresponds to step 1, above. 
    File format:  AMBER OFF

Minimize.bash : 
    This script performs steps 2-5, above.
    File format:  BASH
