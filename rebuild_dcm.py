import os
import glob
import re

lib_path = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged_old.lib"
dcm_out_path = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged_old.dcm"
symbols_dir = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols"

# 1. Get all valid component names from the .lib file
valid_names = set()
with open(lib_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('DEF '):
            name = line.strip().split()[1]
            valid_names.add(name)

# 2. Iterate through all .dcm files and extract matching blocks
dcm_files = glob.glob(os.path.join(symbols_dir, "*.dcm"))
new_dcm_blocks = []

for dcm_file in dcm_files:
    if "NxLibrary_Merged" in dcm_file:
        continue
        
    with open(dcm_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Match $CMP blocks
    blocks = re.findall(r'(\$CMP\s+(.*?)\r?\n.*?(?:\$ENDCMP\r?\n|\$ENDCMP$))', content, re.DOTALL | re.MULTILINE)
    for block_text, cmp_name in blocks:
        cmp_name_clean = cmp_name.strip().replace(' ', '_')
        if cmp_name_clean in valid_names:
            # Reconstruct block with cleaned name
            lines = block_text.splitlines()
            if lines:
                lines[0] = f"$CMP {cmp_name_clean}"
            clean_block = "\n".join(lines) + "\n"
            new_dcm_blocks.append(clean_block)

# 3. Write out the new DCM file
with open(dcm_out_path, 'w', encoding='utf-8') as f:
    f.write("EESchema-DOCLIB  Version 2.0\n")
    for block in new_dcm_blocks:
        f.write("#\n")
        f.write(block)
    f.write("#\n#End Doc Library\n")

print(f"Written {len(new_dcm_blocks)} valid DCM blocks.")
