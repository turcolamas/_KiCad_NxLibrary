import os
import glob

def merge_kicad_sym(directory, output_file):
    symbols = []
    files = glob.glob(os.path.join(directory, "*.kicad_sym"))
    for file in files:
        if os.path.basename(file) == output_file:
            continue
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find the first (symbol ...
            start = content.find('\n  (symbol')
            if start == -1:
                start = content.find('\n(symbol')
            if start != -1:
                end = content.rfind(')')
                if end != -1:
                    symbols.append(content[start:end].strip())
    
    if symbols:
        out_path = os.path.join(directory, output_file)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('(kicad_symbol_lib (version 20211014) (generator kicad_symbol_editor)\n')
            for sym in symbols:
                f.write('  ' + sym + '\n')
            f.write(')\n')
        print(f"Merged {len(symbols)} components into {output_file}")

def merge_legacy_lib(directory, output_lib, output_dcm):
    defs = []
    cmps = []
    
    # Merge .lib
    lib_files = glob.glob(os.path.join(directory, "*.lib"))
    for file in lib_files:
        if os.path.basename(file).lower() in [output_lib.lower(), "st-microelectronics.lib"]:
            if os.path.basename(file).lower() == output_lib.lower(): continue
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            in_def = False
            current_def = []
            for line in lines:
                if line.startswith('DEF '):
                    in_def = True
                    current_def = []
                if in_def:
                    current_def.append(line)
                if line.startswith('ENDDEF'):
                    in_def = False
                    defs.append("".join(current_def))

    if defs:
        out_path = os.path.join(directory, output_lib)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('EESchema-LIBRARY Version 2.4\n#encoding utf-8\n')
            for d in defs:
                f.write('#\n')
                f.write(d)
            f.write('#\n#End Library\n')
        print(f"Merged {len(defs)} legacy symbols into {output_lib}")

    # Merge .dcm
    dcm_files = glob.glob(os.path.join(directory, "*.dcm"))
    for file in dcm_files:
        if os.path.basename(file) == output_dcm:
            continue
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            in_cmp = False
            current_cmp = []
            for line in lines:
                if line.startswith('$CMP '):
                    in_cmp = True
                    current_cmp = []
                if in_cmp:
                    current_cmp.append(line)
                if line.startswith('$ENDCMP'):
                    in_cmp = False
                    cmps.append("".join(current_cmp))

    if cmps:
        out_path = os.path.join(directory, output_dcm)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('EESchema-DOCLIB  Version 2.0\n')
            for c in cmps:
                f.write('#\n')
                f.write(c)
            f.write('#\n#End Doc Library\n')
        print(f"Merged {len(cmps)} documentation blocks into {output_dcm}")


if __name__ == '__main__':
    target_dir = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\NxLibrary\symbols"
    merge_kicad_sym(target_dir, "NxLibrary_Merged.kicad_sym")
    merge_legacy_lib(target_dir, "NxLibrary_Merged.lib", "NxLibrary_Merged.dcm")
