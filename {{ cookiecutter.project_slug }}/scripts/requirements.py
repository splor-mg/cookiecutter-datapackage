import pkg_resources
import logging

LOG_FORMAT = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)

logger_options=dict(
                on_missing=logger.error,
                on_wrong_version=logger.error
            )

def check_requirements(
        requirements: str = 'requirements.in',
        logger_functions=None
):
    if logger_functions is None:
        logger_functions = logger_options
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

        if logger_functions["on_missing"] == logger.error:
            raise Exception(message)
            #raise Exception(f"Required packages are missing. Please check your installed packages.")
        else:
            logger_functions["on_missing"](message)

    if wrong_version_packages:
        message = [f"{pac} (Installed: {ins}, Expected: {exp})" for pac, ins, exp in wrong_version_packages]

        if logger_functions["on_wrong_version"] == logger.error:
            raise Exception(f"Required packages with wrong versions: {', '.join(message)}")
            #raise Exception("Packages with wrong versions were found. Please check your installed packages.")
        else:
            logger_functions["on_wrong_version"](f"Required packages with wrong versions: {' '.join(message)}")

    if not missing_packages and not wrong_version_packages:
        logger.info("All packages are installed and have the correct version.")


def read_requirements_txt(file_path):
    packages_to_check = {}

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        for line in lines:
            if not line.strip().startswith('#'):
                if line.startswith('git+https://github.com/'):
                    # trata req começando com git+ branch será a versão
                    parts = line.split('.git@')
                    if len(parts) == 2:
                        package_name = parts[0].split('/')[-1]
                        # somente branchs que tem nome de versão, conforme convenção de projeto
                        package_version = parts[1].replace('v', '') if parts[1].startswith('v') else None
                        packages_to_check[package_name] = package_version


                else:
                    parts = line.split('==')

                    if len(parts) == 2:
                        package_name, package_version = parts
                        packages_to_check[package_name] = package_version

                    elif len(parts) == 1:
                        packages_to_check[parts[0]] = None

    return packages_to_check