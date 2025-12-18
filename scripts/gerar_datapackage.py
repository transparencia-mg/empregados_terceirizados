# scripts/gerar_datapackage.py
import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

resources = []

for csv in sorted(DATA_DIR.glob("terceirizados_*.csv")):
    ano = csv.stem.split("_")[-1]

    resources.append({
        "name": f"terceirizados-{ano}",
        "title": f"Empregados Terceirizados – {ano}",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "description": f"Dados de empregados terceirizados do ano de {ano}"
    })

datapackage = {
    "profile": "data-package",
    "name": "empregados-terceirizados",
    "title": "Empregados Terceirizados do Governo de Minas Gerais",
    "description": "Base anual de empregados terceirizados do Governo do Estado de Minas Gerais.",
    "owner_org": "controladoria-geral-do-estado-cge",
    "license": {
        "type": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/"
    },
    "resources": resources
}

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("datapackage.json gerado com sucesso.")

