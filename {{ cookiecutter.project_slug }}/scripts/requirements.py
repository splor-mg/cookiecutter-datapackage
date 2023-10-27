import importlib.metadata as pkg_metadata
import logging

LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)



def check_requirements(
        requirements: str = 'requirements.in',
        stop_on_missing: bool = True,
        stop_on_wrong_version: bool = True,
):
    logger_functions = dict(
        on_missing=logger.error,
        on_wrong_version=logger.error
    )

    missing_packages = []
    wrong_version_packages = []

    packages = read_requirements_txt(requirements)

    for package_name, expected_version in packages.items():
        try:
            installed_version = pkg_metadata.version(package_name)

            if expected_version:
                if installed_version != expected_version:
                    wrong_version_packages.append((package_name, installed_version, expected_version))

        except pkg_metadata.PackageNotFoundError:
            missing_packages.append(package_name)


    if missing_packages:
        message = f"Required packages are missing: {', '.join(missing_packages)}"

        if stop_on_missing:
            raise Exception(message)
        else:
            logger_functions["on_missing"](message)

    if wrong_version_packages:
        message = [f"{pac} (Installed: {ins}, Expected: {exp})" for pac, ins, exp in wrong_version_packages]

        if stop_on_wrong_version:
            raise Exception(f"Required packages with wrong versions: {', '.join(message)}")

        else:
            logger_functions["on_wrong_version"](f"Required packages with wrong versions: {' '.join(message)}")

    if not missing_packages and not wrong_version_packages:
        logger.info("All packages are installed and have the correct version.")


def read_requirements_txt(file_path):
    packages_to_check = {}

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        for line in lines:
            packages_to_check.update(parse_requirement(line))

    return packages_to_check


def parse_requirement(req):
    if not req.strip().startswith('#'):
        if req.startswith('git+https://github.com/'):
            parts = req.split('.git@')
            if len(parts) == 2:
                package_name = parts[0].split('/')[-1]
                package_version = parts[1].replace('v', '') if parts[1].startswith('v') else None
                return {package_name: package_version}

        else:
            parts = req.split('==')

            if len(parts) == 2:
                package_name, package_version = parts
                return {package_name: package_version}

            elif len(parts) == 1:
                return {parts[0]: None}

if __name__ == '__main__':
    check_requirements()

