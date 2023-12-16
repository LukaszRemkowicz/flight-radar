##### A package responsible for getting flight data

##### aerich migration flow:

1) Initialization:
   - aerich init -t {file_with_db_config}.{DB_config_as_dict}  (settings.DB_CONFIG)
   - aerich init-db

2) Migrations:
   - aerich migrate
   - aerich upgrade