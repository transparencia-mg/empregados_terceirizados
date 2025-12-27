#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re

def normalizar(col):
    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col)
    return col.strip("_")

def gerar_schema(csv_path):
    try:
        df = pd.read_csv(
            csv_path,
            sep=";",
            dtype=str,
            encoding="utf-8",
            low_memory=False
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            csv_path,
            sep=";",
            dtype=str,
            encoding="latin1",
            low_memory=False
        )

    fields = [
        {"name": "_id", "type": "string"}
    ]

    for col in df.columns:
        fields.append({
            "name": normalizar(col),
            "type": "string"
        })

    return {
        "fields": fields,
        "primaryKey": "_id",
        "missingValues": ["", "NA", "N/A", "null"]
    }
