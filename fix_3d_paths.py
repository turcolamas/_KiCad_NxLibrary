import os
import re

# Configuración de Rutas
# Carpeta donde se encuentran todos tus footprints (.kicad_mod)
repository_dir = r"c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\_Lib_Repository"

# La variable de entorno que crearás en KiCad (Preferencias -> Configurar Rutas)
# Apuntará a la ruta de tu _Lib_Repository
env_var = "${NX_LIBRARY}" 

def process_footprint(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    changed = False
    new_lines = []
    
    # Expresión regular para capturar la ruta del archivo 3D
    # Busca "(model " seguido opcionalmente de comillas, luego cualquier texto hasta la extensión
    model_regex = re.compile(r'\(model\s+["\']?(.*?\.(?:wrl|step|stp|STEP|STP|WRL))["\']?')
    
    for line in lines:
        if "(model " in line:
            match = model_regex.search(line)
            if match:
                old_path = match.group(1)
                
                # Extraer solo el nombre del archivo (ej. "IR2117S.stp")
                filename = os.path.basename(old_path.replace('\\', '/')) 
                
                # Detectar la categoría analizando en qué carpeta está el archivo .kicad_mod
                filepath_lower = filepath.lower()
                if "samacsys" in filepath_lower:
                    category = "SamacSys"
                elif "snapeda" in filepath_lower:
                    category = "SnapEDA"
                else:
                    category = "NxLibrary" # Por defecto
                
                # Construir la nueva ruta usando la variable de entorno
                new_path = f'{env_var}/{category}/3dmodels/{filename}'
                
                # Evitar procesar si ya está correcto
                if old_path != new_path:
                    # Reemplazamos exactamente lo que capturó la regex por la nueva ruta entre comillas dobles
                    match_str = match.group(0)
                    new_line = line.replace(match_str, f'(model "{new_path}"')
                    new_lines.append(new_line)
                    changed = True
                    continue
                
        new_lines.append(line)
        
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    print(f"Buscando archivos .kicad_mod en: {repository_dir}\n")
    modified_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(repository_dir):
        for file in files:
            if file.endswith('.kicad_mod'):
                full_path = os.path.join(root, file)
                try:
                    if process_footprint(full_path):
                        modified_count += 1
                        print(f"Modificado: {file}")
                except Exception as e:
                    print(f"Error procesando {file}: {e}")
                    error_count += 1
                    
    print("\n" + "="*50)
    print("¡PROCESO COMPLETADO!")
    print(f"Footprints actualizados: {modified_count}")
    if error_count > 0:
        print(f"Errores encontrados: {error_count}")
        
    print("\nSIGUIENTE PASO EN KICAD:")
    print("1. Abre KiCad.")
    print("2. Ve a Preferencias -> Configurar Rutas... (Configure Paths...).")
    print(f"3. Añade una nueva variable llamada: NX_LIBRARY")
    print(f"4. Ponle esta ruta: {repository_dir}")
    print("="*50)

if __name__ == "__main__":
    main()
