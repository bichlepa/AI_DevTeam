"""
Klasse AI_Computer abgeleitet von AI_Agent.
"""

import os
import logging

import ai_interface
import config
import file
from ai.ai_base import AI_Agent
from prompts.computer import ComputerPrompts



class AI_Computer(AI_Agent):
    name = "Computer"
    role = "Computer"
    role_ID = "computer"
    prompts = ComputerPrompts
    role_description = ComputerPrompts.role_description
    skip_in_role_list = True

    def __init__(self, data):
        super().__init__(data)


    def next_step(self, data):
        pass # Basisklasse Funktion nicht verwenden

    def start(self, data):
        """
        Starte mit der Ausführung des Ablaufs.
        Parameter data enthält
        - project_name: Name des Projekts
        - all_role_descriptions: Beschreibungen aller Rollen
        - all_agents: Objekte aller Agenten
        Der logische Ablauf ist wie folgt:
        - Nachricht an Benutzer vorbeiten (Er ist quasi der erste Agent)
        - Schleife:
            - Nachricht an den Agenten senden
            - Antwort des Agenten an die KI zum Auswerten senden
            - Antwort der KI parsen und enthaltene Aktionen durchführen
                - Falls eine Aktion heißt, eine Nachricht an ein Teammitglied zu senden: Ziel-Agenten ändern und Nachricht speichern
                - Falls eine Aktion heißt, dass die Agenten fertig sind: Schleife beenden
        """

        # Daten, die bei der Initialisierung übergeben wurden, der Variable data hinzufügen
        data.update(self.data)

        # Erste Nachricht an den Benutzer vorbereiten
        data["next_message"] = self.prompts.first_message_to_user
        data["next_sender"] = "System"
        data["next_receiver"] = config.USER_NAME
        

        # Die Schleife beginnt damit, dass eine Nachricht an den Agenten gesendet wird
        # im ersten Schritt ist der Benutzer der Agent, danach je nach dem an wen die Nachricht geht
        max_iterations = 100
        iterations = 0
        while iterations < max_iterations:
            # Nachricht an den Agenten senden
            data["current_receiver"] = data["next_receiver"]
            data["current_sender"] = data["next_sender"]
            data["received_message"] = data["next_message"]

            if data["current_sender"] == "System":
                current_sender_agent = None
                data["message_sender_name"] = "System"
                data["message_sender_role"] = "System"
            else:
                current_sender_agent = self.data["all_agents_by_name"][data["current_sender"]]
                data["message_sender_name"] = current_sender_agent.name
                data["message_sender_role"] = current_sender_agent.role
                
            current_reiceiver_agent = self.data["all_agents_by_name"][data["current_receiver"]]
            data["message_receiver_name"] = current_reiceiver_agent.name
            data["message_receiver_role"] = current_reiceiver_agent.role

            response = current_reiceiver_agent.next_step(data)
            data["next_sender"] = None
            data["next_receiver"] = None
            data["next_message"] = None
            data["computer_message"] = None

            # Die Antwort enthält Anweisungen für den Computer. Diese werden jetzt durch den Computer-KI-Agenten ausgewertet.
            
            # Prompt für die KI bauen

            # Bisherigen Kontext löschen
            self.context = []

            # Systemprompt erstellen
            prompt_data = data.copy()
            prompt_system = self._build_first_system_prompt(data)
            self.context.append({"role": "system", "content": prompt_system})

            # Ersten Prompt für die KI bauen
            prompt_data = data.copy()
            prompt_data["agent_message"] = response
            filelist = current_reiceiver_agent.get_data("opened_files")
            prompt_data["opened_files"] ="\n".join(filelist)
            
            filelist = current_reiceiver_agent.get_data("expanded_folders")
            prompt_data["expanded_folders"] ="\n".join(filelist)
            prompt = self._build_first_prompt(prompt_data)

            ai_finished = False
            while(not ai_finished):

                # Nachricht an die KI senden
                response = self._send_message_to_ai(prompt)

                # Antwort der KI parsen
                allActions = self._parse_ai_response(response)
                logging.info(f"Geparste Aktionen: {allActions}")

                # Infos vorbereiten
                home_dir = current_reiceiver_agent.get_home_dir()
                data["question"] = None
                data["answer_to_question"] = None

                # Aktionen durchführen (wie in computer.py definiert)
                action_results = []
                for action in allActions:
                    if action["name"] == "view_file":
                        # Liste geöffneter Dateien im Agenten aktualisieren
                        filelist = current_reiceiver_agent.get_data("opened_files")
                        # prüfen ob nicht schon geöffnet
                        if action["parameters"]["file_path"] not in filelist:
                            filelist.append(action["parameters"]["file_path"])
                            action_results.append(f"File {action['parameters']['file_path']} opened.")
                        else:
                            action_results.append(f"File {action['parameters']['file_path']} is already open.")
                        current_reiceiver_agent.update_data({"opened_files": filelist})
                    elif action["name"] == "close_file":
                        # Liste geöffneter Dateien im Agenten aktualisieren
                        filelist = current_reiceiver_agent.get_data("opened_files")
                        # prüfen ob geöffnet
                        if action["parameters"]["file_path"] in filelist:
                            action_results.append(f"File {action['parameters']['file_path']} closed.")
                            filelist.remove(action["parameters"]["file_path"])
                        else:
                            action_results.append(f"File {action['parameters']['file_path']} was not open.")
                        current_reiceiver_agent.update_data({"opened_files": filelist})
                    elif action["name"] == "write_file":
                        # Datei schreiben
                        result = file.write_file(home_dir, action["parameters"]["file_path"], action["content"])
                        if result:
                            action_results.append(f"File {action['parameters']['file_path']} written.")
                        else:
                            action_results.append(f"File {action['parameters']['file_path']} could not be written.")
                    elif action["name"] == "create_folder":
                        # Ordner erstellen
                        result = file.create_folder(home_dir, action["parameters"]["folder_path"])
                        if result["success"]:
                            action_results.append(f"Folder {action['parameters']['folder_path']} created.")
                        else:
                            action_results.append(f"Folder {action['parameters']['folder_path']} could not be created.")
                    elif action["name"] == "delete_file":
                        # Datei löschen
                        #file.delete_file(home_dir, action["parameters"]["file_path"])
                        pass
                    elif action["name"] == "delete_folder":
                        # Ordner löschen
                        #file.delete_folder(home_dir, action["parameters"]["folder_path"], action["parameters"].get("recursive", False))
                        pass
                    elif action["name"] == "move_file":
                        # Datei verschieben
                        file.move_file(home_dir, action["parameters"]["source_path"], action["parameters"]["target_path"])
                    elif action["name"] == "copy_file":
                        # Datei kopieren
                        #file.copy_file(home_dir, action["parameters"]["source_path"], action["parameters"]["target_path"])
                        pass
                    elif action["name"] == "search_files":
                        # Dateien suchen
                        #files = file.search_files(home_dir, action["parameters"]["search_string"])
                        #current_reiceiver_agent.update_data({"search_results": files})
                        #todo
                        pass
                    elif action["name"] == "send_message":
                        # Nachricht an ein Teammitglied speichern. Sie wird bei der nächsten Iteration gesendet.
                        # Es kann nur eine Nachricht auf einmal gespeichert werden
                        if data["next_receiver"]:
                            action_results.append("Only one message can be saved at a time.")
                        else:
                            data["next_sender"] = data["current_receiver"]
                            data["next_receiver"] = action["parameters"]["recipient"]
                            data["next_message"] = action["content"]
                            action_results.append(f"Message to {data['next_receiver']} saved for sending.")
                    elif action["name"] == "ask_question":
                        # Frage an den Agenten speichern, die beim nächsten Schleichdurchlauf gestellt wird
                        data["computer_question"] = action["content"]
                    elif action["name"] == "print_file":
                        # Dateiinhalt anzeigen
                        #todo
                        pass
                    elif action["name"] == "insert_in_file":
                        # Inhalt in Datei einfügen
                        #file.insert_in_file(home_dir, action["parameters"]["file_path"], action["parameters"]["line"], action["content"])
                        pass
                    elif action["name"] == "replace_in_file":
                        # Inhalt in Datei ersetzen
                        #file.replace_in_file(home_dir, action["parameters"]["file_path"], action["parameters"]["start_line"], action["parameters"]["end_line"], action["content"])
                        pass
                    elif action["name"] == "finish":
                        # Computer-KI hat die Aufgabe beendet
                        ai_finished = True
                        # Computer-KI-Meldung nachher an KI-Agenten senden
                        data["computer_message"] = action["content"]
                
                # Wenn nicht beendet, nächste Iteration vorbereiten
                if not ai_finished:
                    if (data["computer_question"]):
                        # Frage an den Agenten stellen
                        data["received_message"] = "" # Damit die Nachricht nicht doppelt angezeigt wird
                        prompt_data = data.copy()
                        response = current_reiceiver_agent.next_step(prompt_data)
                        data["answer_to_question"] = response
                        action_results.append(f"Answer to question received.")
                    else:
                        # Nächsten Prompt für die KI bauen
                        prompt_data = data
                        prompt_data["action_results"] = action_results
                        prompt = self._build_next_prompt(prompt_data)
                    iterations += 1
                else:
                    break
                
                if config.DEBUG:
                    input(f"The computer agent has completed an iteration while processing a message from {data['current_receiver']}. Press Enter to continue.")

            # für Debugging nach jeder Iteration nachfragen
            if config.DEBUG:
                input(f"Der Agent Computer hat eine Iteration beendet und wird gleich eine Nachricht an {data['next_receiver']} senden. Drücke Enter, um fortzufahren.")
            iterations += 1


    def _send_message_to_agent(self, sender, receiver, message):
        """
        Sendet eine Nachricht an einen Agenten.
        """
        pass

    def _parse_ai_response(self, response):
        """
        Parst die Antwort der KI in vordefinierte Felder.
        Jedes Feld ist so formattiert:
        ```
        # Action: <Name der Aktion>
        ## Parameters
        - <Paramter1>: <Wert1>
        - <Paramter2>: <Wert2>
        ## Content (optional)
        <Inhalt>
        ```
        """

        results = []

        # Antwort in Zeilen aufteilen
        lines = response.split("\n")

        # Inhalt der Antwort parsen mit Zustandsmaschine
        state = "searching codeblock"
        current_line = 0
        actionName = ""
        actionPars = {}
        actionContent = ""
        while current_line < len(lines):
            line = lines[current_line]
            if state == "searching codeblock":
                if line.startswith("```"):
                    state = "expecting action"
                    actionName = ""
                    actionPars = {}
                    actionContent = ""
            elif state == "expecting action":
                if line.startswith("# action: "):
                    actionName = line.split(": ")[1].strip()
                    state = "expecting parameters"
                else:
                    # Keine Aktion gefunden, weiter suchen
                    state = "searching codeblock"
            elif state == "expecting parameters":
                if line.startswith("## parameters"):
                    state = "parsing parameters"
                else:
                    # Keine Parameter gefunden, weiter suchen
                    state = "searching codeblock"
            elif state == "parsing parameters":
                if line.startswith("```"):
                    state = "searching codeblock"
                if line.startswith("## content"):
                    state = "parsing content"
                else:
                    parts = line.split(": ")
                    if len(parts) == 2:
                        actionPars[parts[0].strip()] = parts[1].strip()
            elif state == "parsing content":
                if line.startswith("```"):
                    state = "searching codeblock"
                else:
                    actionContent += line + "\n"
        
            if state == "searching codeblock" and actionName and actionPars:
                results.append({"name": actionName, "parameters": actionPars, "content": actionContent})

            current_line += 1

        return results
    
    
    