# -*- coding: utf-8 -*-
# This file is part of EnvYaml project
# https://github.com/thesimj/envyaml
#
# MIT License
#
# Copyright (c) 2021 Mykola Bubelich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io
import os
import re

try:
    from yaml import safe_load
except ImportError:
    safe_load = None

# pattern to remove comments
RE_COMMENTS = re.compile(r"(^#.*\n)", re.MULTILINE | re.UNICODE | re.IGNORECASE)
# pattern to read .env file
RE_DOT_ENV = re.compile(
    r"^(?!\d+)(?P<name>[\w\-\.]+)\=[\"\']?(?P<value>(.*?))[\"\']?$",
    re.MULTILINE | re.UNICODE | re.IGNORECASE,
)

# pattern to extract env variables
RE_PATTERN = re.compile(
    r"(?P<pref>[\"\'])?"
    r"(\$(?:(?P<escaped>(\$|\d+))|"
    r"{(?P<braced>(.*?))(\|(?P<braced_default>.*?))?}|"
    r"(?P<named>[\w\-\.]+)(\|(?P<named_default>.*))?))"
    r"(?P<post>[\"\'])?",
    re.MULTILINE | re.UNICODE | re.IGNORECASE | re.VERBOSE,
)

__version__ = "1.9.210927"


class EnvYAML:
    __version__ = __version__

    ENVYAML_STRICT_DISABLE = "ENVYAML_STRICT_DISABLE"  # type: str
    DEFAULT_ENV_YAML_FILE = "env.yaml"  # type:str
    DEFAULT_ENV_FILE = ".env"  # type:str

    __env_file = None  # type:str
    __yaml_file = None  # type: str
    __cfg = None  # type: dict
    __strict = True  # type: bool

    def __init__(
        self,
        yaml_file=None,
        env_file=None,
        include_environment=True,
        strict=True,
        flatten=True,
        **kwargs
    ):
        """Create EnvYAML class instance and read content from environment and files if they exists

        :param str yaml_file: file path for config or env.yaml by default
        :param str env_file: file path for .env file or None by default
        :param bool include_environment: include environment variable, by default true
        :param bool strict: use strict mode and throw exception when have unset variable, by default true
        :param bool flatten: whether we should flatten config hierarchy or not
        :param dict kwargs: additional environment variables keys and values
        :return: new instance of EnvYAML
        """
        # raise exception module not found when no pyyaml installed
        if safe_load is None:
            raise ModuleNotFoundError(
                'EnvYAML require "pyyaml >= 5" module to work. '
                "Consider install this module into environment!"
            )

        # read environment
        self.__cfg = dict(os.environ) if include_environment else {}

        # set strict mode to false if "ENVYAML_STRICT_DISABLE" presents in env else use "strict" from function
        self.__strict = False if self.ENVYAML_STRICT_DISABLE in self.__cfg else strict

        # default file names
        self.__env_file = env_file
        self.__yaml_file = yaml_file

        # read .env file and update config
        self.__cfg.update(
            self.__read_env_file(
                self.__get_file_path(env_file, "ENV_FILE", self.DEFAULT_ENV_FILE),
                self.__strict,
            )
        )

        # fill cfg with kwargs
        self.__cfg.update(kwargs)

        # read yaml file and parse it
        yaml_config = self.__read_yaml_file(
            self.__get_file_path(
                yaml_file, "ENV_YAML_FILE", self.DEFAULT_ENV_YAML_FILE
            ),
            self.__cfg,
            self.__strict,
        )

        # update config
        if isinstance(yaml_config, list):
            self.__cfg.update({k: v for k, v in enumerate(yaml_config)})
        else:
            self.__cfg.update(yaml_config)

        # make config as flat dict with '.'
        if flatten:
            self.__cfg = self.__flat(self.__cfg)

    def get(self, key, default=None):
        """Get configuration variable with default value. If no `default` value set use None

        :param any key: name for the configuration key
        :param any default: default value if no key found
        :return: any
        """

        return self.__cfg.get(key, default)

    def export(self):
        """Export config

        :return: dict with config
        """
        return self.__cfg.copy()

    @staticmethod
    def environ():
        """Get os.environ mapping object

        :return: A mapping object representing the string environment
        """
        return os.environ

    @staticmethod
    def __read_env_file(file_path, strict):
        """read and parse env file

        :param str file_path: path to file
        :param bool strict: strict mode
        :return: dict
        """
        config = dict()
        defined = set()

        if file_path:
            with io.open(file_path, encoding="utf8") as f:
                content = f.read()  # type: str

            # iterate over findings
            for entry in RE_DOT_ENV.finditer(content):
                name = entry.group("name")
                value = entry.group("value")

                # check double definition
                if name in config:
                    defined.add(name)

                # set variable name and value
                config[name] = value

        # strict mode
        if strict and defined:
            raise ValueError(
                "Strict mode enabled, variables "
                + ", ".join(["$" + v for v in defined])
                + " defined several times!"
            )

        return config

    @staticmethod
    def __read_yaml_file(file_path, cfg, strict, separator="|"):
        """read and parse yaml file

        :param str file_path: path to file
        :param dict cfg: configuration variables (environ and .env)
        :param bool strict: strict mode
        :return: dict
        """

        # read and parse files
        with io.open(file_path, encoding="utf8") as f:
            content = f.read()  # type:str

        # remove all comments
        content = RE_COMMENTS.sub("", content)

        # not found variables
        not_found_variables = set()

        # changes dictionary
        replaces = dict()

        # iterate over findings
        for entry in RE_PATTERN.finditer(content):
            groups = entry.groupdict()  # type: dict

            # replace
            variable = None
            default = None
            replace = None

            if groups["named"]:
                variable = groups["named"]
                default = groups["named_default"]

            elif groups["braced"]:
                variable = groups["braced"]
                default = groups["braced_default"]

            elif groups["escaped"] and "$" in groups["escaped"]:
                content = content.replace("$" + groups["escaped"], groups["escaped"])

            if variable is not None:
                if variable in cfg:
                    replace = cfg[variable]
                elif variable not in cfg and default is not None:
                    replace = default
                else:
                    not_found_variables.add(variable)

            if replace is not None:
                # build match
                search = "${" if groups["braced"] else "$"
                search += variable
                search += separator + default if default is not None else ""
                search += "}" if groups["braced"] else ""

                # store findings
                replaces[search] = replace

        # strict mode
        if strict and not_found_variables:
            raise ValueError(
                "Strict mode enabled, variables "
                + ", ".join(["$" + v for v in not_found_variables])
                + " are not defined!"
            )

        # replace finding with there respective values
        for replace in sorted(replaces, reverse=True):
            content = content.replace(replace, replaces[replace])

        # load proper content
        yaml = safe_load(content)

        # if contains somethings
        if yaml and isinstance(yaml, (dict, list)):
            return yaml

        # by default return empty dict
        return {}

    @staticmethod
    def __get_file_path(file_path, env_name, default):
        """Construct file path

        :param str file_path: path to file
        :param str env_name: env name
        :param str default: default file path
        :return: return file path or None if file not exists
        """
        if file_path:
            return file_path

        elif os.environ.get(env_name):
            return os.environ.get(env_name)

        elif os.path.exists(default):
            return default

    @staticmethod
    def __flat_deep(prefix, config):
        """Flat siblings

        :param str prefix: prefix
        :param any config: configuration
        :return: dict
        """
        dest_ = {}

        elements = (
            enumerate(config)
            if (isinstance(config, list) or isinstance(config, tuple))
            else config.items()
        )  # type: (str, any)

        for key_, value_ in elements:
            key_ = prefix + "." + str(key_)

            if isinstance(value_, dict):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            elif isinstance(value_, list):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            else:
                dest_[key_] = value_

        return dest_

    @staticmethod
    def __flat(config):
        """Flat dictionaries in recursive way

        :param dict config: configuration
        :return: dict
        """
        dest_ = {}

        for key_, value_ in config.items():
            key_ = str(key_)

            if (
                isinstance(value_, dict)
                or isinstance(value_, list)
                or isinstance(value_, type)
            ):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            else:
                dest_[key_] = value_

        return dest_

    def format(self, key, **kwargs):
        """Apply quick format for string values with {arg}

        :param str key: key to argument
        :return: str
        """
        return self.__cfg[key].format(**kwargs)

    def keys(self):
        """Set-like object providing a view on keys"""
        return self.__cfg.keys()

    def __contains__(self, item):
        """Check if key in configuration

        :param any item: get
        :return: bool
        """
        return item in self.__cfg

    def __getitem__(self, key):
        """Get item ['item']

        :param str key: get environment name as item
        :return: any
        """

        return self.__cfg[key]


# export only this
__all__ = [__version__, EnvYAML]
