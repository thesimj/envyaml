# EnvYAML | Easy configuration file parser for structured data

[![Latest Version](https://badgen.net/pypi/v/envyaml)](https://pypi.python.org/pypi/envyaml/) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/envyaml.svg)](https://anaconda.org/conda-forge/envyaml)
[![EnvYaml CI/CD Pipeline](https://github.com/thesimj/envyaml/actions/workflows/main.yml/badge.svg)](https://github.com/thesimj/envyaml/actions/workflows/main.yml)
[![Coverage Status](https://badgen.net/coveralls/c/github/thesimj/envyaml)](https://coveralls.io/github/thesimj/envyaml?branch=main)
![Versions](https://badgen.net/pypi/python/envyaml)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Alerts](https://img.shields.io/lgtm/alerts/g/thesimj/envyaml.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thesimj/envyaml/alerts/)
[![Code Quality](https://img.shields.io/lgtm/grade/python/g/thesimj/envyaml.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thesimj/envyaml/context:python)
[![License](https://img.shields.io/pypi/l/envyaml.svg)](LICENSE)
[![Downloads](https://static.pepy.tech/personalized-badge/envyaml?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/envyaml)

### Motivation
Modern configuration files become to be more and more complex, flexible, and readable.
YAML file format is perfect to store configuration but had no option to pass environment variables. They give flexibility, readability and provide an option to store complex data structure.
This project goal is to simplify usage of the YAML file and environment variables as program configuration files with easy config key access.


### Install
```bash
pip install envyaml
```
or
```bash
conda install conda-forge::envyaml
```

### Basic usage
Let's assume we had a project with this config file `env.yaml`

```yaml
# env.yaml
project:
  name: "${PROJECT_NAME}-${PROJECT_ID}"

database:
    host: $DATABASE_HOST
    port: 3301
    username: username
    password: $DATABASE_PASSWORD
    database: test

    table:
      user: table_user
      blog: table_blog

    query: |-
      SELECT * FROM "users" WHERE "user" = $1 AND "login" = $2 AND "pwd" = $3

    insert: |-
      INSERT INTO "{table}" (user, login) VALUES ($1, $2)

redis:
    host: $REDIS_HOST|127.0.0.1
    port: 5040
    db: $REDIS_DB|3 # with default value

    config:
      expire: 300
      prefix: $REDIS_PREFIX

escaped: $$.extra

empty_env: $NOT_EXIST_ENV_VARIABLE
```

Environment variables set to
```
PROJECT_NAME=simple-hello
PROJECT_ID=42
DATABASE_HOST=xxx.xxx.xxx.xxx
DATABASE_PASSWORD=super-secret-password
REDIS_PREFIX=state
```

Parse file with `EnvYAML`

```python
from envyaml import EnvYAML

# read file env.yaml and parse config
env = EnvYAML('env.yaml')

# access project name
print(env['project.name'])

# >> simple-hello-42

# access whole database section
print(env['database'])

# {
# 'database': 'test',
# 'host': 'xxx.xxx.xxx.xxx',
# 'password': 'super-secret-password',
# 'port': 3301,
# 'table':
#   {
#       'blog': 'table_blog',
#       'user': 'table_user'
#   },
# 'username': 'username'
# }

# access database host value as key item
print(env['database.host'])

# >> xxx.xxx.xxx.xxx

# access database user table value as key item
print(env['database.table.user'])

# >> table_user

# get sql query with $1,$2,$3 variables
print(env['database.query'])

# >> SELECT * FROM "users" WHERE "user" = $1 AND "login" = $2 AND "pwd" = $3

# using default values if variable not defined
# one example is redis host and redis port, when $REDIS_HOST not set then default value will be used
print(env['redis.host'])

# >> 127.0.0.1

# one example is redis host and redis port, when $REDIS_DB not set then default value will be used
print(env['redis.db'])

# >> 3

# access list items by number
print(env['list_test'][0])

# >> one

# access list items by number as key
print(env['list_test.1'])

# >> two

# test if you have key
print('redis.port' in env)

# >> True

```

Access config with `get` function and default value
```python
print(env.get('not.exist.value', 'default'))
# >> default

print(env.get('empty_env', 'default'))
# >> default

print(env['empty_env'])
# >> None
```

Use `format` function to update placeholder
```python
print(env.format('database.insert', table="users"))
# >> INSERT INTO "users" (user, login) VALUES ($1, $2)
```

### Strict mode
This mode is **enable by default** and prevents from declaring variables that do not exist in `environment variables` or `.env` file. This leads to having runtime `ValueError` exception when variables do not define with message `Strict mode enabled, variable $VAR not defined!`. To disable **strict** mode specify `strict=False` at EnvYAML object initialization. Another option to disable `strict` mode is to define `ENVYAML_STRICT_DISABLE` environment variable before initializing EnvYAML object.


### Escaped variables
In case of usage `$` in env.yaml file as value double `$$` should be used. Example:
Use `escaped` variable
```python
print(env['escaped'])
# >> $.extra
```


### License
MIT licensed. See the [LICENSE](LICENSE) file for more details.
