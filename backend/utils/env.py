import os


def get_env(name: str) -> str:
    """
    Get environment variable and raise error if not found

    Args:
        name: Environment variable name

    Returns:
        str: Environment variable value

    Raises:
        Error: If environment variable is not set
    """
    value = os.getenv(name)
    if value is None or value == '':
        raise ValueError(
            f'Environment variable {name} is not set or is empty. '
            f'Please set it in your .env file.'
        )
    return value
