# -*- coding: utf-8 -*-
# This file is part of EnvYaml project
# https://github.com/thesimj/envyaml
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


import os
from typing import Optional

from yaml import safe_load

__version__ = '0.1902'


class EnvYAML:
    __version__: str = __version__

    DEFAULT_ENV_YAML_FILE: str = 'env.yaml'
    DEFAULT_ENV_FILE: str = '.env'

    __env_file: str = None
    __yaml_file: str = None
    __config_raw: dict = {}
    __config: dict = {}
    __separator: str = '__'

    def __init__(self, yaml_file: str = None, env_file: str = None, separator: str = '__'):
        """Create EnvYAML class instance and read content from file

        :param yaml_file: file path for config or env.yaml by default
        :param separator: use separator for path levels
        """
        self.__yaml_file = yaml_file
        self.__env_file = env_file
        self.__separator = separator

        # get env file and read
        env_config: dict = self.__read_env_file(self.__get_file_path(env_file, 'ENV_FILE', self.DEFAULT_ENV_FILE))
        yaml_config: dict = self.__read_yaml_file(self.__get_file_path(yaml_file, 'ENV_YAML_FILE', self.DEFAULT_ENV_YAML_FILE))

        # compose raw config
        self.__config_raw = {**env_config, **yaml_config}

        # compose config
        self.__config = self.__dict_flat(self.__config_raw)

    def get(self, key: str, default: any = None) -> any:
        """Get config variable with default value. If no `default` value set use None

        :param key: config key
        :param default: value will be used when no key found
        :return: value for config key or default value
        :rtype any
        """
        if key in self.__config:
            return self.__config[key]

        return default

    def export(self) -> dict:
        """Export config
        :return: dict with config
        """
        return self.__config_raw.copy()

    @staticmethod
    def __read_env_file(file_path: str):
        config: dict = {}

        if file_path:
            with open(file_path) as f:
                for line in f.readlines():  # type:str
                    name, value = line.strip().split('=', 1)
                    # set environ
                    os.environ[name] = value
                    # set local config
                    config[name] = value

        return config

    @staticmethod
    def __read_yaml_file(file_path: str) -> dict:
        # read and parse files
        with open(file_path) as f:
            # expand env vars
            return safe_load(os.path.expandvars(f.read()))

    @staticmethod
    def __get_file_path(file_path: str, env_name: str, default: str) -> Optional[str]:
        if file_path:
            return file_path

        elif os.environ.get(env_name):
            return os.environ.get(env_name)

        elif os.path.exists(default):
            return default

        # if file not found, then none
        return None

    def __dict_flat(self, config: any, deep: [str] = None) -> dict:
        dest_: dict = {}
        for key_, value_ in config.items():
            key_ = str(key_)
            if isinstance(value_, dict):
                if deep:
                    dest_.update(self.__dict_flat(value_, deep=deep + [key_]))
                else:
                    dest_.update(self.__dict_flat(value_, deep=[key_]))
            if isinstance(value_, list):
                if deep:
                    dest_.update(self.__dict_flat(dict(enumerate(value_)), deep=deep + [key_]))
                else:
                    dest_.update(self.__dict_flat(dict(enumerate(value_)), deep=[key_]))
            else:
                if deep:
                    dest_[str.join(self.__separator, deep + [key_])] = value_
                else:
                    dest_[key_] = value_

        return dest_

    def __getattr__(self, name: str) -> any:
        return self.__config[name]

    def __getitem__(self, item):
        return self.__config[item]
