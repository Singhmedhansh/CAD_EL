"""Quick validation script to show engine BOM structure"""
import sys
sys.path.insert(0, '.')

from src.bom_templates import engine_assembly_bom

items = engine_assembly_bom()
assemblies = [i for i in items if i.get('Level', 0) == 1]
parts_per_asm = {}

for asm in assemblies:
    asm_no = asm['Item No']
    parts = [i for i in items if str(i['Item No']).startswith(asm_no + '.') and i.get('Level', 0) == 2]
    parts_per_asm[asm['Part Name']] = len(parts)

print('\n' + '='*60)
print('ENGINE BOM STRUCTURE VALIDATION')
print('='*60)
print(f'Main Assembly: V6 Engine (Level 0)')
print(f'Sub-Assemblies: {len(assemblies)}')
for name, count in parts_per_asm.items():
    print(f'  ├─ {name}: {count} parts')
print(f'\nTotal BOM Items: {len(items)}')
print(f'  (1 main + {len(assemblies)} sub-assemblies + {sum(parts_per_asm.values())} parts)')
print('='*60)
