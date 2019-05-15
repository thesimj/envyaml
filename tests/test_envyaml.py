from __future__ import absolute_import

import os

import pytest

from envyaml import EnvYAML

# set os env
os.environ["TEST_ENV"] = "test-env"


def test_it_should_read_env_file():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert env["env_file.project.name"] == "project-x-42"
    assert env["USERNAME"] == "env-username"
    assert env["PASSWORD"] == "env-password-with-escape"
    assert env["PASSWORD_WE"] == "env-password-without-escape"
    assert env["EMPTY"] == ""

    # Test wrong names, should be not found and raise KeyErro
    with pytest.raises(KeyError):
        assert env["01sre"]

    with pytest.raises(KeyError):
        assert env["!dtdrthkj"]

    with pytest.raises(KeyError):
        assert env["$WRONG_NAME"]

    # Config from comment
    with pytest.raises(KeyError):
        assert env["comments"]


def test_it_should_read_custom_file():
    env = EnvYAML("tests/env.test.yaml")

    # access by property name
    assert env["one.two.three.value"] == "one-two-three-value"
    # access by item name
    assert env["one.two.three.value"] == "one-two-three-value"
    # access list item
    assert env["list_test"][0] == "one"
    # access list item (array)
    assert env["list_test.0"] == "one"

    assert isinstance(env["keys"], dict) and len(env["keys"]) == 2


def test_it_should_access_environment_variables():
    os.environ["ENV_VAR"] = "test-env-var"

    env = EnvYAML()

    assert env["ENV_VAR"] == "test-env-var"


def test_it_should_fail_when_access_environment_variables():
    os.environ["ENV_VAR"] = "test-env-var"

    env = EnvYAML(include_environment=False)

    with pytest.raises(KeyError):
        assert env["ENV_VAR"] == "test-env-var"


def test_it_should_access_environ():
    os.environ["ENV_VAR"] = "test-env-var"

    env = EnvYAML()

    assert env.environ() == os.environ
    assert env.environ()["ENV_VAR"] == os.environ["ENV_VAR"]


def test_it_should_read_default_file():
    env = EnvYAML()

    # access by property name
    assert env["one.two.three.value"] == "one-two-three-value"
    # access by item name
    assert env["one.two.three.value"] == "one-two-three-value"
    # access list item
    assert env["list_test"][0] == "one"
    # access list item (array)
    assert env["list_test.0"] == "one"

    assert isinstance(env["keys"], dict) and len(env["keys"]) == 2


def test_it_should_populate_env_variable():
    env = EnvYAML("tests/env.test.yaml")

    assert env["config.test_env"] == os.environ["TEST_ENV"]


def test_it_should_return_dict_on_export():
    env = EnvYAML("tests/env.test.yaml")

    assert isinstance(env.export(), dict) and len(env.export()) >= 4


def test_it_should_convert_config_to_dict():
    env = EnvYAML("tests/env.test.yaml")

    assert isinstance(dict(env["test"]), dict)


def test_it_should_access_all_keys_in_config():
    env = EnvYAML("tests/env.test.yaml")

    assert len(env.keys()) > 10


def test_it_should_access_keys_and_lists():
    env = EnvYAML("tests/env.test.yaml")

    assert isinstance(env["keys_and_lists"], dict)
    assert isinstance(env["keys_and_lists.one"], list)
    assert isinstance(env["keys_and_lists.two"], list)

    assert env["keys_and_lists.one.0"] == "one"
    assert env["keys_and_lists.two.1.super.one"] == "one"


def test_it_should_read_config_from_env_variable():
    # Set env file
    os.environ["ENV_YAML_FILE"] = "tests/env.test.yaml"
    os.environ["ENV_FILE"] = "tests/test.env"

    env = EnvYAML()

    assert env["env_file.project.name"] == "project-x-42"
    assert isinstance(env.export(), dict) and len(env.export()) >= 4


def test_it_should_raise_exception_when_file_not_found():
    with pytest.raises(IOError):
        EnvYAML("tests/env.notfound.yaml")


def test_it_should_use_default_value():
    env = EnvYAML("tests/env.test.yaml")

    assert env.get("not.exist.key") is None
    assert env.get("not.exist.key", "default") == "default"
    assert env.get("config.test") == 100


def test_it_should_get_lists_values_by_number():
    env = EnvYAML("tests/env.test.yaml")

    assert env["list_test"][0] == "one"
    assert env["list_test"][1] == "two"
    assert env["list_test"][2] == "tree"

    assert env.get("list_test.0") == "one"
    assert env.get("list_test.1") == "two"
    assert env.get("list_test.2") == "tree"

    assert env["list_test.0"] == "one"
    assert env["list_test.1"] == "two"
    assert env["list_test.2"] == "tree"


def test_it_should_not_fail_when_try_load_non_exist_default_file():
    del os.environ["ENV_YAML_FILE"]
    del os.environ["ENV_FILE"]

    env = EnvYAML()

    assert isinstance(env, EnvYAML)


def test_it_should_not_fail_when_try_load_default_empty_yaml_file():
    env = EnvYAML("tests/env.empty.yaml")

    assert isinstance(env, EnvYAML)


def test_it_should_not_fail_when_try_load_default_empty_dotenv_file():
    env = EnvYAML(env_file="tests/test.empty.env")

    assert isinstance(env, EnvYAML)
