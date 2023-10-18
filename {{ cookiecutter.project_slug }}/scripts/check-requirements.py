import os

import pkg_resources
import logging
from pathlib import Path

LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)

log_dir = ('{{ cookiecutter.project_slug }}/logs') # buscar forma correta no coockiecutter
os.makedirs(log_dir, exist_ok=True) # provavelmente desnecessário no CC

file_handler = logging.FileHandler( Path(log_dir, 'logs.log'))
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
logger.addHandler(file_handler)

logger_functions = dict(
    on_missing=logger.warning,
    on_wrong_version=logger.warning
)

def check_packages(requirements: str = 'requirements.txt', logger_options: dict = logger_functions ):
    missing_packages = []
    wrong_version_packages = []

    packages = read_requirements_txt(requirements)

    for package_name, expected_version in packages.items():
        try:
            installed_version = pkg_resources.get_distribution(package_name).version

            if expected_version:
                if pkg_resources.parse_version(installed_version) != pkg_resources.parse_version(expected_version):
                    wrong_version_packages.append((package_name, installed_version, expected_version))

        except pkg_resources.DistributionNotFound:
            missing_packages.append(package_name)

    logger.info("Checking installed packages before continuing...")

    if missing_packages:
        message = f"Required packages are missing: {', '.join(missing_packages)}"

        if logger_functions['on_missing'] == logger.error:
            logger_functions['on_missing'](message)
            raise Exception(f"Required packages are missing. Please check your installed packages.")
        else:
            logger_functions['on_missing'](message)

    if wrong_version_packages:
        message = [f"{pac} (Installed: {ins}, Expected: {exp})" for pac, ins, exp in wrong_version_packages]

        if logger_functions['on_wrong_version'] == logger.error:
            logger_functions['on_wrong_version'](f"Wrong versions of packages: {' '.join(message)}")
            raise Exception("Packages with wrong versions were found. Please check your installed packages.")
        else:
            logger_functions['on_wrong_version'](f"Packages with the wrong version were detected: {' '.join(message)}")


    if not missing_packages and not wrong_version_packages:
        logger.info("All packages are installed and have the correct version.")

    return missing_packages, wrong_version_packages # retornar mesmo que não seja usado, estilo pandas?

def read_requirements_txt(file_path):
    packages_to_check = {}

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        for line in lines:
            if line.strip() and not line.startswith('#'):
                parts = line.split('==')

                if len(parts) == 2:
                    package_name, package_version = parts
                    packages_to_check[package_name] = package_version

                elif len(parts) == 1:
                    packages_to_check[parts[0]] = None

    return packages_to_check


