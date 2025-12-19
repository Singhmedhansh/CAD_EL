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
        # Generate 5 car assembly images
        p_engine = os.path.join(INPUT_IMAGES_DIR, "demo_engine.png")
        generate_demo_image(p_engine, "engine")
        paths.append(p_engine)
        
        p_trans = os.path.join(INPUT_IMAGES_DIR, "demo_transmission.png")
        # Generate detailed transmission image
        img = Image.new("RGB", (800, 600), (35, 35, 40))
        d = ImageDraw.Draw(img)
        # Main transmission case
        d.rectangle([(200, 200), (600, 500)], fill=(95, 95, 100))
        d.rectangle([(195, 195), (605, 205)], fill=(75, 75, 80))  # top edge
        # Bell housing (circular front)
        d.ellipse([(150, 280), (250, 420)], fill=(85, 85, 90))
        d.ellipse([(170, 300), (230, 400)], fill=(55, 55, 60))  # center hole
        # Torque converter
        d.ellipse([(100, 310), (180, 390)], fill=(110, 110, 115))
        # Cooling lines
        d.line([(300, 210), (300, 170), (450, 170), (450, 210)], fill=(40, 40, 45), width=8)
        d.line([(350, 210), (350, 150), (500, 150), (500, 210)], fill=(40, 40, 45), width=8)
        # Output shaft
        d.rectangle([(600, 330), (720, 370)], fill=(70, 70, 75))
        d.ellipse([(710, 320), (740, 380)], fill=(90, 90, 95))
        # Valve body area
        d.rectangle([(220, 480), (580, 520)], fill=(80, 80, 85))
        # Bolts around case
        bolt_color = (120, 120, 125)
        for x in range(220, 580, 60):
            d.ellipse([(x, 210), (x+10, 220)], fill=bolt_color)
            d.ellipse([(x, 490), (x+10, 500)], fill=bolt_color)
        for y in range(240, 480, 60):
            d.ellipse([(210, y), (220, y+10)], fill=bolt_color)
            d.ellipse([(590, y), (600, y+10)], fill=bolt_color)
        # Shift linkage
        d.line([(400, 200), (420, 140), (440, 140)], fill=(180, 180, 185), width=6)
        d.ellipse([(435, 135), (455, 155)], fill=(150, 150, 155))
        # Pan with drain plug
        d.rectangle([(240, 500), (560, 530)], fill=(65, 65, 70))
        d.ellipse([(395, 510), (405, 520)], fill=(180, 180, 185))
        # TCM module
        d.rectangle([(520, 250), (580, 320)], fill=(40, 40, 50))
        d.rectangle([(525, 255), (575, 265)], fill=(200, 180, 60))  # connector
        img.save(p_trans, format="PNG")
        paths.append(p_trans)
        
        p_susp = os.path.join(INPUT_IMAGES_DIR, "demo_suspension.png")
        # Generate detailed suspension image
        img = Image.new("RGB", (800, 600), (30, 30, 35))
        d = ImageDraw.Draw(img)
        
        # Left side suspension assembly
        # Strut body (shock absorber)
        strut_color = (90, 90, 95)
        d.rectangle([(150, 150), (180, 420)], fill=strut_color)
        d.ellipse([(145, 145), (185, 165)], fill=(110, 110, 115))  # top mount
        # Piston rod
        d.rectangle([(160, 80), (170, 150)], fill=(140, 140, 145))
        d.ellipse([(155, 75), (175, 85)], fill=(120, 120, 125))
        # Coil spring around strut
        spring_color = (70, 70, 75)
        for y in range(160, 400, 20):
            d.arc([(130, y), (200, y+30)], start=180, end=0, fill=spring_color, width=8)
            d.arc([(130, y+10), (200, y+40)], start=0, end=180, fill=spring_color, width=8)
        # Lower control arm
        arm_color = (80, 80, 85)
        d.polygon([(100, 450), (180, 420), (280, 480), (200, 500)], fill=arm_color)
        # Ball joint
        d.ellipse([(155, 415), (185, 445)], fill=(100, 100, 105))
        # Bushing mounts
        d.ellipse([(95, 440), (115, 460)], fill=(50, 50, 55))
        d.ellipse([(270, 470), (290, 490)], fill=(50, 50, 55))
        # Steering knuckle
        knuckle_color = (105, 105, 110)
        d.polygon([(160, 420), (200, 420), (210, 500), (150, 500)], fill=knuckle_color)
        # Wheel bearing hub
        d.ellipse([(155, 480), (205, 530)], fill=(95, 95, 100))
        d.ellipse([(170, 495), (190, 515)], fill=(60, 60, 65))  # center
        
        # Right side suspension assembly (mirror)
        # Strut body
        d.rectangle([(620, 150), (650, 420)], fill=strut_color)
        d.ellipse([(615, 145), (655, 165)], fill=(110, 110, 115))
        # Piston rod
        d.rectangle([(630, 80), (640, 150)], fill=(140, 140, 145))
        d.ellipse([(625, 75), (645, 85)], fill=(120, 120, 125))
        # Coil spring
        for y in range(160, 400, 20):
            d.arc([(600, y), (670, y+30)], start=180, end=0, fill=spring_color, width=8)
            d.arc([(600, y+10), (670, y+40)], start=0, end=180, fill=spring_color, width=8)
        # Lower control arm
        d.polygon([(700, 450), (650, 420), (520, 480), (600, 500)], fill=arm_color)
        # Ball joint
        d.ellipse([(615, 415), (645, 445)], fill=(100, 100, 105))
        # Bushing mounts
        d.ellipse([(685, 440), (705, 460)], fill=(50, 50, 55))
        d.ellipse([(510, 470), (530, 490)], fill=(50, 50, 55))
        # Steering knuckle
        d.polygon([(600, 420), (640, 420), (650, 500), (590, 500)], fill=knuckle_color)
        # Wheel bearing hub
        d.ellipse([(595, 480), (645, 530)], fill=(95, 95, 100))
        d.ellipse([(610, 495), (630, 515)], fill=(60, 60, 65))
        
        # Sway bar connecting both sides
        sway_color = (85, 85, 90)
        d.rectangle([(100, 465), (700, 480)], fill=sway_color)
        # Sway bar links
        d.line([(200, 465), (200, 440)], fill=(75, 75, 80), width=6)
        d.line([(600, 465), (600, 440)], fill=(75, 75, 80), width=6)
        d.ellipse([(195, 435), (205, 445)], fill=(90, 90, 95))
        d.ellipse([(595, 435), (605, 445)], fill=(90, 90, 95))
        
        # Subframe/crossmember
        d.rectangle([(80, 510), (720, 540)], fill=(70, 70, 75))
        # Mounting bolts
        for x in [100, 250, 400, 550, 700]:
            d.ellipse([(x-5, 515), (x+5, 525)], fill=(120, 120, 125))
        
        img.save(p_susp, format="PNG")
        paths.append(p_susp)
        
        # Exhaust system
        p_exhaust = os.path.join(INPUT_IMAGES_DIR, "demo_exhaust.png")
        img = Image.new("RGB", (800, 600), (25, 25, 30))
        d = ImageDraw.Draw(img)
        # Exhaust manifolds (left and right)
        manifold_color = (140, 90, 60)  # rusty/orange cast iron
        d.polygon([(100, 200), (180, 180), (200, 280), (120, 300)], fill=manifold_color)
        d.polygon([(700, 200), (620, 180), (600, 280), (680, 300)], fill=manifold_color)
        # Collector pipes
        pipe_color = (100, 100, 105)
        d.rectangle([(200, 220), (350, 260)], fill=pipe_color)
        d.rectangle([(450, 220), (600, 260)], fill=pipe_color)
        # Catalytic converters (bulbous)
        cat_color = (110, 110, 115)
        d.ellipse([(320, 200), (400, 280)], fill=cat_color)
        d.ellipse([(400, 200), (480, 280)], fill=cat_color)
        # Heat shield pattern
        for i in range(330, 470, 20):
            d.line([(i, 210), (i+10, 270)], fill=(80, 80, 85), width=3)
        # O2 sensors
        sensor_color = (180, 180, 185)
        d.line([(150, 200), (150, 160)], fill=sensor_color, width=4)
        d.ellipse([(145, 155), (155, 165)], fill=sensor_color)
        d.line([(650, 200), (650, 160)], fill=sensor_color, width=4)
        d.ellipse([(645, 155), (655, 165)], fill=sensor_color)
        # Center pipe with flex section
        d.rectangle([(350, 230), (450, 250)], fill=pipe_color)
        # Flex bellows
        for x in range(370, 430, 8):
            d.line([(x, 230), (x, 250)], fill=(70, 70, 75), width=2)
        # Resonator
        d.ellipse([(420, 300), (520, 380)], fill=(90, 90, 95))
        d.rectangle([(400, 330), (420, 350)], fill=pipe_color)  # inlet
        d.rectangle([(520, 330), (540, 350)], fill=pipe_color)  # outlet
        # Main muffler
        d.ellipse([(520, 420), (680, 520)], fill=(85, 85, 90))
        d.rectangle([(540, 460), (560, 480)], fill=pipe_color)  # inlet
        # Perforated pattern on muffler
        for x in range(540, 660, 25):
            for y in range(440, 500, 25):
                d.ellipse([(x, y), (x+5, y+5)], fill=(60, 60, 65))
        # Tailpipes
        d.rectangle([(680, 455), (750, 475)], fill=(110, 110, 115))
        d.rectangle([(680, 485), (750, 505)], fill=(110, 110, 115))
        d.ellipse([(740, 450), (760, 480)], fill=(95, 95, 100))
        d.ellipse([(740, 480), (760, 510)], fill=(95, 95, 100))
        # Hangers
        hanger_color = (50, 50, 55)
        for x in [380, 470, 600]:
            d.rectangle([(x, 260), (x+10, 290)], fill=hanger_color)
            d.ellipse([(x+2, 285), (x+8, 295)], fill=hanger_color)
        img.save(p_exhaust, format="PNG")
        paths.append(p_exhaust)
        
        # Cooling system
        p_cooling = os.path.join(INPUT_IMAGES_DIR, "demo_cooling.png")
        img = Image.new("RGB", (800, 600), (20, 25, 30))
        d = ImageDraw.Draw(img)
        # Radiator
        radiator_color = (90, 90, 95)
        d.rectangle([(250, 150), (550, 450)], fill=radiator_color)
        # Radiator fins/tubes (horizontal pattern)
        for y in range(160, 440, 8):
            d.line([(260, y), (540, y)], fill=(70, 70, 75), width=2)
        # Radiator tanks (top and bottom)
        tank_color = (60, 60, 70)
        d.rectangle([(240, 130), (560, 160)], fill=tank_color)
        d.rectangle([(240, 440), (560, 470)], fill=tank_color)
        # Radiator cap on top
        d.ellipse([(380, 120), (420, 140)], fill=(180, 180, 185))
        d.ellipse([(390, 125), (410, 135)], fill=(140, 140, 145))
        # Expansion tank
        expansion_color = (80, 80, 90)
        d.polygon([(580, 200), (680, 200), (670, 350), (590, 350)], fill=expansion_color)
        d.line([(620, 220), (640, 220)], fill=(200, 200, 210), width=2)  # level marks
        d.line([(620, 260), (640, 260)], fill=(200, 200, 210), width=2)
        d.line([(620, 300), (640, 300)], fill=(200, 200, 210), width=2)
        # Cooling fans behind radiator
        fan_color = (50, 50, 55)
        for x_offset in [0, 150]:
            cx, cy = 320 + x_offset, 300
            d.ellipse([(cx-60, cy-60), (cx+60, cy+60)], fill=fan_color)
            d.ellipse([(cx-10, cy-10), (cx+10, cy+10)], fill=(70, 70, 75))
            # Fan blades
            for angle in range(0, 360, 45):
                import math
                x1 = cx + 15 * math.cos(math.radians(angle))
                y1 = cy + 15 * math.sin(math.radians(angle))
                x2 = cx + 50 * math.cos(math.radians(angle + 15))
                y2 = cy + 50 * math.sin(math.radians(angle + 15))
                d.polygon([(cx, cy), (x1, y1), (x2, y2)], fill=(80, 80, 85))
        # Fan shroud
        d.rectangle([(230, 180), (250, 420)], fill=(70, 70, 75))
        d.rectangle([(550, 180), (570, 420)], fill=(70, 70, 75))
        # Upper radiator hose
        hose_color = (40, 40, 45)
        d.arc([(200, 100), (300, 180)], start=270, end=0, fill=hose_color, width=20)
        d.rectangle([(240, 100), (260, 140)], fill=hose_color)
        # Lower radiator hose
        d.arc([(200, 420), (300, 500)], start=0, end=90, fill=hose_color, width=20)
        d.rectangle([(240, 460), (260, 500)], fill=hose_color)
        # Water pump (on the side)
        pump_color = (100, 100, 105)
        d.ellipse([(150, 250), (220, 320)], fill=pump_color)
        d.ellipse([(170, 270), (200, 300)], fill=(80, 80, 85))  # pulley
        # Thermostat housing
        d.polygon([(220, 140), (280, 140), (270, 180), (230, 180)], fill=(105, 105, 110))
        # Coolant temp sensor
        d.line([(280, 440), (320, 440)], fill=(180, 180, 185), width=5)
        d.rectangle([(315, 435), (330, 445)], fill=(160, 160, 165))
        # Hose clamps
        clamp_color = (150, 150, 155)
        for y in [130, 470]:
            d.rectangle([(248, y), (252, y+10)], fill=clamp_color)
        img.save(p_cooling, format="PNG")
        paths.append(p_cooling)
        
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
