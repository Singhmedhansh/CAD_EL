import argparse
import os
from tabulate import tabulate
from typing import List, Dict, Optional
from PIL import Image, ImageDraw

from src.bom_templates import default_wood_table_bom, choose_bom_from_filename
from src.image_analyzer import load_image, looks_wood_like
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
    headers = ["Item No", "Part Name", "Quantity", "Unit Price", "Subtotal", "Material"]
    table = []
    for row in items:
        table.append([
            row["Item No"],
            row["Part Name"],
            row["Quantity"],
            format_currency(float(row.get("Unit Price", 0.0))),
            format_currency(float(row.get("Subtotal", 0.0))),
            row["Material"],
        ])
    print(tabulate(table, headers=headers, tablefmt="grid"))



def generate_demo_image(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
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
    wood_like = looks_wood_like(img)
    bom = choose_bom_from_filename(os.path.basename(image_path))
    if not wood_like:
        print("[WARN] Image does not appear wood-like; using chosen wood BOM anyway.")
    return bom



def main():
    parser = argparse.ArgumentParser(description="Wood Table BOM Generator")
    parser.add_argument("--image", type=str, help="Path to PNG/JPG image of a wood table")
    parser.add_argument("--images", nargs="+", help="Paths to multiple PNG/JPG images for batch processing")
    parser.add_argument("--dir", type=str, help="Directory containing images to process")
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
        generate_demo_image(image_path)
        print(f"[INFO] Generated demo image at: {image_path}")

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

    # Validation: at least 3 assemblies and min 10 parts each
    if len(results) < 3 or any(len(r["items"]) < 10 for r in results):
        print("\n[ERROR] Validation failed: need at least 3 assemblies and at least 10 parts in each.")
        print("[HINT] Provide 3+ images named with keywords like 'table', 'chair', 'shelf' to select templates.")
        return

    overall = sum(r["total"] for r in results)
    print(f"\n=== Summary ===")
    for r in results:
        print(f" - {r['assembly']}: {format_currency(r['total'])} ({len(r['items'])} parts)")
    print(f"Overall Total: {format_currency(overall)}")


if __name__ == "__main__":
    main()
