# Project Overview: Auto Developer

## Project Objective
The Auto Developer software aims to automate almost the entire software development process using AI. In addition to a well-documented source code, it will also generate a comprehensive requirements specification, documentation, and test cases according to the V-model, while being able to handle large projects.

## Requirements
- The software will create a requirements definition based on user inputs.
- It will generate a project overview.
- It will create an architecture specification.
- It will derive module requirements from the requirements definition.
- It will provide specifications for the modules and their interfaces.
- It will generate source code for the modules.
- It will create test cases at all levels of the V-model.
- It will produce test plans.
- It will ensure traceability between artifacts.
- It will allow users to make changes at all levels.
- It will adjust other artifacts with every change made.
- Users will be able to select the desired AI (provider and model) for each step.
- The software will allow users to edit AI prompts without changing the source code.
- It will be operable via a user interface.
- It will be integratable into a CI/CD process.

## Quality Requirements
- The software must be able to handle large projects.
- It should be well-maintainable, with simple changes (like AI prompts) easily adaptable.
- The entire interaction with the AI must be traceable.

## User Stories
1. Users want to easily adjust configurations the first time they use the software.
2. Users want to submit any change requests to the artifacts, which the software will implement.
3. Users want to report bugs in the artifacts, enabling the software to fix them.
4. Users should be able to provide missing information if the AI encounters difficulties while processing their requests.
5. When a change request is clear, the software will automatically execute the changes.
6. Users want the option to stop the execution step by step, allowing them to review prompts and changes to the artifacts.
7. In case of an error, users should receive a detailed error report to rectify issues.
8. Users should be able to exit the software anytime, which should resume from the last point on the next start.

## Architecture
The KI will utilize various agents with designated roles for different tasks, ensuring a streamlined process for software development. The project manager coordinates tasks and defines which agent will address user input, leading to efficient management and execution of development processes.

## Components
The software will be written in Python, encompassing multiple modules that facilitate its various functionalities.
