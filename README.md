# EnvYAML | [![Build Status](https://travis-ci.com/thesimj/envyaml.svg?branch=master)](https://travis-ci.com/thesimj/envyaml) [![Coverage Status](https://coveralls.io/repos/github/thesimj/envyaml/badge.svg?branch=master)](https://coveralls.io/github/thesimj/envyaml?branch=master)
Simple YAML configuration file parser with easy access for structured data

### Why
Modern configuration file become to be more complex, flexible and readable. 
YAML file format are perfect to store configuration file but had no option to pass environment variables.
This project try to simplify usage YAML file and environment variables as program configuration file with easy config key access.  

### Basic usage
Let's assume we had a project with this config file `env.yaml`

```yaml
# env.yaml
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
$DATABASE_HOST=xxx.xxx.xxx.xxx
$DATABASE_PASSWORD=super-secret-password
$REDIS_PREFIX=state
```

parse file with `EnvYAML`

```python
from envyaml import EnvYAML

# read file env.yaml and parse config
env = EnvYAML('env.yaml')

# access whole database section
print(env.database)

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
print(env.database__host)

# >> xxx.xxx.xxx.xxx

# access database user table value as properties name
print(env.database__table__user)

# >> table_user
```

access config parameters with key option `['name']`
```python
print(env['database__port'])
# >> 3301
```

access config with `get` function and default value
```python
print(env.get('not__exist__value', 'default'))
# >> default
```

### License
MIT licensed. See the [LICENSE](LICENSE) file for more details.
