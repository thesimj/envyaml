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
from typing import Any

from yaml import safe_load


class EnvYaml:
    __version__: str = '0.1901'

    env_path: str = ['env.yaml', 'env.yml']
    separator: str = '__'

    __config_raw: dict = {}
    __config: dict = {}

    def __init__(self, file_path: str = None, separator: str = '__'):
        self.env_path = [file_path] if file_path else os.environ.get('ENV_YAML_FILE', self.env_path)
        self.separator = separator

        # read and parse files
        with open(file_path) as f:
            # expand env vars
            self.__config_raw = safe_load(os.path.expandvars(f.read()))

            # make it flat
            if self.__config_raw:
                self.__config = self.__dict_flat(self.__config_raw)

    def export(self) -> dict:
        return self.__config_raw.copy()

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
                    dest_[str.join(self.separator, deep + [key_])] = value_
                else:
                    dest_[key_] = value_

        return dest_

    def __getattr__(self, name: str) -> Any:
        return self.__config[name]

    def __getitem__(self, item):
        return self.__config[item]
