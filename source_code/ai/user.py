"""
Klasse user abgeleitet von AI_Agent. Sie repräsentiert den Benutzer des Systems und implementiert die Interaktion mit dem Benutzer.
"""

import config
from ai.ai_base import AI_Agent
from prompts.user import UserPrompts



class AI_User(AI_Agent):
    name = config.USER_NAME
    role = "development manager"
    role_ID = "user"
    prompts = UserPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        # Basisklasse Funktion nicht verwenden
        self.data = data
        self.home_dir = None


    def next_step(self, data):
        """
        Führt einen Schritt aus.
        """

        # Allgemeine Daten für die Prompts
        prompt_data = self.data
        # data mit den spezifischen Daten überschreiben
        prompt_data.update(data)

        # Text, der dem Benutzer angezeigt wird, bauen
        prompt = self._build_next_prompt(prompt_data)

        # Nachricht ausgeben und Eingabe des Benutzers einlesen
        response = input(prompt)
        
        # Text, der an den Computer gesendet wird, bauen
        data["response"] = response
        computer_prompt = self._build_computer_prompt(data)

        # Nachricht an den Computer zurückgeben
        return computer_prompt
        

    def _build_computer_prompt(self, data):
        """
        Baut den Prompt für den Computer.
        """
       
        prompt = self.prompts.computer_prompt
        
        # fülle Platzhalter im Prompt
        prompt = self._fill_prompt_template(prompt, data)

        return prompt
