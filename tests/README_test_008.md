Test 008 is complicated.  It checks serveral details of sequence builds.  Some of these details only appear after
several prior steps have been completed.  

To simplify things somewhat, Test 008 checks the prior steps as well.

Full comprehension of this test requires some understanding of carbohydrate modeling (though not necessarily of 
carbohydrates themselves).

This test probably does too much all at once, at least by normal separation-of-concerns standards, but separating
the concerns, while advantageous in some ways, will not necessarily make what is happening any easier to understand
or to troubleshoot.

Importantly, one main purpose of Test 008 is to ensure that the resulting directory structures are correct.  For 
this reason, the `correct_outputs` folder contains entire directory trees.

## The Seven Steps In Test 008

0. Evaluation - tests execution of a sequence evaluation.  This sequence has multiple possible conformers because
   that simplifies the following tests.  This test produces the default structure.
1. Build The First Two - tests execution when a user has requested two structures, one of which is the default.
   In this test, the default already exists.  That is, the output from step 0 is not deleted.
2. Build The Second Two - here, the user has requested two previously un-made structures, and neither is the default.
3. Build The Third Four - the user has requested two existing structures plus two more. One of the existing structures
   is the default structure.
4. Evaluate Again - this tests that a second evaluation, even with existing structures, is handled well.  The existing
   structures are not deleted for this test.
5. Build Two With No Default - tests a request of two structures when the default has not been requested and 
   does not already exist.  _All previous structures are deleted for this test._
6. Build Single-Conformer - this tests that any changes to the multi-conformer processing did not affect the
   processing for single-conformer structures.  Note that this does test something different from Test 015.
   The difference between that test and this one is in the form of the JSON input.  
   _All previous structures are deleted for this test._

## Locations Of The Code

As of the moment of this writing, with many changes still needed, the code for this test is over 1000 lines
in total. For sanity, the code is split over serveral files in subdirectories.  It takes some work to follow
the logic, but putting everything into one god script would not make things easier.

There are some places where things could be made clearer or more uniform, but it is mostly understandable.

All paths are relative to `$GEMSHOME/tests`.

- `008.test.multi-conformer-builds.sh` : the main control script
- `sub_parts/008.*` : control scripts for each of the seven sub-tests
- `inputs/00.*` : the JSON files used as input to the seven sub-tests
- `correct_outputs/008.*.testing-arrays.bash` : the parts that run the tests after the code completes
- `correct_outputs/008_reference` : correct directory trees for each of the seven sub-tests.  These directory trees
  start at the 'cb' directory and should contain ony two sub-directories, 'Builds' and 'Sequences'.
- `correct_outputs/008_reference_data.bash` : file containing directory tree data to use for testing (see notes below).

Notes regarding the 008 reference directories:

- Sub-directories in the Builds directory will be unique, random, UUID hashes.  They cannot be set or predicted.
  For this reason, they must be declared in `correct_outputs/008-directory-hashes.bash` so that the tests know 
  where to find information.  It would, technically, be possible to figure it out based on entries in the Sequences
  directory.  But, that assumes that the Sequences entries are correct, and that is part of what is being tested.
- Sub-directories in the Sequences directory will be UUID hashes generated from the carbohydrate sequences.  They
  are not expected to change unless there is a bug or if the hash generation method changes.  
- Information further down in the Sequences directories will link to the sub-directories in Builds.
