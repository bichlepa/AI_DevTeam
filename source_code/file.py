import os
import json5
import fnmatch

from config import PROJECT_DIR, PROJECT_OVERVIEW_DIR, PROJECT_STAKEHOLDER_REQS_DIR, PROJECT_SYSTEM_REQS_DIR, PROJECT_ARCHITECTURE_DIR, PROJECT_COMPONENT_REQS_DIR, PROJECT_COMPONENT_DESIGN_DIR, PROJECT_SOURCE_CODE_DIR, PROJECT_TESTPLAN_DIR, PROJECT_TESTCASES_DIR, PROJECT_TEST_IMPLEMENTATION_DIR

def get_file_list(base_dir_ = "", expanded_folders_ = [], excluded_files_ = []):
    """
    Erstellt eine Liste aller Dateien in allen aufgeklappten Ordnern und bildet die Baumstruktur mit ASCII-Zeichen ab.
    Berücksichtigt dabei relative Verzeichnisse und ausgeschlossene Dateien/Ordner.
    """

    base_dir = os.path.join(PROJECT_DIR, base_dir_)
    
    file_tree = []
    excluded_files = excluded_files_
    expanded_folders = expanded_folders_

    def is_excluded(path):
        """
        Überprüft, ob ein Pfad (Datei oder Ordner) anhand der excluded_files ausgeschlossen werden soll.
        """
        relative_path = os.path.relpath(path, base_dir)
        for pattern in excluded_files:
            if fnmatch.fnmatch(relative_path, pattern):
                return True
        return False

    def walk_directory(directory, prefix=""):
        # Holt die Dateien und Ordner im aktuellen Verzeichnis
        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            return  # Ignoriere Ordner ohne Berechtigungen
        
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]

        # Füge Dateien zur Liste hinzu
        for idx, file in enumerate(files):
            file_path = os.path.join(directory, file)
            if not is_excluded(file_path):
                connector = "└── " if idx == len(files) - 1 and not dirs else "├── "
                file_tree.append(f"{prefix}{connector}{file}")

        # Füge Unterordner hinzu
        for idx, folder in enumerate(dirs):
            folder_path = os.path.join(directory, folder)
            if not is_excluded(folder_path):
                connector = "└── " if idx == len(dirs) - 1 else "├── "
                file_tree.append(f"{prefix}{connector}{folder}/")

                # Rekursiver Aufruf nur für erweiterte Ordner
                relative_folder = os.path.relpath(folder_path, base_dir)
                if relative_folder in expanded_folders:
                    new_prefix = f"{prefix}{'    ' if idx == len(dirs) - 1 else '│   '}"
                    walk_directory(folder_path, new_prefix)

    # Starte das Traversieren vom Root-Verzeichnis
    walk_directory(base_dir)
    return file_tree


def read_file(home_dir, file_path):
    # Liest den Inhalt einer Datei und gibt ihn zurück
    # Gibt eine Struktur zurück: { "content": <Inhalt der Datei>, "success": <True/False>, "error": <Fehlermeldung> }

    # Pfade ggf. anpassen
    file_path = process_path(home_dir, file_path)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return {"content": file.read(), "success": True}
    else:
        return {"content": "", "success": False, "error": "Die Datei existiert nicht."}


def write_file(home_dir, file_path, content):
    # Schreibt den gegebenen Inhalt in die angegebene Datei

    success = True # todo Erfolgskontrolle

    # Pfade ggf. anpassen
    file_path = process_path(home_dir, file_path)

    # Schreibt den gegebenen Inhalt in die angegebene Datei
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return success


def create_folder(home_dir, folder_path):
    # Erstellt einen neuen Ordner

    success = True # todo Erfolgskontrolle

    # Pfade ggf. anpassen
    folder_path = process_path(home_dir, folder_path)

    # Erstellt den Ordner
    os.makedirs(folder_path, exist_ok=True)

    return success

def delete_file(home_dir, file_path):
    # Löscht die angegebene Datei

    success = True # todo Erfolgskontrolle

    # Pfade ggf. anpassen
    file_path = process_path(home_dir, file_path)

    # Löscht die Datei
    os.remove(file_path)

    return success

def delete_folder(home_dir, folder_path, recursive=False):
    # Löscht den angegebenen Ordner

    # Pfade ggf. anpassen
    folder_path = process_path(home_dir, folder_path)

    # Löscht den Ordner
    if recursive:
        os.removedirs(folder_path)
    else:
        os.rmdir(folder_path)




def read_json(file_path):
    # Liest den Inhalt einer JSON-Datei und gibt ihn zurück
    # Wenn die Datei nicht existiert, wird ein leeres Dictionary zurückgegeben

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json5.load(file)
    else:
        return {}


def process_path(home_dir, path):
    # Ersetzt das Home-Verzeichniszeichen (~) durch das tatsächliche Home-Verzeichnis
    path = path.replace("~", home_dir)

    # Fügt das Projektverzeichnis dem relativen Pfad hinzu
    path = os.path.join(PROJECT_DIR, path)

    return path
