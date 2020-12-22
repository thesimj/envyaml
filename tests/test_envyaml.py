from __future__ import absolute_import

import os

import pytest

from envyaml import EnvYAML

# set os env
os.environ["TEST_ENV"] = "test-env"


def test_it_should_return_default_value():
    env = EnvYAML(
        yaml_file="tests/env.default.yaml", env_file="tests/test.env", strict=True
    )

    assert env["simple_d"] is None
    assert env["simple_e"] == ""
    assert env["config.complex"] == "xxxXyyy"
    assert env["config.with_default"] == "DEFAULT"


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
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

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

    env = EnvYAML("tests/env.empty.yaml")

    assert env["ENV_VAR"] == "test-env-var"

    del os.environ["ENV_VAR"]


def test_it_should_fail_when_access_environment_variables():
    os.environ["ENV_VAR"] = "test-env-var"

    env = EnvYAML("tests/env.empty.yaml", include_environment=False)

    with pytest.raises(KeyError):
        assert env["ENV_VAR"] == "test-env-var"

    del os.environ["ENV_VAR"]


def test_it_should_access_environ():
    os.environ["ENV_VAR"] = "test-env-var"

    env = EnvYAML("tests/env.empty.yaml")

    assert env.environ() == os.environ
    assert env.environ()["ENV_VAR"] == os.environ["ENV_VAR"]

    del os.environ["ENV_VAR"]


def test_it_should_get_default_values():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert env.get("empty.novalues", "default") is None
    assert env.get("empty.noenvvalue", "env-value") == ""  # value actually set to ""

    assert env["empty.noenvvalue"] == ""


def test_it_should_raise_key_error_when_no_values():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    with pytest.raises(KeyError):
        assert env["empty.no-value-at-all"]


def test_it_should_read_default_file():
    env = EnvYAML()

    # access by item name
    assert env["one.two.three.value"] == "one-two-three-value"
    # access list item
    assert env["list_test"][0] == "one"
    # access list item (array)
    assert env["list_test.0"] == "one"

    assert isinstance(env["keys"], dict) and len(env["keys"]) == 2


def test_it_should_populate_env_variable():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert env["config.test_env"] == os.environ["TEST_ENV"]


def test_it_should_return_dict_on_export():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert isinstance(env.export(), dict) and len(env.export()) >= 4


def test_it_should_convert_config_to_dict():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert isinstance(dict(env["test"]), dict)


def test_it_should_access_all_keys_in_config():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert len(env.keys()) > 10


def test_it_should_access_keys_and_lists():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

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

    del os.environ["ENV_YAML_FILE"]
    del os.environ["ENV_FILE"]


def test_it_should_raise_exception_when_file_not_found():
    with pytest.raises(IOError):
        EnvYAML("tests/env.notfound.yaml")


def test_it_should_use_default_value():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert env.get("not.exist.key") is None
    assert env.get("not.exist.key", "default") == "default"
    assert env.get("config.test") == 100


def test_it_should_get_lists_values_by_number():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

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
    if "ENV_YAML_FILE" in os.environ:
        del os.environ["ENV_YAML_FILE"]

    if "ENV_FILE" in os.environ:
        del os.environ["ENV_FILE"]

    env = EnvYAML()

    assert isinstance(env, EnvYAML)


def test_it_should_not_fail_when_try_load_default_empty_yaml_file():
    env = EnvYAML("tests/env.empty.yaml")

    assert isinstance(env, EnvYAML)


def test_it_should_not_fail_when_try_load_default_empty_dotenv_file():
    env = EnvYAML(env_file="tests/test.empty.env")

    assert isinstance(env, EnvYAML)


def test_it_should_be_valid_in_check():
    env = EnvYAML(env_file="tests/env.test.yaml")

    if "test.one" in env:
        assert env["test.one"] == 123

    assert "test.not_exists" not in env


def test_it_should_proper_handle_dollar_sign_with_number():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert (
        env["sql"]
        == 'SELECT * FROM "users" WHERE "user" = $1 AND "login" = $2 AND "pwd" = $3'
    )


def test_it_should_proper_complex_variable():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    assert env["complex"] == "xxxXyyy"


def test_it_should_proper_complex_variable_2():
    # initial setup
    os.environ["PROJECT_NAME"] = "x"
    os.environ["PROJECT_ID"] = "x"
    os.environ["BAR"] = "BAR"
    os.environ["PASSWORD"] = "x"
    os.environ["USERNAME"] = "x"

    env = EnvYAML("tests/env.test.yaml")

    assert env["complex"] == "xxxBARyyy"
    assert env["code.ffmpeg"] == "ffmpeg -an -c:v libx264 -preset veryfast"

    # delete
    del os.environ["PROJECT_NAME"]
    del os.environ["PROJECT_ID"]
    del os.environ["BAR"]
    del os.environ["PASSWORD"]
    del os.environ["USERNAME"]


def test_it_should_be_read_if_strict_disabled():
    env = EnvYAML("tests/env.ignored.yaml", strict=False)

    assert env["env_file.config"] == "$ENV_CONFIG_VERSION"
    assert env["env_file.project.pwd"] == "password"
    assert env["extra_a"] == "$DEFAULT_X"


def test_it_should_return_proper_formatted_string():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")
    assert env.format("format.test_a", key_1=1, key_2=2) == "1.2"


def test_it_should_raise_exception_in_strict_mode():
    with pytest.raises(ValueError):
        EnvYAML("tests/env.ignored.yaml")


def test_it_should_parser_environment_inside_array_and_object():
    env = EnvYAML("tests/env.test.yaml", env_file="tests/test.env")

    # assert array
    assert env['var_in_array.to.0'] == 'env-username'
