#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

CKAN_API_KEY = os.getenv("CKAN_API_KEY")

if not CKAN_API_KEY:
    print("ERRO: variável de ambiente CKAN_API_KEY não definida")
    sys.exit(1)

cmd = [
    "dpckan", "publish",
    "datapackage/datapackage.json",
    "--ckan-host", "https://www.dados.mg.gov.br",
    "--api-key", CKAN_API_KEY,
    "--dataset-name", "empregados-terceirizados",
    "--organization", "controladoria-geral-do-estado-cge",
    "--force"
]

print("Executando:", " ".join(cmd[:-1] + ["***"]))

subprocess.run(cmd, check=True)
