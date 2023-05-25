alembic --config .\settings.ini --name database revision --autogenerate -m 'first migration'
alembic --config .\settings.ini --name database upgrade head
alembic --config .\settings.ini --name database current