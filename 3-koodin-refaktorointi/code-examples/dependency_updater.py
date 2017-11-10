############################################################################################
#
# Sampo Siltanen
# 2017
#
# This script crawls through Visual Studio build intermediate target folder
# and fetches the .obj file names for Debug and Release run modes and
# adds them to additional dependencies in .vsxproj file
#
# This software asks for four parameters
#   1. Project file name to be updated
#   2. Path to the project file
#   3. Path to Debug .obj files
#   4. Path to Release .obj files
#
# User may give these parameters as command line parameters in that order or
# otherwise the software asks for them during run time.
#
# Use of this software is at the user's own risk.
# I do not take any responsibility for mishaps caused by the use of this software.
#
#############################################################################################

from os.path import isdir, join, splitext
from os import listdir
import sys
import xml.etree.ElementTree as ET

logging = True

def die(complaint):
    print(complaint, file=sys.stderr)
    sys.exit(1)

def log(message):
    if logging: print(message)

def main(args):
    if (len(args) < 5): die('Not enough parameters provided. Exiting...')
    _, projectname, projectpath, debugpath, releasepath = args
    log('Project name: ' + projectname)
    log('Path to project file: ' + projectpath)
    log('Path to debug .obj files: ' + debugpath)
    log('Path to release .obj files: ' + releasepath)

    if not isdir(projectpath): die('Oops, invalid project path. Exiting...')
    if isdir(debugpath):
        updateProjectFile(projectname, projectpath, debugpath, 'Debug')
    else: die('Oops, no debug folder found')
    if isdir(releasepath):
        updateProjectFile(projectname, projectpath, releasepath, 'Release')
    else: die('Oops, no release folder found')

# Updates the project file with .obj file names found from the given folder
# Expects projectname string, path to project file string, path to .obj files string and [Debug|Release] string
def updateProjectFile(projectname, projectpath, objpath, runMode):
    objfiles = [file for file in listdir(objpath)
                if file.endswith('.obj') and file != 'main.obj']
    projectfile = join(projectpath, projectname.lower() + '.vcxproj')
    ET.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
    updated, newtree = updated_project(ET.parse(projectfile), objfiles, runMode)
    if updated:
        newtree.write(projectfile, encoding="utf-8", xml_declaration=True)
        log('Updated ' + runMode + ' dependencies in ' + projectname)
    else:
        log(runMode + ' dependencies in ' + projectname + ' were already up-to-date')

def updated_project(tree, objfiles, runMode):
    root = tree.getroot()
    fileUpdated = False
    for itemDefinitionGroup in root.iter('{http://schemas.microsoft.com/developer/msbuild/2003}ItemDefinitionGroup'):
        if runMode not in itemDefinitionGroup.attrib.get('Condition'): continue
        for additionalDependencies in itemDefinitionGroup.iter('{http://schemas.microsoft.com/developer/msbuild/2003}AdditionalDependencies'):
            changed, newdeps = updated_deps(additionalDependencies.text, objfiles)
            if changed:
                additionalDependencies.text = newdeps
                fileUpdated = True
    return (fileUpdated, tree)

def is_additional(fname): return splitext(fname)[1] not in ['.lib', '.obj']

def updated_deps(olddeps, objfiles):
    dependencies = olddeps.split(';')
    newdeps = ';'.join([f for f in dependencies if f.endswith('.lib')]
                    + objfiles
                    + [f for f in dependencies if is_additional(f)])
    return (newdeps != olddeps, newdeps)

###########################################
#
# Script entry point
#
###########################################
if (__name__ == '__main__'):
    import sys
    main(sys.argv)
