import pkg_resources
import logging

LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)


logger_functions = dict(
    on_missing=logger.error,
    on_wrong_version=logger.warning
)




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

    return packages_to_check


def check_packages(packages, logger_options ):
    missing_packages = []
    wrong_version_packages = []

    for package_name, expected_version in packages.items():
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
            if pkg_resources.parse_version(installed_version) != pkg_resources.parse_version(expected_version):
                wrong_version_packages.append((package_name, installed_version, expected_version))
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package_name)

    logger.info("Checking installed packages before continuing...")

    if missing_packages:
        logger_functions['on_missing']("Missing packages:")
        for package in missing_packages:
            logger.info(package)

        if logger_functions['on_missing'] == logger.error:
            raise Exception("Wrong version packages were found. Aborting the program.")

    if wrong_version_packages:
        logger_functions['on_wrong_version']("Packages with the wrong version:")
        for package, installed_version, expected_version in wrong_version_packages:
            logger.info(f"{package} (Installed: {installed_version}, Expected: {expected_version})")

        if logger_functions['on_wrong_version'] == logger.error:
            raise Exception("Missing packages were found. Aborting the program.")

    if not missing_packages and not wrong_version:
        logger.info("All packages are installed in the correct version.")

    return missing_packages, wrong_version_packages


requirements = read_requirements_txt('requirements.txt')

missing, wrong_version = check_packages(requirements, logger_functions)

