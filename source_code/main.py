# main.py

import datetime
import logging
import os
import config
import ai.user as user
import ai.ai_computer as ai_computer
import ai.ai_project_manager as ai_project_manager
import ai.ai_developer as ai_developer
import ai.ai_requirements_engineer as ai_requirements_engineer
import ai.ai_test_engineer as ai_test_engineer
import ai.ai_architect as ai_architect

# Configure logging
os.makedirs("log", exist_ok=True)
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(filename=f'log/ai_interactions_{current_time}.log',
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')

def main():

    # Schritt des Projekts ausführen
    data = {
        "project_name": config.PROJECT_NAME
    }

    # Alle AI-Agenten durchgehen
    all_agent_classes = [ai_computer.AI_Computer, user.AI_User, ai_project_manager.AI_ProjectManager, ai_developer.AI_Developer, ai_requirements_engineer.AI_RequirementsEngineer, ai_test_engineer.AI_TestEngineer, ai_architect.AI_Architect]
    # Infos zu allen Agenten sammeln und einen String erstellen, mit allen Rollenbeschreibungen
    roles_text = ""
    for agent in all_agent_classes:
        if not agent.skip_in_role_list:
            roles_text += agent.name + ", " + agent.role + ": " + agent.role_description + "\n"
    data["all_role_descriptions"] = roles_text
    # Alle Agenten initialisieren
    all_agents = []
    for agent in all_agent_classes:
        all_agents.append(agent(data))
    data["all_agents_by_name"] = {}
    for agent in all_agents:
        data["all_agents_by_name"][agent.name] = agent

    # Benutzerinteraktion starten
    computer = data["all_agents_by_name"]["Computer"]
    result = computer.start(data)
    print(result)

if __name__ == "__main__":
    main()

