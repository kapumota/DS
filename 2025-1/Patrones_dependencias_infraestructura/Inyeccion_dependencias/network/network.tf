terraform {
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
    local = { source = "hashicorp/local", version = "~> 2.1" }
  }
}

resource "null_resource" "network" {
  triggers = {
    name = "hello-local-network"
    cidr = "10.0.0.0/28"
  }
}

resource "local_file" "network_metadata" {
  content  = jsonencode({
    name = null_resource.network.triggers.name,
    cidr = null_resource.network.triggers.cidr
  })
  filename = "${path.module}/network_metadata.json"
}
