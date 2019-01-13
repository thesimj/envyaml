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

redis:
    host: $REDIS_HOST
    port: 5040
    
    config:
      expire: 300
      prefix: $REDIS_PREFIX
```

and environment variables set to
```
PROJECT_NAME=simple-hello
PROJECT_ID=42
DATABASE_HOST=xxx.xxx.xxx.xxx
DATABASE_PASSWORD=super-secret-password
REDIS_PREFIX=state
```

parse file with `EnvYAML`

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

# access database host value as properties name
print(env['database.host'])

# >> xxx.xxx.xxx.xxx

# access database user table value as properties name
print(env['database.table.user'])

# >> table_user

# access list items by number
print(env['list_test'][0])

# >> one
```

access config parameters with key option `['name']`
```python
print(env['database.port'])
# >> 3301
```

access config with `get` function and default value
```python
print(env.get('not.exist.value', 'default'))
# >> default
```

### License
MIT licensed. See the [LICENSE](LICENSE) file for more details.
