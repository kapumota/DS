"""
Pruebas de contrato: validación mínima de esquema JSON para módulos locales.
"""
import json
import pytest
from jsonschema import validate
from pruebas_contrato.main import NetworkFactoryLocal
from pruebas_contrato.network import ServerFactoryLocal

SCHEMA = {
    "type": "object",
    "properties": {
        "resources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["type", "name"]
            }
        }
    },
    "required": ["resources"]
}
@ pytest.mark.parametrize("cls,args", [
    (NetworkFactoryLocal, {"name":"testnet","ip_range":"10.0.0.0/24"}),
    (ServerFactoryLocal, {"name":"web01","network_cidr":"10.0.0.0/24"})
])
def test_contract_schema(cls, args, tmp_path):
    inst = cls(**args)
    data = inst.build()
    validate(instance=data, schema=SCHEMA)

@ pytest.mark.parametrize("cls,args,expected", [
    (NetworkFactoryLocal, {"name":"testnet","ip_range":"192.168.1.0/28"}, "local_network"),
    (ServerFactoryLocal, {"name":"app01","network_cidr":"192.168.1.0/28"}, "local_server")
])
def test_type_field(cls, args, expected):
    data = cls(**args).build()
    assert data['resources'][0]['type'] == expected

@ pytest.mark.parametrize("cls,args,field", [
    (NetworkFactoryLocal, {"name":"testnet","ip_range":"10.0.0.0/24"}, "cidr"),
    (ServerFactoryLocal, {"name":"svc","network_cidr":"10.1.0.0/24"}, "network_ip")
])
def test_required_fields(cls, args, field):
    data = cls(**args).build()
    assert field in data['resources'][0]
