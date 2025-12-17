from typing import List, Dict

# BOM templates for different wood assemblies
# Quantities are numeric and include a unit price in USD.

def default_wood_table_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Item No": 1, "Part Name": "Table Top Panel", "Quantity": 1, "Unit Price": 85.00, "Material": "Solid wood (oak/pine), ~1200x700x25mm"},
        {"Item No": 2, "Part Name": "Table Leg", "Quantity": 4, "Unit Price": 12.50, "Material": "Solid wood, ~70x70x730mm"},
        {"Item No": 3, "Part Name": "Apron/Rail", "Quantity": 4, "Unit Price": 9.75, "Material": "Solid wood, ~1000x90x20mm"},
        {"Item No": 4, "Part Name": "Corner Bracket", "Quantity": 4, "Unit Price": 2.80, "Material": "Steel L-bracket"},
        {"Item No": 5, "Part Name": "Wood Screws", "Quantity": 40, "Unit Price": 0.08, "Material": "#8 x 1-1/2\" wood screws"},
        {"Item No": 6, "Part Name": "Bolts + Nuts", "Quantity": 8, "Unit Price": 0.60, "Material": "M8 x 60mm bolts with nuts & washers"},
        {"Item No": 7, "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.50, "Material": "PVA wood glue (bottle)"},
        {"Item No": 8, "Part Name": "Finish", "Quantity": 1, "Unit Price": 14.00, "Material": "Stain/varnish/oil (can)"},
        {"Item No": 9, "Part Name": "Cross Support", "Quantity": 2, "Unit Price": 8.50, "Material": "Solid wood, ~900x70x20mm"},
        {"Item No": 10, "Part Name": "Felt Pads", "Quantity": 4, "Unit Price": 0.50, "Material": "Self-adhesive floor protectors"},
    ]
    return items


def default_wood_chair_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Item No": 1, "Part Name": "Seat Panel", "Quantity": 1, "Unit Price": 25.00, "Material": "Solid wood, ~450x450x20mm"},
        {"Item No": 2, "Part Name": "Chair Leg", "Quantity": 4, "Unit Price": 8.50, "Material": "Solid wood, ~40x40x450mm"},
        {"Item No": 3, "Part Name": "Backrest Panel", "Quantity": 1, "Unit Price": 18.00, "Material": "Solid wood, ~450x300x20mm"},
        {"Item No": 4, "Part Name": "Backrest Slat", "Quantity": 5, "Unit Price": 2.20, "Material": "Solid wood slats"},
        {"Item No": 5, "Part Name": "Side Rail", "Quantity": 2, "Unit Price": 6.75, "Material": "Solid wood, ~400x60x20mm"},
        {"Item No": 6, "Part Name": "Front/Rear Rail", "Quantity": 2, "Unit Price": 7.10, "Material": "Solid wood, ~400x70x20mm"},
        {"Item No": 7, "Part Name": "Wood Screws", "Quantity": 30, "Unit Price": 0.07, "Material": "#8 x 1-1/4\" wood screws"},
        {"Item No": 8, "Part Name": "Dowels", "Quantity": 20, "Unit Price": 0.05, "Material": "8mm beech dowels"},
        {"Item No": 9, "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.00, "Material": "PVA wood glue"},
        {"Item No": 10, "Part Name": "Finish", "Quantity": 1, "Unit Price": 12.00, "Material": "Varnish/oil"},
    ]
    return items


def default_wood_shelf_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Item No": 1, "Part Name": "Side Panel", "Quantity": 2, "Unit Price": 22.00, "Material": "Solid wood, ~1800x300x18mm"},
        {"Item No": 2, "Part Name": "Shelf Board", "Quantity": 3, "Unit Price": 18.00, "Material": "Solid wood, ~800x300x18mm"},
        {"Item No": 3, "Part Name": "Top/Bottom Panel", "Quantity": 2, "Unit Price": 20.00, "Material": "Solid wood, ~800x300x18mm"},
        {"Item No": 4, "Part Name": "Back Panel", "Quantity": 1, "Unit Price": 15.00, "Material": "Plywood, ~800x1800x6mm"},
        {"Item No": 5, "Part Name": "Shelf Pins", "Quantity": 16, "Unit Price": 0.12, "Material": "Metal pins"},
        {"Item No": 6, "Part Name": "Support Brackets", "Quantity": 6, "Unit Price": 2.50, "Material": "Steel angle"},
        {"Item No": 7, "Part Name": "Wood Screws", "Quantity": 40, "Unit Price": 0.08, "Material": "#8 x 1-1/2\" wood screws"},
        {"Item No": 8, "Part Name": "Bolts + Nuts", "Quantity": 10, "Unit Price": 0.60, "Material": "M6 bolts with nuts & washers"},
        {"Item No": 9, "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.50, "Material": "PVA wood glue"},
        {"Item No": 10, "Part Name": "Finish", "Quantity": 1, "Unit Price": 16.00, "Material": "Stain/varnish"},
    ]
    return items


def choose_bom_from_filename(name: str) -> List[Dict[str, object]]:
    lower = name.lower()
    if "chair" in lower:
        return default_wood_chair_bom()
    if "shelf" in lower:
        return default_wood_shelf_bom()
    # default to table
    return default_wood_table_bom()
