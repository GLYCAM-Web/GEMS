#!/usr/bin/env bash

## This file should be updated if ever the data in the 008_reference directories is updated.

## These data are used in the 008.*.testing-arrays.bash in the current directory.

## Paths are all relative to the $GEMSHOME/tests directory

Subtest_0_Ref_PDB_UUID="2100a048-5f8c-4646-bd77-a4bd8a17501b"
Subtest_1_Ref_PDB_UUID="3561e3cd-4ce7-40ee-afb5-b603a1717d9a"
Subtest_2_Ref_PDB_UUID="8a36e191-1716-4415-a21d-5c2d3d55e78e"
Subtest_3_Ref_PDB_UUID="1f0c09a5-bbfc-4c13-8f70-e6586d13b715"
## Subtest 4 does not currently need to refer to the saved structure data
Subtest_5_Ref_PDB_UUID="4b237ac4-5c60-408f-9b08-f14496ff353d"
Subtest_6_Ref_PDB_UUID="f2bdcfc5-cfb4-40fa-94bf-5ba06dffea4b"


# The following could be more elegant.  I'm not sure that more elegant is more readable.
declare -A Ref_Path_Prefix
Ref_Path_Prefix=(
	[0]="correct_outputs/008_reference/Part-0_final-state/cb"
	[1]="correct_outputs/008_reference/Part-1_final-state/cb"
	[2]="correct_outputs/008_reference/Part-2_final-state/cb"
	[3]="correct_outputs/008_reference/Part-3_final-state/cb"
	[4]="correct_outputs/008_reference/Part-4_final-state/cb"
	[5]="correct_outputs/008_reference/Part-5_final-state/cb"
	[6]="correct_outputs/008_reference/Part-6_final-state/cb"
)


Subtest_0_Ref_PDB="${Ref_Path_Prefix[0]}/Builds/${Subtest_0_Ref_PDB_UUID}/New_Builds/${defaultStructureConformationID}/min-gas.pdb"
Subtest_1_Ref_PDB_Start="${Ref_Path_Prefix[1]}/Builds/${Subtest_1_Ref_PDB_UUID}/New_Builds"
Subtest_2_Ref_PDB_Start="${Ref_Path_Prefix[2]}/Builds/${Subtest_2_Ref_PDB_UUID}/New_Builds"
Subtest_3_Ref_PDB_Start="${Ref_Path_Prefix[3]}/Builds/${Subtest_3_Ref_PDB_UUID}/New_Builds"
## Subtest 4 does not currently need to refer to the saved structure data
Subtest_5_Ref_PDB_Start="${Ref_Path_Prefix[5]}/Builds/${Subtest_5_Ref_PDB_UUID}/New_Builds"
Subtest_6_Ref_PDB_Start="${Ref_Path_Prefix[6]}/Builds/${Subtest_6_Ref_PDB_UUID}/New_Builds"

