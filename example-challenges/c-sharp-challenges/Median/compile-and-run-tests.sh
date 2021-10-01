#!/bin/bash

FILENAME="Median"
TEST_FILENAME="${FILENAME}Test"

# Set to the corresponding files created by your execution of `setup.sh`
NUNIT_PATH="./NUnit.3.13.2/lib/net35/"
NUNIT_LIB="NUnit.3.13.2/lib/net35/nunit.framework.dll"
NUNIT_CONSOLE_RUNNER="./NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"

export MONO_PATH=${NUNIT_PATH}

echo -e "> Compiling...\n" 
mcs ${FILENAME}.cs ${TEST_FILENAME}.cs -target:library -r:${NUNIT_LIB} -out:${TEST_FILENAME}.dll

echo -e "> Executing tests...\n" 
mono ${NUNIT_CONSOLE_RUNNER} ${TEST_FILENAME}.dll -noresult

