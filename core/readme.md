## FastAPI

### Aerich

#### initiate migration

`aerich init -t core.settings.DATABASE --location=./core/migrations`

#### create initial migration

`aerich init-db`

#### Update models and make migrate

`aerich migrate --name drop_column`

#### Upgrade to latest version

`aerich upgrade`

#### Downgrade to previous version

`aerich downgrade`

#### Show history

`aerich history`

#### Show heads to be migrated

`aerich heads`
