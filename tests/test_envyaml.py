from __future__ import absolute_import

import os

from envyaml.envyaml import EnvYaml

# set os env
os.environ['TEST_ENV'] = 'test-env'


def test_it_should_read_custom_file():
    config = EnvYaml('tests/env.test.yaml')

    # access by property name
    assert config.one__two__three__value == "one-two-three-value"
    # access by item name
    assert config['one__two__three__value'] == "one-two-three-value"
    # access list item
    assert config.list_test__0 == 'one'
    # access list item (array)
    assert config['list_test__0'] == 'one'


def test_it_should_populate_env_variable():
    config = EnvYaml('tests/env.test.yaml')

    assert config.config__test_env == os.environ['TEST_ENV']


def test_it_should_work_with_custom_separator():
    config = EnvYaml('tests/env.test.yaml', separator=':')

    assert config['one:two:three:value'] == "one-two-three-value"


def test_it_should_return_dict_on_export():
    config = EnvYaml('tests/env.test.yaml', separator=':')

    assert isinstance(config.export(), dict) and len(config.export()) >= 4
