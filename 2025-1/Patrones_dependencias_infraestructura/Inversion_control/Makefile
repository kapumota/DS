TF_ENV := \
  TF_DATA_DIR=$(CURDIR)/.terraform \
  TF_PLUGIN_CACHE_DIR=$(CURDIR)/.terraform/plugin-cache \
  TMP=$(CURDIR)/.terraform/tmp \
  TEMP=$(CURDIR)/.terraform/tmp

.PHONY: all prepare network server clean destroy

all: prepare network server          ## Flujo completo

prepare:
	@mkdir -p .terraform/plugin-cache .terraform/tmp

network: prepare
	cd network && $(TF_ENV) terraform init -upgrade -no-color && \
	$(TF_ENV) terraform apply -auto-approve -no-color

server: network
	python main.py
	$(TF_ENV) terraform init -upgrade -no-color && \
	$(TF_ENV) terraform apply -auto-approve -no-color

clean:                               ## Borra artefactos locales
	rm -rf .terraform .terraform.lock.hcl main.tf.json \
	       network/network_outputs.json network/.terraform network/.terraform.lock.hcl

destroy:                             ## Destruye ambos módulos
	-$(TF_ENV) terraform destroy -auto-approve -no-color || true
	-cd network && $(TF_ENV) terraform destroy -auto-approve -no-color || true
