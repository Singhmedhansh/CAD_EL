from typing import List, Dict

# BOM templates for different assemblies
# Hierarchical structure: Level 0 = Main Assembly, Level 1 = Sub-assembly, Level 2 = Part
# Quantities are numeric and include a unit price in USD.

def engine_assembly_bom() -> List[Dict[str, object]]:
    """Engine assembly - standalone with 10 major parts."""
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Cylinder Block", "Quantity": 1, "Unit Price": 850.00, "Material": "Cast iron, 6-cylinder V-configuration"},
        {"Level": 0, "Item No": "2", "Part Name": "Piston Assembly", "Quantity": 6, "Unit Price": 65.00, "Material": "Forged aluminum with rings, 86mm bore"},
        {"Level": 0, "Item No": "3", "Part Name": "Connecting Rod", "Quantity": 6, "Unit Price": 85.00, "Material": "Forged steel, I-beam design"},
        {"Level": 0, "Item No": "4", "Part Name": "Crankshaft", "Quantity": 1, "Unit Price": 525.00, "Material": "Forged steel, fully balanced, hardened journals"},
        {"Level": 0, "Item No": "5", "Part Name": "Camshaft", "Quantity": 2, "Unit Price": 210.00, "Material": "Steel, DOHC configuration, variable valve timing"},
        {"Level": 0, "Item No": "6", "Part Name": "Cylinder Head", "Quantity": 2, "Unit Price": 425.00, "Material": "Aluminum alloy, 3-valve per cylinder"},
        {"Level": 0, "Item No": "7", "Part Name": "Timing Chain Kit", "Quantity": 1, "Unit Price": 185.00, "Material": "Roller chain with tensioner, guides & sprockets"},
        {"Level": 0, "Item No": "8", "Part Name": "Oil Pump", "Quantity": 1, "Unit Price": 145.00, "Material": "Gear-type, high-pressure"},
        {"Level": 0, "Item No": "9", "Part Name": "Water Pump", "Quantity": 1, "Unit Price": 95.00, "Material": "Centrifugal, cast aluminum housing"},
        {"Level": 0, "Item No": "10", "Part Name": "Engine Gasket Set", "Quantity": 1, "Unit Price": 125.00, "Material": "Complete MLS head, pan, valve cover gaskets"},
    ]
    return items


def transmission_assembly_bom() -> List[Dict[str, object]]:
    """Transmission assembly - standalone with 10 major parts."""
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Transmission Case", "Quantity": 1, "Unit Price": 650.00, "Material": "Cast aluminum, 6-speed automatic housing"},
        {"Level": 0, "Item No": "2", "Part Name": "Torque Converter", "Quantity": 1, "Unit Price": 425.00, "Material": "3-element fluid coupling with lock-up clutch"},
        {"Level": 0, "Item No": "3", "Part Name": "Planetary Gear Set", "Quantity": 3, "Unit Price": 285.00, "Material": "Hardened steel gears, sun/planet/ring configuration"},
        {"Level": 0, "Item No": "4", "Part Name": "Clutch Pack", "Quantity": 6, "Unit Price": 75.00, "Material": "Friction and steel plates, multi-disc"},
        {"Level": 0, "Item No": "5", "Part Name": "Valve Body", "Quantity": 1, "Unit Price": 385.00, "Material": "Aluminum casting with hydraulic control passages"},
        {"Level": 0, "Item No": "6", "Part Name": "Transmission Control Module (TCM)", "Quantity": 1, "Unit Price": 425.00, "Material": "Electronic control unit, adaptive shift logic"},
        {"Level": 0, "Item No": "7", "Part Name": "Oil Pump", "Quantity": 1, "Unit Price": 165.00, "Material": "Gerotor type, driven by input shaft"},
        {"Level": 0, "Item No": "8", "Part Name": "Output Shaft", "Quantity": 1, "Unit Price": 195.00, "Material": "Forged steel, splined for driveshaft connection"},
        {"Level": 0, "Item No": "9", "Part Name": "Transmission Cooler", "Quantity": 1, "Unit Price": 135.00, "Material": "Aluminum tube-and-fin heat exchanger"},
        {"Level": 0, "Item No": "10", "Part Name": "Shift Solenoid Pack", "Quantity": 1, "Unit Price": 245.00, "Material": "8 electronic solenoids for gear selection"},
    ]
    return items


def suspension_assembly_bom() -> List[Dict[str, object]]:
    """Front suspension assembly - standalone with 10 major parts."""
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Strut Assembly", "Quantity": 2, "Unit Price": 285.00, "Material": "MacPherson strut, gas-charged monotube damper"},
        {"Level": 0, "Item No": "2", "Part Name": "Coil Spring", "Quantity": 2, "Unit Price": 85.00, "Material": "High-tensile steel, progressive rate"},
        {"Level": 0, "Item No": "3", "Part Name": "Control Arm", "Quantity": 2, "Unit Price": 165.00, "Material": "Stamped steel, lower A-arm with bushings"},
        {"Level": 0, "Item No": "4", "Part Name": "Ball Joint", "Quantity": 2, "Unit Price": 55.00, "Material": "Forged steel housing with grease fitting"},
        {"Level": 0, "Item No": "5", "Part Name": "Sway Bar", "Quantity": 1, "Unit Price": 125.00, "Material": "Solid steel torsion bar, 28mm diameter"},
        {"Level": 0, "Item No": "6", "Part Name": "Sway Bar Link", "Quantity": 2, "Unit Price": 35.00, "Material": "Steel rod with ball joints, adjustable"},
        {"Level": 0, "Item No": "7", "Part Name": "Steering Knuckle", "Quantity": 2, "Unit Price": 145.00, "Material": "Cast aluminum, wheel hub mounting"},
        {"Level": 0, "Item No": "8", "Part Name": "Wheel Bearing Hub", "Quantity": 2, "Unit Price": 95.00, "Material": "Sealed double-row ball bearing assembly"},
        {"Level": 0, "Item No": "9", "Part Name": "Strut Mount", "Quantity": 2, "Unit Price": 45.00, "Material": "Rubber-isolated bearing with upper spring seat"},
        {"Level": 0, "Item No": "10", "Part Name": "Bushing Kit", "Quantity": 1, "Unit Price": 65.00, "Material": "Polyurethane control arm & sway bar bushings"},
    ]
    return items

def default_wood_table_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Table Top Panel", "Quantity": 1, "Unit Price": 85.00, "Material": "Solid wood (oak/pine), ~1200x700x25mm"},
        {"Level": 0, "Item No": "2", "Part Name": "Table Leg", "Quantity": 4, "Unit Price": 12.50, "Material": "Solid wood, ~70x70x730mm"},
        {"Level": 0, "Item No": "3", "Part Name": "Apron/Rail", "Quantity": 4, "Unit Price": 9.75, "Material": "Solid wood, ~1000x90x20mm"},
        {"Level": 0, "Item No": "4", "Part Name": "Corner Bracket", "Quantity": 4, "Unit Price": 2.80, "Material": "Steel L-bracket"},
        {"Level": 0, "Item No": "5", "Part Name": "Wood Screws", "Quantity": 40, "Unit Price": 0.08, "Material": "#8 x 1-1/2\" wood screws"},
        {"Level": 0, "Item No": "6", "Part Name": "Bolts + Nuts", "Quantity": 8, "Unit Price": 0.60, "Material": "M8 x 60mm bolts with nuts & washers"},
        {"Level": 0, "Item No": "7", "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.50, "Material": "PVA wood glue (bottle)"},
        {"Level": 0, "Item No": "8", "Part Name": "Finish", "Quantity": 1, "Unit Price": 14.00, "Material": "Stain/varnish/oil (can)"},
        {"Level": 0, "Item No": "9", "Part Name": "Cross Support", "Quantity": 2, "Unit Price": 8.50, "Material": "Solid wood, ~900x70x20mm"},
        {"Level": 0, "Item No": "10", "Part Name": "Felt Pads", "Quantity": 4, "Unit Price": 0.50, "Material": "Self-adhesive floor protectors"},
    ]
    return items


def default_wood_chair_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Seat Panel", "Quantity": 1, "Unit Price": 25.00, "Material": "Solid wood, ~450x450x20mm"},
        {"Level": 0, "Item No": "2", "Part Name": "Chair Leg", "Quantity": 4, "Unit Price": 8.50, "Material": "Solid wood, ~40x40x450mm"},
        {"Level": 0, "Item No": "3", "Part Name": "Backrest Panel", "Quantity": 1, "Unit Price": 18.00, "Material": "Solid wood, ~450x300x20mm"},
        {"Level": 0, "Item No": "4", "Part Name": "Backrest Slat", "Quantity": 5, "Unit Price": 2.20, "Material": "Solid wood slats"},
        {"Level": 0, "Item No": "5", "Part Name": "Side Rail", "Quantity": 2, "Unit Price": 6.75, "Material": "Solid wood, ~400x60x20mm"},
        {"Level": 0, "Item No": "6", "Part Name": "Front/Rear Rail", "Quantity": 2, "Unit Price": 7.10, "Material": "Solid wood, ~400x70x20mm"},
        {"Level": 0, "Item No": "7", "Part Name": "Wood Screws", "Quantity": 30, "Unit Price": 0.07, "Material": "#8 x 1-1/4\" wood screws"},
        {"Level": 0, "Item No": "8", "Part Name": "Dowels", "Quantity": 20, "Unit Price": 0.05, "Material": "8mm beech dowels"},
        {"Level": 0, "Item No": "9", "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.00, "Material": "PVA wood glue"},
        {"Level": 0, "Item No": "10", "Part Name": "Finish", "Quantity": 1, "Unit Price": 12.00, "Material": "Varnish/oil"},
    ]
    return items


def default_wood_shelf_bom() -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = [
        {"Level": 0, "Item No": "1", "Part Name": "Side Panel", "Quantity": 2, "Unit Price": 22.00, "Material": "Solid wood, ~1800x300x18mm"},
        {"Level": 0, "Item No": "2", "Part Name": "Shelf Board", "Quantity": 3, "Unit Price": 18.00, "Material": "Solid wood, ~800x300x18mm"},
        {"Level": 0, "Item No": "3", "Part Name": "Top/Bottom Panel", "Quantity": 2, "Unit Price": 20.00, "Material": "Solid wood, ~800x300x18mm"},
        {"Level": 0, "Item No": "4", "Part Name": "Back Panel", "Quantity": 1, "Unit Price": 15.00, "Material": "Plywood, ~800x1800x6mm"},
        {"Level": 0, "Item No": "5", "Part Name": "Shelf Pins", "Quantity": 16, "Unit Price": 0.12, "Material": "Metal pins"},
        {"Level": 0, "Item No": "6", "Part Name": "Support Brackets", "Quantity": 6, "Unit Price": 2.50, "Material": "Steel angle"},
        {"Level": 0, "Item No": "7", "Part Name": "Wood Screws", "Quantity": 40, "Unit Price": 0.08, "Material": "#8 x 1-1/2\" wood screws"},
        {"Level": 0, "Item No": "8", "Part Name": "Bolts + Nuts", "Quantity": 10, "Unit Price": 0.60, "Material": "M6 bolts with nuts & washers"},
        {"Level": 0, "Item No": "9", "Part Name": "Wood Glue", "Quantity": 1, "Unit Price": 6.50, "Material": "PVA wood glue"},
        {"Level": 0, "Item No": "10", "Part Name": "Finish", "Quantity": 1, "Unit Price": 16.00, "Material": "Stain/varnish"},
    ]
    return items


def choose_bom_from_filename(name: str) -> List[Dict[str, object]]:
    lower = name.lower()
    if "engine" in lower or "motor" in lower:
        return engine_assembly_bom()
    if "transmission" in lower or "gearbox" in lower:
        return transmission_assembly_bom()
    if "suspension" in lower or "strut" in lower:
        return suspension_assembly_bom()
    if "chair" in lower:
        return default_wood_chair_bom()
    if "shelf" in lower:
        return default_wood_shelf_bom()
    # default to table
    return default_wood_table_bom()
