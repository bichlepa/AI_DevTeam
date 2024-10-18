import os
import json5
import fnmatch
import re

from config import PROJECT_DIR, PROJECT_OVERVIEW_DIR, PROJECT_STAKEHOLDER_REQS_DIR, PROJECT_SYSTEM_REQS_DIR, PROJECT_ARCHITECTURE_DIR, PROJECT_COMPONENT_REQS_DIR, PROJECT_COMPONENT_DESIGN_DIR, PROJECT_SOURCE_CODE_DIR, PROJECT_TESTPLAN_DIR, PROJECT_TESTCASES_DIR, PROJECT_TEST_IMPLEMENTATION_DIR

import os
import fnmatch

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

    def count_items(directory):
        """
        Zählt die Anzahl der Dateien und Ordner in einem Verzeichnis.
        """
        try:
            items = os.listdir(directory)
        except PermissionError:
            return 0, 0  # Ignoriere Ordner ohne Berechtigungen
        
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
        return len(files), len(dirs)

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
                relative_folder = os.path.relpath(folder_path, base_dir)
                if relative_folder in expanded_folders:
                    connector = "└── " if idx == len(dirs) - 1 else "├── "
                    file_tree.append(f"{prefix}{connector}{folder}/")
                    new_prefix = f"{prefix}{'    ' if idx == len(dirs) - 1 else '│   '}"
                    walk_directory(folder_path, new_prefix)
                    # Check if the expanded folder is empty
                    if not files and not dirs:
                        file_tree.append(f"{new_prefix}(empty)")
                else:
                    file_count, dir_count = count_items(folder_path)
                    connector = "└── " if idx == len(dirs) - 1 else "├── "
                    file_tree.append(f"{prefix}{connector}{folder}/ ({file_count} files, {dir_count} dirs)")

    # Starte das Traversieren vom Root-Verzeichnis
    walk_directory(base_dir)
    return file_tree

def file_exists(home_dir, file_path):
    # Prüft, ob die angegebene Datei existiert
    # Gibt eine Struktur zurück: { "exists": <True/False>, "error": <Fehlermeldung> }

    # Pfade ggf. anpassen
    file_path = process_path(home_dir, file_path)

    if os.path.exists(file_path):
        return True
    else:
        return False

def folder_exists(home_dir, folder_path):
    # Prüft, ob der angegebene Ordner existiert
    # Gibt eine Struktur zurück: { "exists": <True/False>, "error": <Fehlermeldung> }

    # Pfade ggf. anpassen
    folder_path = process_path(home_dir, folder_path)

    if os.path.exists(folder_path):
        return True
    else:
        return False

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

    success = True
    error = "" # todo Fehlermeldungen

    try:
        # Pfade ggf. anpassen
        file_path = process_path(home_dir, file_path)

        # Ordner erstellen, falls sie nicht existieren
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Schreibt den gegebenen Inhalt in die angegebene Datei
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        error = str(e)
        success = False
    
    return {"success": success, "error": error}


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


#file.search_file_content(home_dir, action["parameters"]["folder_path"], action["parameters"]["search_string"], action["parameters"].get("use_regex", False), action["parameters"].get("whole_word", False), action["parameters"].get("case_sensitive", False), action["parameters"].get("file_mask", "*"))

def search_file_content(home_dir, folder_path, search_string, use_regex=False, whole_word=False, case_sensitive=False, file_mask="*"):
    # Sucht nach Dateien, die den Suchbegriff enthalten

    # Pfade ggf. anpassen
    folder_path = process_path(home_dir, folder_path)

    # Sucht nach Dateien, die den Suchbegriff enthalten
    search_results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not case_sensitive:
                    content = content.lower()
                    search_string = search_string.lower()
                if use_regex:
                    if re.search(search_string, content):
                        search_results.append(file_path)
                elif whole_word:
                    if f" {search_string} " in f" {content} ":
                        search_results.append(file_path)
                else:
                    if search_string in content:
                        search_results.append(file_path)
    
    # alle Pfade relativ machen
    search_results = [os.path.relpath(path, PROJECT_DIR) for path in search_results]
    return search_results

#search_results = file.search_file_name(home_dir, action["parameters"]["folder_path"], action["parameters"]["file_mask"], action["parameters"].get("find_files", True), action["parameters"].get("find_folders", False))

def search_file_name(home_dir, folder_path, file_mask, find_files=True, find_folders=False):
    # Sucht nach Dateien, die den Dateinamen enthalten

    # Pfade ggf. anpassen
    folder_path = process_path(home_dir, folder_path)

    # Sucht nach Dateien, die den Dateinamen enthalten
    search_results = []
    for root, dirs, files in os.walk(folder_path):
        if find_folders:
            for dir in dirs:
                if fnmatch.fnmatch(dir, file_mask):
                    search_results.append(os.path.join(root, dir))
        if find_files:
            for file in files:
                if fnmatch.fnmatch(file, file_mask):
                    search_results.append(os.path.join(root, file))

    # alle Pfade relativ machen
    search_results = [os.path.relpath(path, PROJECT_DIR) for path in search_results]
    return search_results

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
