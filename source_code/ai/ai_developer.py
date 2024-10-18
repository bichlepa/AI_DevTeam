"""
Klasse AI_Developer abgeleitet von AI_Agent.
"""

import ai_interface
import config
import file
import os
from ai.ai_base import AI_Agent
from prompts.developer import DeveloperPrompts



class AI_Developer(AI_Agent):
    name = "Louis"
    role = "developer"
    role_ID = "developer"
    prompts = DeveloperPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        super().__init__(data)
