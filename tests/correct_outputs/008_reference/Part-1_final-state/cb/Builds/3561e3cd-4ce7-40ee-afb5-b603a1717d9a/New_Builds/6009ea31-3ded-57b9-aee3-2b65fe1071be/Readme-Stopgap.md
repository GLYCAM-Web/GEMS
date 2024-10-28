# Stop-Gap measures file

This file contains a description of a stop-gap measure that was taken and 
some hints as to how it might be better resolved.

## Issue #89 in the website repo on github

Unsaturated uronates (dUA's) were not being processed properly.  They 
needed the information found in this file:

    frcmod.glycam06_intraring_doublebond_protonatedacids

### What should happen

One or more of these:

- This file should be added to the AMBER source code so that it can be sourced
during regular builds.
- The contents of this file should be added to the regular params and the 
params version incremented accordingly.

Either of these should also require the dUA prep files to be added to AMBER's
source tree.

### What ideally will also happen

We need to make a git repo for all our parameters.  That will take time 
and care.

### What happened instead

The file mentioned above was copied into this location in the `MD_Utils` repo:

    MD_Utils/protocols/Glycan/Prep_and_Minimization

A line was added to each `*.leapin` file so that its contents would be loaded.
