
import shutil
from os import getcwd
from os.path import join, exists, abspath
import dependency_updater

def destroy_testdata(target_path):
    if exists(target_path): shutil.rmtree(target_path)

def create_testdata(target_path):
    destroy_testdata(target_path)
    shutil.copytree('dependency_updater_test_data', target_path)

def get_dep_lines(target_path):
    return (line for line in open(join(target_path, "nonpnpapp.vcxproj"))
            if '<AdditionalDependencies>' in line)

def test_testdata():
    create_testdata('test1')
    dep_lines = list(get_dep_lines('test1'))
    assert len(dep_lines) == 4
    for line in dep_lines: assert 'foo.obj' in line
    destroy_testdata('test1')

#def test_changed_obj_update():
    #create_testdata('test2')
    #dependency_updater.updateProjectFile('nonpnpapp',
        #abspath('test2'), abspath('test2/objfiles'), 'Debug')
    #dep_lines = list(get_dep_lines('test2'))
    #assert len(dep_lines) == 4
    #assert 'quux.obj' in dep_lines[1]
    #assert 'foo.obj' not in dep_lines[1]
    #destroy_testdata('test2')
