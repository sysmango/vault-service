import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_vault_exe_exists(host):
    vault_exe = host.files('/usr/local/bin/vault')
    assert vault_exe.exists

def test_vault_service_exists(host):
    vault_service = host.service('vault')
    assert vault_service.exists

def test_vault_service_running(host):
    vault_service = host.service('vault')
    assert vault_service.is_running
    assert vault_service.is_enabled
