# Get started

### project structure
```bash
./
├── bin                    # bin scripts directory
│   ├── compilemessages    # compile project translates
│   └── makemessages       # generate translates
├── data                   # docker containers data
│   └── redis              # redis container data
├── locale                 # locales directory                    
│   ├── en
│   ├── ru
│   └── project.pot        # project translates template
├── services               # project services
│   ├── api                # api service
│   ├── contrib            # modules shared with services. may be packaging in future
│   ├── docs               # project documentation
│   └── rpc                # service for run background jobs
├── Dockerfile.api
├── Dockerfile.rpc
├── Pipfile
├── README.md
├── docker-compose.yml
└── pytest.ini
```
### Prepare development

1. Create necessary directories and files:
```bash
mkdir -r ./data/redis
touch .env
```
2. Create .env file
```
PYTHONPATH=$PYTHONPATH:/contrib
DB_NAME='./db.sqlite'
REDIS_HOST='redis'
SIGN_DOMAIN='127.0.0.1:8000/confirmation/'
RPC_URL='http://rpc:8080'

MESSAGE_CONFIRM=1
MESSAGE_WELCOME=2
MESSAGE_RESTORE=3

FILE_NOTIFICATION='FileLogBackendInterface'

LOCALE_DOMAIN='project'
LOCALE_DIR='/locale'
```
3. Build and run containers
```bash
docker-compose up
```
# Internationalization

1 Create/update translatable strings
```bash
./bin/makemessages ./services
```
2. Compile messages
```bash
./bin/compilemessages
```

# Development documentation

The project use sphinx library for development documentation. See mode on https://www.sphinx-doc.org/en/master/
