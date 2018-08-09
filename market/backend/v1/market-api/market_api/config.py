import os


class LoginConfigException(Exception):
    pass


class BaseConfig:
    """Base configuration."""
    DEBUG = False
    SECRET_KEY = os.getenv('LOGIN_API_SECRET')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True


def get_config_location():
    environment_configs = dict(
        dev='market_api.config.DevelopmentConfig',
        # test=TestConfig,
        # prod=ProdConfig
    )

    try:
        environment_name = os.environ['SELENE_ENVIRONMENT']
    except KeyError:
        raise LoginConfigException('the SELENE_ENVIRONMENT variable is not set')

    try:
        configs_location = environment_configs[environment_name]
    except KeyError:
        raise LoginConfigException(
            'no configuration defined for the "{}" environment'.format(environment_name)
        )

    return configs_location