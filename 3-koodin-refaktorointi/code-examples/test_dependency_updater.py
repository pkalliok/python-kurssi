
import shutil
from os import getcwd, chdir
from os.path import join, exists, abspath
from contextlib import contextmanager
import dependency_updater

def destroy_testdata(target_path):
    if exists(target_path): shutil.rmtree(target_path)

def create_testdata(target_path):
    destroy_testdata(target_path)
    shutil.copytree('dependency_updater_test_data', target_path)

@contextmanager
def data_fixture(target_path):
    save_cwd = getcwd()
    test_dir = abspath(target_path)
    create_testdata(test_dir)
    yield test_dir
    destroy_testdata(test_dir)
    chdir(save_cwd)

def get_dep_lines(target_path):
    return (line for line in open(join(target_path, "nonpnpapp.vcxproj"))
            if '<AdditionalDependencies>' in line)

def test_testdata():
    with data_fixture('test1') as d:
        dep_lines = list(get_dep_lines('test1'))
        assert len(dep_lines) == 4
        for line in dep_lines: assert 'foo.obj' in line

def test_changed_obj_update():
    with data_fixture('test2') as d:
        dependency_updater.updateProjectFile('nonpnpapp',
                abspath(d), abspath(join(d,'objfiles')), 'Debug')
        dep_lines = list(get_dep_lines(d))
        assert len(dep_lines) == 4
        assert 'quux.obj' in dep_lines[1]
        assert 'foo.obj' not in dep_lines[1]

