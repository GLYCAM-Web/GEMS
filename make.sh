#!/bin/bash

: << '=cut'
COMMENT - Requirements and Known Issues.

# Python 3 is required.
# These are known to work: 3.6.6 :: Anaconda custom and 3.7.3.

# Python.h is required.
# In some cases Python.h does not live in PYTHON_HOME.
# Users can run this command to find it and set PYTHON_HEADER_HOME accordingly:
## python3-config --cflags

# Based on practice SWIG version 3 or later is recommended.
# These are known to work: 3.0.10 and 3.0.12.
# These are known to fail: 2.0.10.
# SWIG Version 2.0.10 fails due to this issue:
# https://sourceforge.net/p/swig/bugs/1331/
# Here's part of a typical failure:
##gmml_wrap.cxx: In function 'PyObject* _wrap_pdbmatrixn_vector_vector_erase__SWIG_0(PyObject*, PyObject*)':
##gmml_wrap.cxx:202628:30: error: no matching function for call to 'std::vector<std::vector<PdbFileSpace::PdbMatrixNCard*>
##>::erase(SwigValueWrapper<__gnu_cxx::__normal_iterator<std::vector<PdbFileSpace::PdbMatrixNCard*>*, std::vector<std::vector<PdbFileSpace::PdbMatrixNCard*> > > >>&)'
##   result = (arg1)->erase(arg2);

=cut

################################################################
#########                 FUNCTIONS                    #########
################################################################

check_pythonhome() {
    if [ -z "$PYTHON_HOME" ]; then
        printf "\nError:  PYTHON_HOME is not set.\n"
        printf "Set PYTHON_HOME to the location of Python.h for a python 3 installation.\n"
        printf "Searching for locations of Python.h:\n"
        if locate_test="$(type -p "locate")" || [ -z "locate" ]; then
            num_Pythons=`locate -ce Python.h`
            if [[ $num_Pythons -gt 0 ]]; then
            {
                printf "Here are the current locations of Python.h on your machine:\n\n"
                locate -e Python.h
                printf "\n"
            }
            else
                printf "locate could not find any instances of Python.h\n"

            fi
        fi
        echo "Exiting."
        exit 1
    elif [ ! -d $PYTHON_HOME ]; then
        guess=`dirname $PYTHON_HOME`
        printf "\nError:  PYTHON_HOME is not set to a directory.\n"
        printf "It is currently %s\n" $PYTHON_HOME
        printf "Perhaps try     %s\n" $guess
        echo "Exiting."
        exit 1
    fi
}

get_numprocs() {
    if [ -z "$GEMSMAKEPROCS" ]; then
        NMP=4
    elif ! [[ $GEMSMAKEPROCS =~ ^[0-9]+$ ]] ; then
        echo "Warning:  GEMSMAKEPROCS is not a valid integer; setting to 4"
        NMP=4
    elif [ "$GEMSMAKEPROCS" -eq "0" ] ; then
        echo "Warning:  GEMSMAKEPROCS cannot be zero; setting to 4"
        NMP=4
    else
        NMP=$GEMSMAKEPROCS
    fi
}

check_gemshome() {
    if [ -z "$GEMSHOME" ]; then
        echo ""
        echo "Error:  GEMSHOME environment variable is not set! It should be set to"
        echo "$1"
        exit 1
    elif [ ! -d $GEMSHOME ]; then
        echo ""
        echo "Error:  GEMSHOME environment variable is set to $GEMSHOME -- this does"
        echo "not appear to be a directory. It should be set to"
        echo "$1"
        exit 1
    elif [ ! "$GEMSHOME" = "$1" -a ! "$GEMSHOME" = "${1}/" ]; then
        #try checking the inode in case there is a problem with symlinks
        if [ `stat -c "%i" $GEMSHOME` != `stat -c "%i" ${1}` ]; then
            echo ""
            echo "Error:  GEMSHOME is expected to be $1 but it is currently"
            echo "$GEMSHOME"
            echo "        This will cause problems!"
            exit 1
        fi
    fi
}

check_gmmldir() {
    if [ ! -d "$1" ]; then
        echo ""
        echo "Error: $1 directory does not exist. If your GEMSHOME is set correctly,"
        echo "it should be here: $1"
        exit 1
    fi
}

check_pull_repo() {
    local repoName="$1"
    local repoURL="$2"
    local baseDir="$3"
    local stableBranch="$4"
    local devBranchName="$5"
    local 
    local theDir="${baseDir}/${repoName}"

    if [ ! -d "${theDir}" ]; then
        mkdir -p ${theDir}
    fi

    if [ "${GW_GRPC_ROLE}" == "Swarm" ]; then
        echo "Swarm deployment detected. ${repoName} should be controlled by upstream processes."
        echo "!!!  NOT ALTERING ${repoName} !!!"
        return 0;
    elif [ "${GW_GRPC_ROLE}" == "Developer" ]; then
        echo "Developer environment detected; pulling ${repoName} from the development branch."
        stableBranch="${devBranchName}"
    else
        stableBranch=""
    fi

    if [ ! -d "${theDir}/.git" ]; then
        echo ""
        echo "${repoName} repo does not exist. Attempting to clone."
        git clone -b ${stableBranch} ${repoURL} ${theDir}
        if [ ! -d "${theDir}/.git" ]; then
            echo ""
            echo "Error: Unable to clone ${repoName}. Some functions will be unavailable."
            echo "You can try again on your own using the following command:"
            echo "git clone -b ${stableBranch} ${repoURL} ${theDir}"
            return 1
        fi
        echo "Cloning of ${repoName} was successful"
        return 0
    fi

    # if on correct branch, pull and return
    local currentBranch=$(cd ${theDir} && git branch --show-current)
    if [ "${currentBranch}" == "${stableBranch}" ]; then
        echo "Attempting to update ${repoName}"
        (cd ${theDir} && git pull)
        local returnValue=$?
        if [ "${returnValue}" != 0 ]; then
            echo ""
            echo "Error! Unable to update ${repoName}."
            echo "You can try again on your own using the command below:"
            echo "cd ${theDir} && git pull origin ${stableBranch}"
            return 1
        else
            return 0
        fi
    else
        echo ""
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "Your ${repoName} repo (${baseDir}/${repoName}) is not on the expected branch."
        echo "    Expected branch:  ${stableBranch}"
        echo "    Current branch:   ${currentBranch}"
        echo ""
        echo "What do you want to do?"
        echo "   p  (pull)       :  Issue 'git pull' in the repo on the current branch"
        echo "   s  (skip)       :  Don't do anything in the repo. Carry on with make."
        echo "   a  (abort)      :  Don't do anything in the repo. Exit make."
        echo "   just hit enter  :  Change to the expected branch and update the repo."
        echo ""
        echo "If you don't know what to do, you should probably just hit enter."
        echo ""
        read -p "Your response:  " branchResponse
        if [[ $branchResponse == [sS] ]]; then
            printf "Skipping update of ${repoName} repo.\n"
            return 0;
        elif [[ $branchResponse == [aA] ]]; then
            printf "Abort!\n"
            exit 1;
        elif [[ $branchResponse == [pP] ]]; then
            printf "Pulling from within the current branch\n"
            (cd ${theDir} && git pull)
            returnValue=$?
            if [ "${returnValue}" != 0 ]; then
                echo ""
                echo "Error! Unable to update ${repoName} within the current branch."
                echo "You can try again on your own using the command below."
                echo "Exiting for now."
                echo ""
                echo "cd ${theDir} && git pull"
                return 1
            else
                return 0
            fi
        else
            echo "Changing to branch ${stableBranch}, ensuring proper upstream, and pulling"
            COMMAND="( cd ${theDir} &&  git branch | grep -q ${stableBranch} )"
            echo "running :  ${COMMAND}"
            if ! eval ${COMMAND} ; then
                echo "The expected branch does not already exist.  Setting it up now."
                COMMAND="( cd ${theDir} \
                    && git remote set-branches --add origin ${stableBranch} \
                    && git fetch \
                    && git checkout -b ${stableBranch} origin/${stableBranch} )"
                eval ${COMMAND}
                returnValue=$?
                if [ "${returnValue}" != 0 ]; then
                    echo ""
                    echo "Error! Unable to change branches and update ${repoName}."
                    echo "You can try again on your own using the command below."
                    echo "Exiting for now."
                    echo ""
                    echo "${COMMAND}"
                    return 1
                else
                    return 0
                fi
            else
                ##  Check out the branch, ensure upstream is tracked properly, then pull
                COMMAND="( cd ${theDir} \
                    && git checkout ${stableBranch} \
                    && git branch -u origin/${stableBranch} \
                    && git pull )"
                eval ${COMMAND}
                returnValue=$?
                if [ "${returnValue}" != 0 ]; then
                    echo ""
                    echo "Error! Unable to update ${repoName}."
                    echo "You can try again on your own using the command below."
                    echo ""
                    echo "${COMMAND}"
                    return 1
                else
                    return 0
                fi
            fi
        fi
    fi
}



################################################################
#########                CHECK SETTINGS                #########
################################################################

gemshome=`pwd`
check_gemshome $gemshome
check_gmmldir $GEMSHOME/gmml
check_gmmldir $GEMSHOME/gmml2
check_pull_repo "MD_Utils" "https://github.com/GLYCAM-Web/MD_Utils.git" "$GEMSHOME/External" "stable" "md-test" 
check_pull_repo "GM_Utils" "https://github.com/GLYCAM-Web/GM_Utils.git" "$GEMSHOME/External" "gm-actual" "gm-test"
get_numprocs

################################################################
#########              CREATE CLIENT HOOKS             #########
################################################################

#Cannot use server side hooks when hosting on git-hub.
#Stuff in .git/hooks is ignored by git.
#Solution: The folder .hooks is tracked by git.
# Copy .hooks to .git/hooks during installation.
cp -r $GEMSHOME/.hooks/* $GEMSHOME/.git/hooks/
# gmml hooks are similarly copied in its make.sh.  SRB Jul 2019.
#I don't think this is ideal, and is perhaps silly. OG Apr 2017.

################################################################
#########                WRITE CONFIG.H                #########
################################################################

# NOTE: Inactive for now

# Store the command
#command=`echo "$0 $*"`

# Write directories into config.h
#printf "# Gems configuration file, created with: %s\n\n" $command > config.h
#printf "###############################################################################\n\n" >> config.h
#printf "# (1) Location of the installation\n\n" >> config.h

#printf "BASEDIR=%s\n" $GEMSHOME >> config.h
#printf "BINDIR=%s/bin\n" $GEMSHOME >> config.h
#printf "TESTDIR=%s/testbin\n" $GEMSHOME >> config.h
#printf "APPDIR=%s/apps\n" $GEMSHOME >> config.h
#printf "HOOKDIR=%s/hooks\n" $GEMSHOME >> config.h
#printf "GMMLDIR=%s/gmml\n" $GEMSHOME >> config.h

#printf "\n###############################################################################\n\n" >> config.h

################################################################
##########               Print help message         ############
################################################################

printHelp()
{
    echo "*************************************************************"
	echo "This make script will both compile and wrap GMML so it is usable."
	echo "by GEMS (this codebase)"
	echo ""
	echo "This is for using GMML and GEMS in isolation! GMML will be wrapped"
	echo "using swig by this script, how you interface with said code is up"
	echo "to you!"
	echo ""
	echo "GEMSHOME should be set to the current GEMS directory."
	printf "*************************************************************\n"
	printf "Please note that once GEMS is built, you can test it by running:\n"
	printf "./test_installation.bash\n"
	printf "*************************************************************\n"
	printf "Options are as follows:\n"
	printf "\t-c\t\t\tClean all files from previous builds\n"
	printf "\t-j <NUM_JOBS>\t\tBuild and wrap GMML with <NUM_JOBS>\n"
	printf "\t-o <O0/O2/OG/debug>\tBuild and wrap GMML using no optimization, 2nd \n\t\t\t\tlevel optimization, or with debug symbols\n"
    printf "\t-h\t\t\tPrint this help message and exit\n"
	printf "*************************************************************\n"
    printf "These environment variables are also used:\n"
    printf "GEMSHOME: The path of the top level directory of GEMS.\n"
    printf "GEMSMAKEPROCS: The parallelism of make; optional, default is 4.\n"
    printf "PYTHON_HOME: The path of the top level directory of Python 3.\n"
    printf "PYTHON_HEADER_HOME: The path of Python.h; optional, default is PYTHON_HOME.\n"
    printf "*************************************************************\n"
	echo "Exiting."
	exit 1
}

################################################################
#########                SET UP DEFAULTS               #########
################################################################

#Changing the following options are for developers.
CLEAN=""
BUILD_LEVEL="O2"
TARGET_MAKE_FILE="Makefile"
#This is not needed, if we are trying to use gems we HAVE to wrap gmml
#WRAP_GMML="-w"

################################################################
#########               COMMAND LINE INPUTS            #########
################################################################
while getopts "j:o:ch" option
do
	case "${option}" in
			j)
				jIn="${OPTARG}"
				if [[ "${jIn}" =~ ^[1-9][0-9]*$ ]]; then
					NMP="${jIn}"
				else
					printHelp
				fi
				;;
			o)
				oIn="${OPTARG}"
				if [ "${oIn}" == "O0" ] || [ "${oIn}" == "no_optimize" ]; then
					CMAKE_BUILD_TYPE_FLAG="O0"
				elif [ "${oIn}" == "O2" ] || [ "${oIn}" == "optimize" ]; then
					CMAKE_BUILD_TYPE_FLAG="O2"
				elif [ "${oIn}" == "debug" ] || [ "${oIn}" == "OG" ]; then
					BUILD_LEVEL="OG"
				else
					printHelp
				fi
				;;
			c)
				CLEAN="-c"
				;;
            h)
                printHelp
                ;;
			*)
				printHelp
				;;
	esac
done

echo "Starting installation of GEMS at `date`".

printf "\nBuilding with these settings:\n"
printf "GEMSHOME: $GEMSHOME\n"
printf "TARGET_MAKE_FILE: $TARGET_MAKE_FILE\n"
printf "CLEAN: $CLEAN\n"
printf "BUILD_LEVEL: $BUILD_LEVEL\n"
printf "WRAP_GMML: TRUE\n\n"

################################################################
#########                  COMPILE GMML                #########
################################################################

cd gmml/ || { echo "ERROR BUILDING GEMS $0 FAILED, CANT CD INTO GMML, EXITING" ; exit 1; }
./make.sh $CLEAN -w -o $BUILD_LEVEL -j $NMP  || { echo "ERROR BUILDING GEMS $0 FAILED, EXITING" ; exit 1; }
cd ../

cd gmml2/ || { echo "ERROR BUILDING GEMS $0 FAILED, CANT CD INTO GMML2, EXITING" ; exit 1; }
./make.sh $CLEAN -w -o $BUILD_LEVEL -j $NMP  || { echo "ERROR BUILDING GEMS $0 FAILED, EXITING" ; exit 1; }
cd ../

################################################################
#########              WRAP UP TO GEMS                 #########
################################################################
#WRAPPING DONE IN GMML! We do want to make a symlink down to our
# wrapped gmml libraries so gems can easily handle this. 
if [[ -f ./gmml/cmakeBuild/gmml.py && -f ./gmml/cmakeBuild/_gmml.so ]]; then
	ln -sf ./gmml/cmakeBuild/gmml.py gmml.py
	ln -sf ./gmml/cmakeBuild/_gmml.so _gmml.so
else
	if [ ! -f ./gmml/cmakeBuild/gmml.py ]; then
		printf "\n!!!WARNING, gmml.py WAS NOT GENERATED!!!\n"
		printf "THIS IS NEEDED FOR US TO INTERACT WITH GMML USING PYTHON!\n"
	fi
	if [ ! -f ./gmml/cmakeBuild/_gmml.so ]; then
		printf "\n!!!WARNING, _gmml.so WAS NOT GENERATED!!!\n"
		printf "THIS IS NEEDED FOR US TO INTERACT WITH GMML USING PYTHON!\n"
		#Note that this can be removed once we remove the hook tests for this
		# Will be leaving in for now, will remove when working on a branch
		# that has a scope that includes this problem
	fi
	printf "\n!!!!WARNING COULD NOT PROPERLY WRAP GMML!!!!\n"
	exit 1
fi

if [[ -f ./gmml2/cmakeBuild/gmml2.py && -f ./gmml2/cmakeBuild/_gmml2.so ]]; then
	ln -sf ./gmml2/cmakeBuild/gmml2.py gmml2.py
	ln -sf ./gmml2/cmakeBuild/_gmml2.so _gmml2.so
else
	if [ ! -f ./gmml2/cmakeBuild/gmml2.py ]; then
		printf "\n!!!WARNING, gmml2.py WAS NOT GENERATED!!!\n"
		printf "THIS IS NEEDED FOR US TO INTERACT WITH GMML USING PYTHON!\n"
	fi
	if [ ! -f ./gmml2/cmakeBuild/_gmml2.so ]; then
		printf "\n!!!WARNING, _gmml2.so WAS NOT GENERATED!!!\n"
		printf "THIS IS NEEDED FOR US TO INTERACT WITH GMML USING PYTHON!\n"
		#Note that this can be removed once we remove the hook tests for this
		# Will be leaving in for now, will remove when working on a branch
		# that has a scope that includes this problem
	fi
fi
#if [[ "$WRAP_GMML" != "no_wrap" ]]; then
#
#    check_pythonhome
#
#    echo ""
#    if [[ -f "gmml.i" ]]; then
#        echo "Wrapping gmml library in python ..."
#        swig -version
#        swig -c++ -python gmml.i
#    else
#        echo "Warning:  Interface file for swig does not exist."
#    fi
#
#    echo ""
#    # In some cases Python.h does not live in PYTHON_HOME; allow user control.
#    if [ -z "$PYTHON_HEADER_HOME" ]; then
#        PYTHON_HEADER_HOME="$PYTHON_HOME"
#    fi
#    PYTHON_FILE="$PYTHON_HEADER_HOME/Python.h"
#    if [ -f $PYTHON_FILE ]; then
#        echo "Using $PYTHON_FILE header file."
#        if [ -f "gmml_wrap.cxx" ]; then
#            echo "Compiling wrapped gmml library in python ..."
#            g++ -std=c++17 -O3 -fPIC -c gmml_wrap.cxx -I"$PYTHON_HEADER_HOME" -I gmml/
#        else
#            echo "Warning:  gmml_wrap.cxx does not exist."
#        fi
#    else
#        echo "Warning:  $PYTHON_FILE not found !"
#    fi
#
#    echo ""
#    if [[ -f "gmml_wrap.o" ]]; then
#        echo "Building python interface ..."
#        g++ -std=c++17 -shared gmml/build/*.o gmml_wrap.o -o _gmml.so
#    else
#        echo "Warning:  gmml python interface has not been compiled correctly."
#    fi
#fi

echo ""
echo "GEMS compilation is finished at `date`".
exit

