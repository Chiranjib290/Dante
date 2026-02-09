#!/usr/bin/env python3
import os
import zipfile
from email.parser import Parser

def get_manifest_from_file(manifest_path):
    """
    Reads a MANIFEST.MF file from a directory and returns a dictionary 
    of manifest attributes.
    """
    try:
        with open(manifest_path, 'r', encoding='utf-8', errors='replace') as f:
            data = f.read()
        parser = Parser()
        return dict(parser.parsestr(data))
    except Exception:
        return None

def get_manifest_from_jar(jar_path):
    """
    Reads the MANIFEST.MF from a JAR file by opening it as a ZIP archive.
    """
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            # Look for the manifest file regardless of case.
            manifest_names = [name for name in jar.namelist() if name.upper().endswith("META-INF/MANIFEST.MF")]
            if manifest_names:
                with jar.open(manifest_names[0]) as mf:
                    data = mf.read().decode('utf-8', errors='replace')
                parser = Parser()
                return dict(parser.parsestr(data))
    except Exception:
        return None

def list_bundles(bundles_dir):
    """
    Recursively searches for bundle manifest information in both JAR files and
    directories containing a manifest. For JAR files found in nested directories,
    the top-level folder (if present) is used as the bundle id.
    Returns a list of dictionaries with bundle details.
    """
    bundles = {}
    if not os.path.exists(bundles_dir):
        print(f"Error: Bundles directory '{bundles_dir}' does not exist.")
        return []

    for root, dirs, files in os.walk(bundles_dir):
        # Process JAR files first.
        for file in files:
            if file.lower().endswith(".jar"):
                jar_path = os.path.join(root, file)
                # Compute a relative path from the bundle root directory.
                rel_path = os.path.relpath(jar_path, bundles_dir)
                parts = rel_path.split(os.sep)
                # Use the top-level folder as the bundle ID if available.
                bundle_id = parts[0] if len(parts) > 1 else os.path.splitext(file)[0]
                if bundle_id not in bundles:
                    manifest = get_manifest_from_jar(jar_path)
                    bundles[bundle_id] = {
                        "id": bundle_id,
                        "name": manifest.get("Bundle-Name", "N/A") if manifest else "N/A",
                        "symbolic_name": manifest.get("Bundle-SymbolicName", "N/A") if manifest else "N/A",
                        "version": manifest.get("Bundle-Version", "N/A") if manifest else "N/A",
                    }
        # Process directories that might be exploded bundles.
        for d in dirs:
            dir_path = os.path.join(root, d)
            standard_manifest = os.path.join(dir_path, "META-INF", "MANIFEST.MF")
            if os.path.isfile(standard_manifest):
                rel_path = os.path.relpath(dir_path, bundles_dir)
                parts = rel_path.split(os.sep)
                bundle_id = parts[0] if len(parts) > 0 else d
                if bundle_id not in bundles:
                    manifest = get_manifest_from_file(standard_manifest)
                    bundles[bundle_id] = {
                        "id": bundle_id,
                        "name": manifest.get("Bundle-Name", "N/A") if manifest else "N/A",
                        "symbolic_name": manifest.get("Bundle-SymbolicName", "N/A") if manifest else "N/A",
                        "version": manifest.get("Bundle-Version", "N/A") if manifest else "N/A",
                    }
    return list(bundles.values())

def print_bundles_table(bundles):
    """
    Prints out the bundle information in a formatted table.
    """
    headers = ["Bundle ID", "Bundle Name", "Symbolic Name", "Version"]
    # Determine maximum width for each column.
    col_widths = {header: len(header) for header in headers}
    for bundle in bundles:
        col_widths["Bundle ID"] = max(col_widths["Bundle ID"], len(str(bundle.get("id", ""))))
        col_widths["Bundle Name"] = max(col_widths["Bundle Name"], len(str(bundle.get("name", ""))))
        col_widths["Symbolic Name"] = max(col_widths["Symbolic Name"], len(str(bundle.get("symbolic_name", ""))))
        col_widths["Version"] = max(col_widths["Version"], len(str(bundle.get("version", ""))))
        
    header_row = (
        f"{headers[0]:<{col_widths['Bundle ID']+2}} "
        f"{headers[1]:<{col_widths['Bundle Name']+2}} "
        f"{headers[2]:<{col_widths['Symbolic Name']+2}} "
        f"{headers[3]:<{col_widths['Version']+2}}"
    )
    print(header_row)
    print("-" * len(header_row))
    
    for bundle in bundles:
        row = (
            f"{bundle.get('id', 'N/A'):<{col_widths['Bundle ID']+2}} "
            f"{bundle.get('name', 'N/A'):<{col_widths['Bundle Name']+2}} "
            f"{bundle.get('symbolic_name', 'N/A'):<{col_widths['Symbolic Name']+2}} "
            f"{bundle.get('version', 'N/A'):<{col_widths['Version']+2}}"
        )
        print(row)

if __name__ == '__main__':
    # Hard-code your Felix root path here.
    bundles_dir = r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\launchpad\felix"
    
    bundles = list_bundles(bundles_dir)
    if bundles:
        print("\nAEM Bundles Details:")
        print_bundles_table(bundles)
    else:
        print("No bundle details were found. Please check the provided bundles directory.")
