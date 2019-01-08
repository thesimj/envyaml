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

__version__ = '0.1903'


class YDict:
    def __init__(self, dictionary):
        """Create YDict instance based on `dict`

        :type dictionary: dict
        :rtype: YDict
        """
        self.__data = dictionary

    def __getattr__(self, item):
        attr = self.__data[item]

        if isinstance(attr, dict):
            return YDict(attr)

        return self.__data[item]

    def __getitem__(self, item):
        return self.__data[item]

    def get(self, key, default=None):
        """Get configuration variable with default value. If no `default` value set use None

        :param key: name for the configuration key
        :param default: default value if no key found
        :type default: any
        :type key: any
        :rtype: any
        """
        if key in self.__data:
            return self.__data[key]

        return default


class EnvYAML:
    __version__ = __version__

    DEFAULT_ENV_YAML_FILE = 'env.yaml'
    DEFAULT_ENV_FILE = '.env'

    __env_file = None  # type:str
    __yaml_file = None  # type: str
    __config_raw = None  # type:dict
    __config = None  # type:YDict

    def __init__(self, yaml_file=None, env_file=None):
        """Create EnvYAML class instance and read content from file

        :param yaml_file: file path for config or env.yaml by default
        :param env_file: file path for `.env` file or None by default
        :type yaml_file: str
        :type env_file: str
        :rtype: EnvYAML
        """
        self.__yaml_file = yaml_file
        self.__env_file = env_file

        # get env file and read
        env_config = self.__read_env_file(self.__get_file_path(env_file, 'ENV_FILE', self.DEFAULT_ENV_FILE))
        yaml_config = self.__read_yaml_file(self.__get_file_path(yaml_file, 'ENV_YAML_FILE', self.DEFAULT_ENV_YAML_FILE))

        # compose raw config
        self.__config_raw = {}
        self.__config_raw.update(env_config)
        self.__config_raw.update(yaml_config)

        # compose config
        self.__config = YDict(self.__dict_flat(self.__config_raw))

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
    def __read_env_file(file_path):
        """read and parse env file

        :type file_path: str
        :rtype: dict
        """
        config = {}

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
        """ construct file path

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

    def __dict_flat(self, config, deep=None):
        """ Flat dictionaries in recursive way

        :rtype: dict
        :type config: dict
        :type deep: [str]
        """
        dest_ = {}
        for key_, value_ in config.items():
            key_ = str(key_)
            if isinstance(value_, dict):
                if deep:
                    dest_.update(self.__dict_flat(value_, deep=deep + [key_]))
                else:
                    dest_.update(self.__dict_flat(value_, deep=[key_]))
            if isinstance(value_, list) or isinstance(value_, tuple):
                if deep:
                    dest_.update(self.__dict_flat(dict(enumerate(value_)), deep=deep + [key_]))
                else:
                    dest_.update({key_: value_})
                    dest_.update(self.__dict_flat(dict(enumerate(value_)), deep=[key_]))
            else:
                if deep:
                    dest_[str.join('.', deep + [key_])] = value_
                else:
                    dest_[key_] = value_

        return dest_

    def __getattr__(self, name):
        """ Get as attribute .name

        :rtype: any
        :type name: str
        """
        return self.__config.__getattr__(name)

    def __getitem__(self, item):
        """ Get item ['item']

        :rtype: str
        :type item: str
        """
        return self.__config.__getitem__(item)


# export only this
__all__ = [__version__, EnvYAML]
