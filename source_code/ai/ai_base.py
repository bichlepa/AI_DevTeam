"""
Basisklasse für alle KI-Agenten.
"""
import os

import logging
import ai_interface
import config
import file
import prompts.base as base_prompts

class AI_Agent:
    name = "undefined"
    role = "undefined"
    role_ID = "undefined"
    prompts = base_prompts

    def __init__(self, data):
        self.context = []

        # Home-Verzeichnis der KI = Projektverzeichnis / self.role_ID
        self.home_dir = os.path.join("ai_homes" , self.role_ID)

        self.data = data
        self.data["name"] = self.name
        self.data["role"] = self.role
        self.data["role_ID"] = self.role_ID
        self.data["role_description"] = self.role_description
        
        # Systemprompt erstellen
        prompt = self._build_first_system_prompt(data)
        self.context.append({"role": "system", "content": prompt})

        # Datei "~/autorun.json" lesen, wenn sie existiert
        autostart_file_path = os.path.join(config.PROJECT_DIR, self.home_dir, "autorun.json")
        if os.path.exists(autostart_file_path):
            autostart_file = file.read_json(autostart_file_path)

            # Aufgeklappte Dateien auslesen
            self.data["expanded_folders"] = autostart_file.get("expand_folders", [])

            # Geöffnete Dateien auslesen
            self.data["opened_files"] = autostart_file.get("open_files", [])
        else:
            self.data["expanded_folders"] = []
            self.data["opened_files"] = []

    def next_step(self, data):
        """
        Führt einen Schritt aus.
        """

        # Allgemeine Daten für die Prompts
        prompt_data = self.data.copy()
        # data mit den spezifischen Daten überschreiben
        prompt_data.update(data)

        # Dateiliste für den Agenten erstellen
        filelist = self._create_file_list(self.data["expanded_folders"])
        # Einen String aus der Dateiliste erstellen
        prompt_data["file_list"] = "\n".join(filelist)

        # Dateien, die dem Agenten gezeigt werden
        prompt_data["opened_files"] = self._read_files(self.data["opened_files"])

        # Prompt für die KI bauen
        prompt = self._build_next_prompt(prompt_data)

        # Systemprompt erstellen, der an jeden Schritt angehängt wird
        prompt_system = self._build_next_system_prompt(prompt_data)

        # Nachricht an die KI senden
        response = self._send_message_to_ai(prompt, prompt_system)

        return response

    def update_data(self, data):
        """
        Aktualisiert die Daten des Agenten.
        """
        self.data.update(data)

    def get_data(self, key):
        """
        Gibt die Daten des Agenten zurück.
        """
        return self.data.get(key, None)

    def get_home_dir(self):
        """
        Gibt das Home-Verzeichnis der KI zurück.
        """
        return self.home_dir

    def _build_first_system_prompt(self, data):
        """
        Setzt den Systemprompt für die KI.
        """
        prompt = self.prompts.system_prompt

        # fülle Platzhalter im Prompt
        prompt = self._fill_prompt_template(prompt, data)
        
        return prompt
    
    def _build_next_system_prompt(self, data):
        """
        Setzt den Systemprompt für die KI.
        """
        prompt = self.prompts.system_prompt_on_each_iteration

        # fülle Platzhalter im Prompt
        prompt = self._fill_prompt_template(prompt, data)
        
        return prompt

    def _build_first_prompt(self, data):
        """
        Baut den Prompt für die KI aus den Nachrichten im Kontext.
        """
        prompt = self.prompts.first_prompt
        
        # fülle Platzhalter im Prompt
        prompt = self._fill_prompt_template(prompt, data)
        
        return prompt

    def _build_next_prompt(self, data):
        """
        Baut den Prompt für die KI aus den Nachrichten im Kontext.
        """
        prompt = self.prompts.next_prompt
        
        # fülle Platzhalter im Prompt
        prompt = self._fill_prompt_template(prompt, data)
        
        return prompt
    
    def _fill_prompt_template(self, template, data):
        # Promptplatzhalter aus self.prompts mit den gegebenen Werten füllen. Sie beginnen mit "a_".
        for key in dir(self.prompts):
            if key.startswith("a_"):
                data[key] = getattr(self.prompts, key)

        # Einige generische Platzhalter leer machen, wenn keine Daten vorhanden sind
        if not data.get("received_message", ""):
            data["a_received_message"] = ""
        if not data.get("computer_message", ""):
            data["a_computer_message"] = ""
        if not data.get("computer_question", ""):
            data["a_computer_question"] = ""
        if not data.get("answer_to_question", ""):
            data["a_answer_to_question"] = ""
        
        # Weitere Felder mit leeren Strings füllen, wenn sie nicht vorhanden sind
        if not data.get("question", ""):
            data["question"] = ""
        
        # Ersetzt Platzhalter im Template durch die gegebenen Werte. Mehrfach wegen verschachtelter Platzhalter.
        return template.format(**data).format(**data)

    def _send_message_to_ai(self, prompt, prompt_system = ""):
        """
        Sendet eine Nachricht an die KI und gibt die Antwort zurück.
        Speichert die Nachrichten in self.context.
        """

        # Prompts in den Kontext einfügen
        self.context.append({"role": "user", "content": prompt})
        if prompt_system:
            self.context.append({"role": "system", "content": prompt_system})

        # Loggen
        logging.info(f"Sending prompt to AI with context length {len(self.context)}")
        if (len(self.context) == 3):
            logging.info(f"This is the first system message: {self.context[0].get('content')}")
        logging.info(f"This is the user message: {prompt}")
        logging.info(f"This is the appended system message: {prompt_system}")

        # Nachricht an die KI senden
        response = ai_interface.send_message_to_ai(self.context)

        # Loggen
        logging.info(f"Received response from AI:\n{response}")

        # Systemprompt wieder aus dem Kontext entfernen
        if prompt_system:
            self.context.pop()
        # Antwort in den Kontext einfügen
        self.context.append({"role": "assistant", "content": response})

        return response

    def _read_files(self, files):
        """
        Liest den Inhalt von Dateien ein und erzeugt einen String für die KI.
        """
        file_content = ""
        for onefile in files:
            # home-Verzeichnis ersetzen, falls vorhanden
            onefile = onefile.replace("~/", self.home_dir)

            # Datei einlesen
            file_content += f"`{onefile}`\n\"\"\"\n{file.read_file(self.home_dir, onefile)["content"]}\n\"\"\"\n\n"
        
        if not file_content:
            file_content = "No files opened."
        return file_content
    
    def _create_file_list(self, expanded_folders, excluded_files=[]):
        home_files = file.get_file_list(self.home_dir, expanded_folders)
        project_files = file.get_file_list(config.PROJECT_DIR, expanded_folders, excluded_files)
        
        return home_files + project_files