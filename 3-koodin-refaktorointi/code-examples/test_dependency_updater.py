
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
    dependency_updater.logging = False
    create_testdata(test_dir)
    yield test_dir
    destroy_testdata(test_dir)
    chdir(save_cwd)
    dependency_updater.logging = True

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
                d, join(d,'objfiles'), 'Debug')
        dep_lines = list(get_dep_lines(d))
        assert len(dep_lines) == 4
        assert 'quux.obj' in dep_lines[1]
        assert 'foo.obj' not in dep_lines[1]

def test_empty_obj_update():
    with data_fixture('test3') as d:
        dependency_updater.updateProjectFile('nonpnpapp',
                d, join(d,'no_objfiles'), 'Debug')
        has_lines = False
        for num, line in enumerate(get_dep_lines(d)):
            if not num%2: continue
            assert 'foo.obj' not in line
            assert 'bar.obj' not in line
            assert 'quux.obj' not in line
            has_lines = True
        assert has_lines

def test_update_with_main():
    with data_fixture('test4') as d:
        dependency_updater.main(['me', 'nonpnpapp',
                d, join(d, 'objfiles'), join(d, 'objfiles')])
        has_lines = False
        for num, line in enumerate(get_dep_lines(d)):
            assert 'foo.obj' not in line
            assert 'baz.obj' in line
            has_lines = True
        assert has_lines

