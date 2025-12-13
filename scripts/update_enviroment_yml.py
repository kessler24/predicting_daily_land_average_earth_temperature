"""Library of functions used to append package versions in environment.yml files 

   Example command line usage: 
   python scripts/update_enviroment_yml.py --root_dir="." --env_name="ai_env"
   
"""

import re
import subprocess
from pathlib import Path
import yaml
import click


def process_dependency(dep, installed_packages):
    """
    Processes a single dependency to update its version based on installed packages.

    Parameters:
        dep (str): The dependency string (e.g., "pandas=2.2.3" or "numpy").
        installed_packages (dict): A dictionary of installed package names and versions. from "conda list"

    Returns:
        str: The updated dependency string with the version if found, or the original dependency.
    """
    # Check if the dependency has no version added
    if "=" not in dep:
        pkg_name = dep.strip()
        if pkg_name in installed_packages:  # Update dependency if in the conda list
            return f"{pkg_name}={installed_packages[pkg_name]}"
        else:
            return dep  # keep as original if not installed
    else:
        pkg_name = re.split(r"=|>=|<=", dep)[0]
        if pkg_name in installed_packages:
            # still re-write the version even if there is a version installed already
            return f"{pkg_name}={installed_packages[pkg_name]}"
        else:
            return dep  # keep as original if not installed


def update_environment_yml(env_name, yml_file="../environment.yml"):
    """
    Updates the `environment.yml` file with the correct package versions
    from the conda environment (env_name) using "conda list".

    Parameters:
        env_name (str): The name of the conda environment
        yml_file (str): The path to the `environment.yml` file to update.

    Returns:
        None
    """
    with open(yml_file, "r") as f:
        env_data = yaml.safe_load(f)

    # Get the list of installed packages & versions from `conda list`
    result = subprocess.run(
        ["conda", "list", "--name", env_name], stdout=subprocess.PIPE, text=True
    )
    installed_packages = {
        line.split()[0]: line.split()[1]
        for line in result.stdout.splitlines()
        if not line.startswith("#") and line
    }

    # Update the versions in the environment.yml
    updated_dependencies = []
    for dep in env_data.get("dependencies", []):
        if isinstance(dep, dict) and "pip" in dep:  # Process the 'pip' dictionary
            updated_pip_dependencies = []
            for pip_dep in dep.get("pip", []):  # process every pip dependencies
                new_pip_dep = process_dependency(pip_dep, installed_packages)
                updated_pip_dependencies.append(new_pip_dep)
            new_dep = dep
            new_dep["pip"] = updated_pip_dependencies  # update pip dictionary
        else:  # if it's conda installed dependencies
            new_dep = process_dependency(dep, installed_packages)

        updated_dependencies.append(
            new_dep
        )  # attach updated dependency string (or pip dictionary)

    # Write the updated environment.yml back
    env_data["dependencies"] = updated_dependencies
    with open(yml_file, "w") as f:
        yaml.dump(env_data, f, sort_keys=False)

    print(f"Updated {yml_file} with versions from the {env_name} environment.")


@click.command()
@click.option(
    "--root_dir",
    default=".",
    type=str,
    help="Path to the root directory where the environment.yml is located. Default is your current directory `.`",
)
@click.option(
    "--env_name",
    default="climate_env",
    type=str,
    help="Name of your conda virtual environment. Default is `ai_env`",
)
def main(root_dir, env_name):
    """grab environment.yml, and add version numbers after each package"""

    # in case anyone just entered "" to indicate it's root directory
    if root_dir.strip() == "":
        root_dir = "."

    # using the functions
    yml_path = Path(root_dir) / "environment.yml"
    update_environment_yml(env_name, yml_path)


if __name__ == "__main__":
    main()
