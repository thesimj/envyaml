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

from yaml import safe_load
from collections import MutableMapping

__version__ = '0.1908'


class EnvYAML:
    __version__ = __version__

    DEFAULT_ENV_YAML_FILE = 'env.yaml'
    DEFAULT_ENV_FILE = '.env'

    __env_file = None  # type:str
    __yaml_file = None  # type: str
    __config_raw = None  # type:dict
    __config = None  # type: dict

    def __init__(self, yaml_file=None, env_file=None, include_environment=True):
        """Create EnvYAML class instance and read content from environment and files if they exists

        :param yaml_file: file path for config or env.yaml by default
        :param env_file: file path for .env file or None by default
        :param include_environment: include environment variable, by default true
        :type yaml_file: str
        :type env_file: str
        :type include_environment: bool
        :rtype: EnvYAML
        """
        self.__yaml_file = yaml_file
        self.__env_file = env_file

        # get env file and read
        env_config = self.__read_env_file(self.__get_file_path(env_file, 'ENV_FILE', self.DEFAULT_ENV_FILE))
        yaml_config = self.__read_yaml_file(self.__get_file_path(yaml_file, 'ENV_YAML_FILE', self.DEFAULT_ENV_YAML_FILE))

        # compose raw config
        self.__config_raw = dict(os.environ) if include_environment else {}
        self.__config_raw.update(env_config)
        self.__config_raw.update(yaml_config)

        # compose config
        self.__config = self.__flat(self.__config_raw)

    def get(self, key, default=None):
        """Get configuration variable with default value. If no `default` value set use None

        :param key: name for the configuration key
        :param default: default value if no key found
        :type default: any
        :type key: any
        :rtype: any
        """
        return self.__config.get(key, default)

    def export(self):
        """Export config

        :return: dict with config
        :rtype: dict
        """
        return self.__config_raw.copy()

    @staticmethod
    def environ():
        """Get os.environ mapping object

        :rtype: MutableMapping
        :return: A mapping object representing the string environment
        """
        return os.environ

    @staticmethod
    def __read_env_file(file_path):
        """read and parse env file

        :type file_path: str
        :rtype: dict
        """
        config = {}

        if file_path:
            with open(file_path) as f:
                for line in f.readlines():  # type:str
                    if line and line[0].isalpha() and ('=' in line):
                        name, value = line.strip().split('=', 1)  # type: str,str
                        # strip value
                        value = value.strip().strip('\'\"')
                        name = name.strip().strip('\'\"')
                        # set environ
                        os.environ[name] = value
                        # set local config
                        config[name] = value

        return config

    @staticmethod
    def __read_yaml_file(file_path):
        """read and parse yaml file

        :type file_path: str
        :rtype: dict
        """
        # read and parse files
        with open(file_path) as f:
            # expand env vars
            return safe_load(os.path.expandvars(f.read()))

    @staticmethod
    def __get_file_path(file_path, env_name, default):
        """Construct file path

        :rtype: str
        :type file_path: str
        :type env_name: str
        :type default: str
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

        :type prefix: str
        :type config: any
        :rtype: dict
        """
        dest_ = {}

        elements = enumerate(config) if (isinstance(config, list) or isinstance(config, tuple)) else config.items()  # type: (str, any)

        for key_, value_ in elements:
            key_ = prefix + '.' + str(key_)

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

        :rtype: dict
        :type config: dict
        """
        dest_ = {}

        for key_, value_ in config.items():
            key_ = str(key_)

            if isinstance(value_, dict) or isinstance(value_, list) or isinstance(value_, type):
                dest_[key_] = value_
                dest_.update(EnvYAML.__flat_deep(key_, value_))

            else:
                dest_[key_] = value_

        return dest_

    def keys(self):
        """Set-like object providing a view on keys"""
        return self.__config.keys()

    def __getitem__(self, item):
        """ Get item ['item']

        :rtype: any
        :type item: str
        """
        return self.__config[item]


# export only this
__all__ = [__version__, EnvYAML]
