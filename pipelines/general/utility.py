import yaml


def read_configuration(configuration_file_path):
    """
    This function reads the configuration from the given path (yaml file)

    Args:
        configuration_file_path ([str]): path to yaml configuration

    Returns:
        [dict]: yaml config. used in this pipeline script as a dict
    """
    with open(configuration_file_path) as file:
        configuration = yaml.full_load(file)
    return configuration




