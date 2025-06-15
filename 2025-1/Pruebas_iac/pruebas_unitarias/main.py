#!/usr/bin/env python3
"""
Simula la definición de una red local y sus subredes en JSON.
Genera dos archivos:
 - network_config.json: definición de recursos a crear
 - network_state.json: estado planificado (simulado)
Además soporta:
 - Validación de rango CIDR
 - Actualización de parámetros de red
 - Limpieza de archivos previos
"""
import argparse
import json
import netaddr
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class NetworkFactoryLocal:
    """
    Genera JSON de configuración y estado de una red con subredes.
    """
    def __init__(self, name: str, ip_range: str, num_subnets: int):
        self.name = name
        self.network_name = f"{name}-network"
        self.subnet_prefix = f"{name}-subnet"
        self.ip_range = ip_range
        self.num_subnets = num_subnets
        self.region = "local-region"
        self._validate_inputs()

    def _validate_inputs(self):
        try:
            netaddr.IPNetwork(self.ip_range)
        except Exception as e:
            logging.error(f"CIDR inválido '{self.ip_range}': {e}")
            sys.exit(1)
        if self.num_subnets < 1:
            logging.error("num_subnets debe ser al menos 1")
            sys.exit(1)

    def build_config(self) -> dict:
        """Construye la sección `resources` equivalente a Terraform."""
        logging.info("Construyendo configuración de red")
        network = {
            "type": "local_network",
            "name": self.network_name,
            "auto_create_subnets": False,
            "region": self.region
        }
        net = netaddr.IPNetwork(self.ip_range)
        # calcula subredes iguales
        try:
            subs = list(net.subnet(net.prefixlen + (32 - net.prefixlen).bit_length(), count=self.num_subnets))
        except Exception:
            subs = net.subnet(24, count=self.num_subnets)
        subnet_list = []
        for i, subnet in enumerate(subs):
            subnet_list.append({
                "type": "local_subnet",
                "name": f"{self.subnet_prefix}-{i}",
                "network": self.network_name,
                "cidr": str(subnet)
            })
        return {"resources": [network] + subnet_list}

    def build_state(self, config: dict) -> dict:
        """Simula el estado planificado leyendo la configuración."""
        logging.info("Generando estado planificado")
        return {"planned_values": config}

    def clean_previous(self, out_dir: str):
        for fname in ['network_config.json', 'network_state.json']:
            path = os.path.join(out_dir, fname)
            if os.path.exists(path):
                os.remove(path)
                logging.debug(f"Eliminado archivo previo {path}")

    def write_files(self, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        self.clean_previous(out_dir)
        config = self.build_config()
        cfg_path = os.path.join(out_dir, 'network_config.json')
        with open(cfg_path, 'w') as f:
            json.dump(config, f, indent=4)
        state = self.build_state(config)
        st_path = os.path.join(out_dir, 'network_state.json')
        with open(st_path, 'w') as f:
            json.dump(state, f, indent=4)
        logging.info(f"Archivos escritos en {out_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generar configuración local de red.")
    parser.add_argument('--name', default='hello-world', help='Nombre base de la red')
    parser.add_argument('--cidr', default='10.0.0.0/16', help='Rango CIDR de la red')
    parser.add_argument('--subnets', type=int, default=3, help='Número de subredes')
    parser.add_argument('--out', default='.', help='Directorio de salida')
    args = parser.parse_args()

    factory = NetworkFactoryLocal(
        name=args.name,
        ip_range=args.cidr,
        num_subnets=args.subnets
    )
    factory.write_files(args.out)
    print(f"Archivos generados en {args.out}: network_config.json y network_state.json")
