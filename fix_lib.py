import os

lib_file = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged.lib"
new_lib = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged_old.lib"

with open(lib_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('DEF '):
        parts = line.strip().split()
        if len(parts) > 9:
            standard_parts = parts[-7:]
            ref = parts[-8]
            name_parts = parts[1:-8]
            name = "_".join(name_parts)
            new_line = "DEF " + name + " " + ref + " " + " ".join(standard_parts) + "\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    elif line.startswith('F1 '):
        parts = line.split('"')
        if len(parts) >= 3 and ' ' in parts[1]:
            parts[1] = parts[1].replace(' ', '_')
            new_lines.append('"'.join(parts))
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(new_lib, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)


dcm_file = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged.dcm"
new_dcm = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols\NxLibrary_Merged_old.dcm"

if os.path.exists(dcm_file):
    with open(dcm_file, 'r', encoding='utf-8', errors='ignore') as f:
        dcm_lines = f.readlines()

    new_dcm_lines = []
    for line in dcm_lines:
        if line.startswith('$CMP '):
            name = line[5:].strip()
            new_name = name.replace(' ', '_')
            new_dcm_lines.append('$CMP ' + new_name + '\n')
        else:
            new_dcm_lines.append(line)

    with open(new_dcm, 'w', encoding='utf-8') as f:
        f.writelines(new_dcm_lines)
