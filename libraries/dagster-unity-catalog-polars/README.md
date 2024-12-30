# Dagster Unity Catalog Polars

A IO Manager to read Unity Catalog Tables in Dagster orchestrated pipelines.

## Instantiating the IO Manager

To instantiate the IO Manager you need to pass a non-cached token generating function as a `Callable[..., str]` such that the load functions generate and refresh the thoken as needed. Is set to every 1000 queries by default, this should suffice most of the time.

The `databricks_settings` input argument needs to be a dictionary with the following structure:
```python
databricks_settings = {
    "server_hostname":<DB-HOSTNAME>,
    "http_path":<SQL-WAREHOUSE-PATH>,
}
```

