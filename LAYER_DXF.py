# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 10:08:52 2026

@author: lauri.leppala
"""
#Creates layers of .dxf drawing by colors and lineweights and then creates new "TEST_BY_COLOR_LINEWEIGHT.dxf"
#drawing which has all layers by color and lineweights.

import ezdxf
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

# ---------------- PATHS ----------------
DXF_PATH = r"C:\" #path to your .DXF drawing
OUTPUT_DXF = r"C:\TEST_BY_COLOR_LINEWEIGHT.dxf" #new dxf drawing that is created
OUTPUT_XLSX = r"C:\lineweight_layers.xlsx" #excel list which shows all layers that are created

# ---------------- LOAD DXF ----------------
doc = ezdxf.readfile(DXF_PATH)
msp = doc.modelspace()

# ---------------- LAYER LOOKUPS ----------------
layer_lineweights = {
    layer.dxf.name: layer.dxf.lineweight
    for layer in doc.layers
}

layer_colors = {
    layer.dxf.name: layer.dxf.color
    for layer in doc.layers
}

# ---------------- COLLECT ENTITIES BY COLOR + LINEWEIGHT ----------------
groups = defaultdict(list)

print("Processing entities...")
for entity in tqdm(msp, desc="Scanning entities"):
    # -------- LINEWEIGHT --------
    lw = entity.dxf.lineweight
    if lw == -1:  # BYLAYER
        lw = layer_lineweights.get(entity.dxf.layer, -1)
    if lw < 0:
        continue

    lw_mm = lw / 100.0

    # -------- COLOR --------
    color = entity.dxf.color
    if color == 256:  # BYLAYER
        color = layer_colors.get(entity.dxf.layer, 256)
    if color < 0:
        continue

    key = (color, lw_mm)
    groups[key].append(entity)

# ---------------- CREATE LAYERS ----------------
summary_rows = []

print("Creating layers and moving entities...")
for idx, ((color, lw_mm), entities) in enumerate(
        tqdm(sorted(groups.items()), desc="Creating layers")):

    lw_raw = int(lw_mm * 100)
    layer_name = f"LW_{lw_raw:03d}_COL_{color}"

    if not doc.layers.has_entry(layer_name):
        doc.layers.new(
            name=layer_name,
            dxfattribs={
                "lineweight": lw_raw,
                "color": color
            }
        )

    for ent in entities:
        ent.dxf.layer = layer_name

    summary_rows.append({
        "Layer Name": layer_name,
        "Color Index": color,
        "Lineweight (mm)": lw_mm,
        "Entity Count": len(entities)
    })

# ---------------- SAVE DXF ----------------
print("Saving DXF...")
doc.saveas(OUTPUT_DXF)

# ---------------- WRITE EXCEL ----------------
print("Writing Excel summary...")
df_summary = pd.DataFrame(summary_rows)

with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
    for _ in tqdm([1], desc="Writing Excel"):
        df_summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

# ---------------- DONE ----------------
print("\n✔ DXF updated with color + lineweight based layers")
print(f"✔ Saved DXF: {OUTPUT_DXF}")
print(f"✔ Saved Excel: {OUTPUT_XLSX}")
