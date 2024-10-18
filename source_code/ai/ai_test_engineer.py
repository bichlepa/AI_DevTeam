"""
Klasse AI_TestEngineer abgeleitet von AI_Agent.
"""

import ai_interface
import config
import file
import os
from ai.ai_base import AI_Agent
from prompts.test_engineer import TestEngineerPrompts



class AI_TestEngineer(AI_Agent):
    name = "Klaus"
    role = "test engineer"
    role_ID = "test_engineer"
    prompts = TestEngineerPrompts
    role_description = prompts.role_description
    skip_in_role_list = False

    def __init__(self, data):
        super().__init__(data)