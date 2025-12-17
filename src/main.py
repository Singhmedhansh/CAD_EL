import argparse
import os
from tabulate import tabulate
from typing import List, Dict, Optional
from PIL import Image, ImageDraw

from src.bom_templates import default_wood_table_bom, choose_bom_from_filename
from src.image_analyzer import load_image, looks_wood_like, detect_component_type
from config import INPUT_IMAGES_DIR



def format_currency(value: float) -> str:
    return f"$ {value:,.2f}"


def compute_totals(items: List[Dict[str, object]]) -> Dict[str, float]:
    grand_total = 0.0
    for row in items:
        qty = int(row.get("Quantity", 0))
        unit = float(row.get("Unit Price", 0.0))
        subtotal = qty * unit
        row["Subtotal"] = subtotal
        grand_total += subtotal
    return {"grand_total": grand_total}


def print_bom(items: List[Dict[str, object]]):
    headers = ["Level", "Item No", "Part Name", "Quantity", "Unit Price", "Subtotal", "Material"]
    table = []
    for row in items:
        level = row.get("Level", 0)
        indent = "  " * level  # Indent based on level
        part_name = indent + row["Part Name"]
        table.append([
            level,
            row["Item No"],
            part_name,
            row["Quantity"],
            format_currency(float(row.get("Unit Price", 0.0))),
            format_currency(float(row.get("Subtotal", 0.0))),
            row["Material"],
        ])
    print(tabulate(table, headers=headers, tablefmt="grid"))



def generate_demo_image(path: str, image_type: str = "table"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if image_type == "engine":
        # Generate realistic engine image with better details
        img = Image.new("RGB", (800, 600), (45, 45, 50))  # dark background
        d = ImageDraw.Draw(img)
        
        # Main engine block (V-shape)
        block_color = (85, 85, 90)
        d.polygon([(250, 250), (400, 180), (550, 250), (550, 450), (400, 480), (250, 450)], fill=block_color)
        
        # Cylinder heads (left bank)
        head_color = (105, 105, 110)
        d.rectangle([(180, 220), (250, 400)], fill=head_color)
        d.rectangle([(175, 215), (255, 225)], fill=(75, 75, 80))  # top edge
        
        # Cylinder heads (right bank)
        d.rectangle([(550, 220), (620, 400)], fill=head_color)
        d.rectangle([(545, 215), (625, 225)], fill=(75, 75, 80))
        
        # Valve covers with bolts
        cover_color = (140, 30, 25)  # red/orange valve covers
        d.rectangle([(170, 230), (240, 390)], fill=cover_color)
        d.rectangle([(560, 230), (630, 390)], fill=cover_color)
        
        # Bolts on valve covers
        bolt_color = (180, 180, 185)
        for y in range(250, 380, 40):
            d.ellipse([(185, y), (195, y+10)], fill=bolt_color)
            d.ellipse([(575, y), (585, y+10)], fill=bolt_color)
        
        # Oil pan
        d.rectangle([(270, 450), (530, 500)], fill=(65, 65, 70))
        d.rectangle([(280, 490), (520, 495)], fill=(45, 45, 50))  # drain plug line
        
        # Intake manifold on top
        d.polygon([(320, 180), (400, 160), (480, 180), (460, 220), (340, 220)], fill=(95, 95, 100))
        
        # Alternator (circular)
        d.ellipse([(580, 340), (650, 410)], fill=(75, 75, 80))
        d.ellipse([(595, 355), (635, 395)], fill=(55, 55, 60))  # center
        
        # Starter motor
        d.ellipse([(150, 360), (200, 410)], fill=(70, 70, 75))
        d.rectangle([(125, 375), (150, 395)], fill=(80, 80, 85))  # mounting
        
        # Spark plug wires
        wire_color = (200, 50, 50)
        for i, x in enumerate([190, 210, 230, 570, 590, 610]):
            y_start = 240 + (i % 3) * 40
            d.line([(x, y_start), (x+10, y_start-30), (380+i*8, 190)], fill=wire_color, width=3)
        
        # Timing chain cover
        d.polygon([(360, 250), (440, 250), (430, 350), (370, 350)], fill=(95, 95, 100))
        
        # Coolant hoses
        hose_color = (40, 40, 45)
        d.ellipse([(420, 175), (460, 195)], fill=hose_color)
        d.ellipse([(340, 175), (380, 195)], fill=hose_color)
        
        # Belt pulleys
        d.ellipse([(590, 280), (630, 320)], fill=(90, 90, 95))
        d.ellipse([(600, 290), (620, 310)], fill=(70, 70, 75))
        
        # Oil filter (cylindrical)
        d.rectangle([(480, 420), (530, 480)], fill=(200, 160, 50))  # gold/yellow
        d.ellipse([(475, 415), (535, 425)], fill=(180, 140, 30))
        
        # Dipstick
        d.rectangle([(320, 300), (325, 380)], fill=(220, 180, 60))
        d.ellipse([(315, 295), (330, 305)], fill=(220, 180, 60))
        
        img.save(path, format="PNG")
    else:
        # Original wood table
        img = Image.new("RGB", (800, 600), (210, 180, 140))  # wood-like background
        d = ImageDraw.Draw(img)
        # Draw a simple table silhouette: top and four legs
        d.rectangle([(100, 150), (700, 250)], fill=(170, 130, 90))  # top
        leg_color = (120, 80, 50)
        d.rectangle([(140, 250), (170, 500)], fill=leg_color)
        d.rectangle([(630, 250), (660, 500)], fill=leg_color)
        d.rectangle([(330, 250), (360, 500)], fill=leg_color)
        d.rectangle([(440, 250), (470, 500)], fill=leg_color)
        img.save(path, format="PNG")



def build_bom_from_image(image_path: str) -> List[Dict[str, object]]:
    img = load_image(image_path)
    component_type = detect_component_type(img)
    bom = choose_bom_from_filename(os.path.basename(image_path))
    
    if component_type == "mechanical":
        print(f"[INFO] Detected mechanical/automotive component")
    elif component_type == "wood":
        print(f"[INFO] Detected wood-like component")
    else:
        print(f"[WARN] Component type uncertain; using BOM based on filename")
    
    return bom



def main():
    parser = argparse.ArgumentParser(description="CAD-EL BOM Generator - Wood and Automotive/Mechanical Assemblies")
    parser.add_argument("--image", type=str, help="Path to PNG/JPG image of assembly")
    parser.add_argument("--images", nargs="+", help="Paths to multiple PNG/JPG images for batch processing")
    parser.add_argument("--dir", type=str, help="Directory containing images to process")
    parser.add_argument("--demo-engine", action="store_true", help="Generate demo engine image and run BOM")
    parser.add_argument("--demo3", action="store_true", help="Generate 3 demo images (table/chair/shelf) and process")
    parser.add_argument("--demo", action="store_true", help="Generate a demo table PNG and run BOM")
    args = parser.parse_args()

    def resolve_image_path(arg_path: Optional[str]) -> Optional[str]:
        # If a path was provided and exists, use it
        if arg_path and os.path.exists(arg_path):
            return arg_path
        # If a filename only was provided, try common locations
        if arg_path and os.sep not in arg_path and "/" not in arg_path:
            candidate = os.path.join(INPUT_IMAGES_DIR, arg_path)
            if os.path.exists(candidate):
                return candidate
        # If no path provided, try common default filenames
        if not arg_path:
            defaults = [
                "download.png",
                "download.jpg",
                "download.jpeg",
                os.path.join(INPUT_IMAGES_DIR, "download.png"),
                os.path.join(INPUT_IMAGES_DIR, "download.jpg"),
                os.path.join(INPUT_IMAGES_DIR, "download.jpeg"),
            ]
            for c in defaults:
                if os.path.exists(c):
                    return c
        # As a last resort, search recursively for the filename
        if arg_path:
            name = os.path.basename(arg_path)
            for root, _dirs, files in os.walk("."):
                if name in files:
                    return os.path.join(root, name)
        return None

    image_path = args.image
    if args.demo:
        image_path = os.path.join(INPUT_IMAGES_DIR, "demo_table.png")
        generate_demo_image(image_path, "table")
        print(f"[INFO] Generated demo image at: {image_path}")

    if args.demo_engine:
        paths = []
        os.makedirs(INPUT_IMAGES_DIR, exist_ok=True)
        # Generate 3 car assembly images
        p_engine = os.path.join(INPUT_IMAGES_DIR, "demo_engine.png")
        generate_demo_image(p_engine, "engine")
        paths.append(p_engine)
        
        p_trans = os.path.join(INPUT_IMAGES_DIR, "demo_transmission.png")
        img = Image.new("RGB", (800, 600), (110, 110, 115))  # metallic gray
        img.save(p_trans, format="PNG")
        paths.append(p_trans)
        
        p_susp = os.path.join(INPUT_IMAGES_DIR, "demo_suspension.png")
        img = Image.new("RGB", (800, 600), (100, 100, 105))  # metallic gray
        img.save(p_susp, format="PNG")
        paths.append(p_susp)
        
        print("[INFO] Generated demo car assembly images:")
        for p in paths:
            print(f" - {p}")
        args.images = paths

    if args.demo3:
        paths = []
        os.makedirs(INPUT_IMAGES_DIR, exist_ok=True)
        # table
        p_table = os.path.join(INPUT_IMAGES_DIR, "demo_table.png")
        generate_demo_image(p_table)
        paths.append(p_table)
        # chair (different bg color)
        p_chair = os.path.join(INPUT_IMAGES_DIR, "demo_chair.jpg")
        img = Image.new("RGB", (800, 600), (200, 160, 120))
        img.save(p_chair, format="JPEG")
        paths.append(p_chair)
        # shelf (different bg color)
        p_shelf = os.path.join(INPUT_IMAGES_DIR, "demo_shelf.jpg")
        img = Image.new("RGB", (800, 600), (190, 150, 110))
        img.save(p_shelf, format="JPEG")
        paths.append(p_shelf)
        print("[INFO] Generated demo images:")
        for p in paths:
            print(f" - {p}")
        args.images = paths

    def resolve_many(paths: List[str]) -> List[str]:
        out = []
        for p in paths:
            r = resolve_image_path(p)
            if r:
                out.append(r)
            else:
                print(f"[WARN] Skipped missing image: {p}")
        return out

    if args.images:
        candidates = resolve_many(args.images)
    elif args.dir:
        exts = {".png", ".jpg", ".jpeg"}
        all_found = []
        for root, _d, files in os.walk(args.dir):
            for f in files:
                if os.path.splitext(f)[1].lower() in exts:
                    all_found.append(os.path.join(root, f))
        candidates = resolve_many(all_found)
    else:
        resolved = resolve_image_path(image_path)
        if not resolved:
            print("[ERROR] Image not found. Provide --image/--images or use --dir with images.")
            return
        candidates = [resolved]
        print(f"[INFO] Using image: {resolved}")

    results = []
    for p in candidates:
        try:
            items = build_bom_from_image(p)
        except Exception as e:
            print(f"[ERROR] Failed to analyze image '{p}': {e}")
            continue
        totals = compute_totals(items)
        asm_name = os.path.basename(p)
        print(f"\n=== Bill of Materials ({asm_name}) ===")
        print_bom(items)
        print(f"\nAssembly Total: {format_currency(totals['grand_total'])}")
        results.append({"assembly": asm_name, "items": items, "total": totals['grand_total']})

    # Summary
    if len(results) > 0:
        overall = sum(r["total"] for r in results)
        print(f"\n=== Summary ===")
        for r in results:
            print(f" - {r['assembly']}: {format_currency(r['total'])} ({len(r['items'])} items)")
        print(f"Overall Total: {format_currency(overall)}")
    else:
        print("\n[ERROR] No BOMs generated. Check input images.")


if __name__ == "__main__":
    main()
