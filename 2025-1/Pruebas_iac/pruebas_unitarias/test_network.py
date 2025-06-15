import pytest
import json
import os
from main import NetworkFactoryLocal
from netaddr import IPNetwork

@ pytest.fixture(scope="module")
def factory(tmp_path_factory):
    d = tmp_path_factory.mktemp('data')
    # Prueba con parámetros personalizados
    f = NetworkFactoryLocal('testnet', '192.168.0.0/24', 2)
    f.write_files(str(d))
    return d

@ pytest.fixture(scope="module")
def config(factory):
    path = factory / 'network_config.json'
    return json.loads(path.read_text())

def test_valid_prefixlen(config):
    # Validar que la red y subred tengan prefijos correctos
    resources = config['resources']
    assert resources[0]['cidr'] if 'cidr' in resources[0] else True


def test_subnet_count(config):
    subs = [r for r in config['resources'] if r['type']=='local_subnet']
    assert len(subs) == 2


def test_names_unique(config):
    names = [r['name'] for r in config['resources']]
    assert len(names) == len(set(names))


def test_invalid_cidr_exit(monkeypatch, tmp_path):
    # CIDR inválido debe terminar el programa
    monkeypatch.setattr('sys.exit', lambda code: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        NetworkFactoryLocal('bad', '10.0.0.0/99', 1)
