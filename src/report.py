import os
import csv
from datetime import datetime
from typing import List, Dict
from openpyxl import Workbook
from config import OUTPUT_DIR, REPORT_BASE_NAME


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def timestamp_name() -> str:
    return f"{REPORT_BASE_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def write_csv(items: List[Dict[str, str]], base_name: str) -> str:
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, f"{base_name}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Item No", "Part Name", "Quantity", "Material"])
        writer.writeheader()
        for row in items:
            writer.writerow(row)
    return path


def write_xlsx(items: List[Dict[str, str]], base_name: str) -> str:
    ensure_output_dir()
    wb = Workbook()
    ws = wb.active
    ws.title = "BOM"
    ws.append(["Item No", "Part Name", "Quantity", "Material"])
    for row in items:
        ws.append([row["Item No"], row["Part Name"], row["Quantity"], row["Material"]])
    path = os.path.join(OUTPUT_DIR, f"{base_name}.xlsx")
    wb.save(path)
    return path
