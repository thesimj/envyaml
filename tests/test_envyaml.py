from __future__ import absolute_import

import os

import pytest

from envyaml.envyaml import EnvYAML

# set os env
os.environ['TEST_ENV'] = 'test-env'


def test_it_should_read_env_file():
    config = EnvYAML('tests/env.test.yaml', env_file='tests/test.env')

    assert config.env_file__project__name == 'project-x-42'


def test_it_should_read_custom_file():
    config = EnvYAML('tests/env.test.yaml')

    # access by property name
    assert config.one__two__three__value == "one-two-three-value"
    # access by item name
    assert config['one__two__three__value'] == "one-two-three-value"
    # access list item
    assert config.list_test__0 == 'one'
    # access list item (array)
    assert config['list_test__0'] == 'one'


def test_it_should_populate_env_variable():
    config = EnvYAML('tests/env.test.yaml')

    assert config.config__test_env == os.environ['TEST_ENV']


def test_it_should_work_with_custom_separator():
    config = EnvYAML('tests/env.test.yaml', separator=':')

    assert config['one:two:three:value'] == "one-two-three-value"


def test_it_should_return_dict_on_export():
    config = EnvYAML('tests/env.test.yaml', separator=':')

    assert isinstance(config.export(), dict) and len(config.export()) >= 4


def test_is_should_read_config_from_env_variable():
    # Set env file
    os.environ['ENV_YAML_FILE'] = 'tests/env.test.yaml'
    os.environ['ENV_FILE'] = 'tests/test.env'

    config = EnvYAML()

    assert config.env_file__project__name == 'project-x-42'
    assert isinstance(config.export(), dict) and len(config.export()) >= 4


def test_is_should_raise_exception_when_file_not_found():
    with pytest.raises(FileNotFoundError):
        EnvYAML('tests/env.notfound.yaml')


def test_is_should_use_default_value():
    config = EnvYAML('tests/env.test.yaml')

    assert config.get('not__exist__key') is None
    assert config.get('not__exist__key', 'default') == 'default'
    assert config.get('config__test') == 100


def test_is_should_get_lists_values_by_number():
    config = EnvYAML('tests/env.test.yaml')

    assert config.list_test__0 == 'one'
    assert config.list_test__1 == 'two'
    assert config.list_test__2 == 'tree'
