#### initiate migration

`aerich init -t core.settings.TORTOISE_ORM --location=./database/migrations`

#### create initial migration

`aerich init-db`

#### Update models and make migrate

`aerich migrate --name [migration_name]`

#### Upgrade to latest version

`aerich upgrade`

#### Downgrade to previous version

`aerich downgrade`

#### Show history

`aerich history`

#### Show heads to be migrated

`aerich heads`
