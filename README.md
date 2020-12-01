# EnvYAML | [![Latest Version](https://pypip.in/version/envyaml/badge.svg)](https://pypi.python.org/pypi/envyaml/) [![Build Status](https://travis-ci.com/thesimj/envyaml.svg?branch=master)](https://travis-ci.com/thesimj/envyaml) [![Coverage Status](https://coveralls.io/repos/github/thesimj/envyaml/badge.svg?branch=master)](https://coveralls.io/github/thesimj/envyaml?branch=master) ![Versions](https://img.shields.io/pypi/pyversions/envyaml.svg) ![License](https://img.shields.io/pypi/l/envyaml.svg)
Simple YAML configuration file parser with easy access for structured data

### Why
Modern configuration file become to be more and more complex, flexible and readable.
YAML file format are perfect to store configuration, but had no option to pass environment variables. They give flexibility, readability and provide option to store complex data structure.
This project aim to simplify usage of the YAML file and environment variables as program configuration file with easy config key access.

### Install
```bash
pip install envyaml
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
This mode is **enable by default** and prevent from declaring variables that
not exist in `environment variables` or `.env` file. This leads to have runtime ValueError exception when variables
not define with message `Strict mode enabled, variable $VAR not defined!`. To disable **strict** mode
specify `strict=False` to EnvYAML object

### License
MIT licensed. See the [LICENSE](LICENSE) file for more details.
