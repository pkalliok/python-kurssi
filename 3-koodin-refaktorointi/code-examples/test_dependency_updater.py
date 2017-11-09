
import shutil
import dependency_updater

def destroy_testdata(target_path): shutil.rmtree(target_path)

def create_testdata(target_path):
    destroy_testdata(target_path)
    shutil.copytree('dependency_updater_test_data', target_path)

def get_dep_lines(target_path):
    return (line for line in open(target_path + "/nonpnpapp.vcxproj")
            if '<AdditionalDependencies>' in line)

def test_testdata():
    create_testdata('/tmp/test1')
    dep_lines = list(get_dep_lines('/tmp/test1'))
    assert len(dep_lines) == 4
    for line in dep_lines: assert 'foo.obj' in line
    destroy_testdata('/tmp/test1')

