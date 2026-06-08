$sourceDir = "C:\Users\USER\Dropbox\Desarrollos Dropbox"
$destDir = "c:\GRUPO NETCOM DB\Proyectos AGNX\_KiCad_NxLibrary\_Lib_Repository"

$sources = @("SamacSys", "SnapEDA", "NxLibrary")

# Crear estructura
foreach ($src in $sources) {
    $path3d = Join-Path $destDir "$src\3dmodels"
    $pathFp = Join-Path $destDir "$src\footprints\$src.pretty"
    $pathSym = Join-Path $destDir "$src\symbols"
    
    if (-not (Test-Path $path3d)) { New-Item -ItemType Directory -Force -Path $path3d | Out-Null }
    if (-not (Test-Path $pathFp)) { New-Item -ItemType Directory -Force -Path $pathFp | Out-Null }
    if (-not (Test-Path $pathSym)) { New-Item -ItemType Directory -Force -Path $pathSym | Out-Null }
}

$extensions = @("*.step", "*.wrl", "*.kicad_mod", "*.lib", "*.dcm", "*.kicad_sym")
$files = Get-ChildItem -Path $sourceDir -Include $extensions -Recurse -File -ErrorAction SilentlyContinue

$copiedCount = 0
$skippedCount = 0

foreach ($file in $files) {
    # Excluir archivos de cache y rescue específicos de proyecto
    if ($file.Name -match "-cache\.lib$|-rescue\.|-eagle-import\.") {
        continue
    }

    $sourceName = "NxLibrary" # Default for orphans

    if ($file.FullName -match "(?i)samacsys") {
        $sourceName = "SamacSys"
    } elseif ($file.FullName -match "(?i)snapeda") {
        $sourceName = "SnapEDA"
    } elseif ($file.FullName -match "(?i)mouser") {
        $sourceName = "Mouser" # If we want to add more, but let's stick to NxLibrary for others per user request, or maybe add them? Let's just use NxLibrary if it doesn't match SamacSys or SnapEDA.
    }

    $destSubDir = ""
    if ($file.Extension -match "\.step|\.wrl") {
        $destSubDir = "3dmodels"
    } elseif ($file.Extension -match "\.kicad_mod") {
        $destSubDir = "footprints\$sourceName.pretty"
    } elseif ($file.Extension -match "\.lib|\.dcm|\.kicad_sym") {
        $destSubDir = "symbols"
    }

    if ($destSubDir) {
        $targetFolder = Join-Path $destDir "$sourceName\$destSubDir"
        $targetFile = Join-Path $targetFolder $file.Name
        
        if (-not (Test-Path $targetFolder)) {
            New-Item -ItemType Directory -Force -Path $targetFolder | Out-Null
        }

        # Avoid overwriting with the same content, but handle duplicates by renaming or just skipping if exists.
        if (-not (Test-Path $targetFile)) {
            Copy-Item -Path $file.FullName -Destination $targetFile -Force
            $copiedCount++
        } else {
            # Si el archivo ya existe y tienen diferente tamaño, podríamos renombrarlo, pero por ahora lo omitimos.
            $skippedCount++
        }
    }
}

Write-Host "Copia completada. Archivos copiados: $copiedCount, Omitidos (ya existentes o duplicados): $skippedCount"
