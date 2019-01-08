from __future__ import absolute_import

import os

import pytest

from envyaml import EnvYAML

# set os env
os.environ['TEST_ENV'] = 'test-env'


def test_it_should_read_env_file():
    config = EnvYAML('tests/env.test.yaml', env_file='tests/test.env')

    assert config.env_file.project.name == 'project-x-42'
    assert config.USERNAME == 'env-username'
    assert config.PASSWORD == 'env-password-with-escape'
    assert config.PASSWORD_WE == 'env-password-without-escape'
    assert config.EMPTY == ''

    # Test wrong names, should be not found and raise KeyErro
    with pytest.raises(KeyError):
        assert config['01sre']

    with pytest.raises(KeyError):
        assert config['!dtdrthkj']

    with pytest.raises(KeyError):
        assert config['$WRONG_NAME']

    # Config from comment
    with pytest.raises(KeyError):
        assert config['comments']


def test_it_should_read_custom_file():
    config = EnvYAML('tests/env.test.yaml')

    # access by property name
    assert config.one.two.three.value == "one-two-three-value"
    # access by item name
    assert config['one.two.three.value'] == "one-two-three-value"
    # access list item
    assert config.list_test[0] == 'one'
    # access list item (array)
    assert config['list_test.0'] == 'one'


def test_it_should_populate_env_variable():
    config = EnvYAML('tests/env.test.yaml')

    assert config.config.test_env == os.environ['TEST_ENV']


def test_it_should_return_dict_on_export():
    config = EnvYAML('tests/env.test.yaml')

    assert isinstance(config.export(), dict) and len(config.export()) >= 4


def test_is_should_read_config_from_env_variable():
    # Set env file
    os.environ['ENV_YAML_FILE'] = 'tests/env.test.yaml'
    os.environ['ENV_FILE'] = 'tests/test.env'

    config = EnvYAML()

    assert config.env_file.project.name == 'project-x-42'
    assert isinstance(config.export(), dict) and len(config.export()) >= 4


def test_is_should_raise_exception_when_file_not_found():
    with pytest.raises(IOError):
        EnvYAML('tests/env.notfound.yaml')


def test_is_should_use_default_value():
    config = EnvYAML('tests/env.test.yaml')

    assert config.get('not.exist.key') is None
    assert config.get('not.exist.key', 'default') == 'default'
    assert config.get('config.test') == 100


def test_is_should_get_lists_values_by_number():
    config = EnvYAML('tests/env.test.yaml')

    assert config.list_test[0] == 'one'
    assert config.list_test[1] == 'two'
    assert config.list_test[2] == 'tree'

    assert config.get('list_test.0') == 'one'
    assert config.get('list_test.1') == 'two'
    assert config.get('list_test.2') == 'tree'

    assert config['list_test.0'] == 'one'
    assert config['list_test.1'] == 'two'
    assert config['list_test.2'] == 'tree'
