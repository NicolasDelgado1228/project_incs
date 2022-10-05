#   -*- coding: utf-8 -*-
#   -*- copyright -*-


#   Dependencies
import subprocess
from os import environ as env
from os import walk, rename
from pybuilder.core import use_plugin, init, task

# Pybuilder plugins
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.install_dependencies")

# Package information
name = "seed"
version = "0.0.1"

# Build tasks
default_task = ["analyze", "isort", "unittest", "clean"]


# Environment
ENVIRONMENT = env.get("ENVIRONMENT_NAME")


@init
def set_properties(project):
    if not ENVIRONMENT:
        pass
    else:
        project.depends_on_requirements("requirements.txt")

    project.set_property("flake8_verbose_output", True)
    project.set_property("flake8_exclude_patterns", "__init__.py")
    project.set_property("flake8_ignore", "E711, W503")
    project.set_property("flake8_include_test_sources", True)
    project.set_property("flake8_break_build", True)


@task
def unittest(project, logger, reactor):
    logger.info("! Running unit test...\n")

    cmd = "coverage run --source=./src/main/python --omit='*/__init__.py,*/secrets_manager.py'  -m unittest discover -s ./src/unittest/python -p '*_tests.py'"
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as err:
        raise Exception(
            "Unittest failure - Please Check your unittests and try build the project again"
        )

    print("\n")

    command = ["coverage", "report", "-m"]

    subprocess.run(command)
    print("\n")


@task
def isort(project, logger):
    logger.info("! Running isort")

    command = ["isort", "./src", "--profile", "black"]

    subprocess.run(command)
    print("\n")


@task
def deploy(project, logger):
    logger.info("! Deploy started")

    deploy_config = json.load(open("deploy_config.json"))

    # Extract functions to deploy
    # deployable_functions = ["web_create_message", "instagram_messages_webhook"]
    deployable_functions = env.get("DEPLOY_SERVICES", "").split(",")

    for function in deploy_config["functions"]:
        if deployable_functions[0] == "all":
            original_name = f"{function['source_path']}/{function['source_file']}.py"
            temp_name = f"{function['source_path']}/main.py"
            rename(original_name, temp_name)

            command = f"gcloud functions deploy {function['name']} --entry-point {function['entry_point']} --source {function['source_path']} --runtime {function['runtime']} --trigger-{function['trigger']} {function['flags']} --set-env-vars GCP_PROJECT={env.get('GCP_PROJECT')}"
            subprocess.run(command.split())

            rename(temp_name, original_name)

        elif function["name"] in deployable_functions:
            original_name = f"{function['source_path']}/{function['source_file']}.py"
            temp_name = f"{function['source_path']}/main.py"
            rename(original_name, temp_name)

            command = f"gcloud functions deploy {function['name']} --entry-point {function['entry_point']} --source {function['source_path']} --runtime {function['runtime']} --trigger-{function['trigger']} {function['flags']} --set-env-vars GCP_PROJECT={env.get('GCP_PROJECT')}"
            subprocess.run(command.split())

            rename(temp_name, original_name)

    print("\n")
