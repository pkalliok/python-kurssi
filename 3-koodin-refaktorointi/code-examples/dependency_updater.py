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

from os.path import isdir, join
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

    projectname = args[1]
    log('Project name: ' + projectname)

    projectpath = args[2]
    log('Path to project file: ' + projectpath)
    if not isdir(projectpath): die('Oops, invalid project path. Exiting...')

    debugpath = args[3]
    log('Path to debug .obj files: ' + debugpath)
    if isdir(debugpath):
        updateProjectFile(projectname, projectpath, debugpath, 'Debug')
    else: die('Oops, no debug folder found')

    releasepath = args[4]
    log('Path to release .obj files: ' + releasepath)
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
        #Find additional dependencies
        for additionalDependencies in itemDefinitionGroup.iter('{http://schemas.microsoft.com/developer/msbuild/2003}AdditionalDependencies'):
            changed, newdeps = updated_deps(additionalDependencies.text, objfiles)
            if changed:
                additionalDependencies.text = newdeps
                fileUpdated = True
    return (fileUpdated, tree)

def updated_deps(olddeps, objfiles):
    #Split dependencies into list
    dependencies = olddeps.split(';')
    #Separate dependency types
    libs = [ x for x in dependencies if '.lib' in x ]
    additional = [ x for x in dependencies if '.lib' not in x and '.obj' not in x ]
    #Append items back to the list
    del dependencies[:]
    dependencies.extend(libs)
    dependencies.extend(objfiles)
    dependencies.extend(additional)
    #Turn list into string again
    tempstr = ';'.join(dependencies)
    return (tempstr != olddeps, tempstr)

###########################################
#
# Script entry point
#
###########################################
if (__name__ == '__main__'):
    import sys
    main(sys.argv)
