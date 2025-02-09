import logging
from typing import Optional

import pyarrow.dataset as ds
from dagster._core.storage.db_io_manager import TableSlice
from deltalake import DeltaTable

from dagster_delta._handler.utils.dnf import partition_dimensions_to_dnf

try:
    from pyarrow.parquet import filters_to_expression  # pyarrow >= 10.0.0
except ImportError:
    from pyarrow.parquet import _filters_to_expression as filters_to_expression


from dagster_delta.io_manager.base import (
    TableConnection,
)


def read_table(
    table_slice: TableSlice,
    connection: TableConnection,
    version: Optional[int] = None,
    date_format: Optional[dict[str, str]] = None,
    parquet_read_options: Optional[ds.ParquetReadOptions] = None,
) -> ds.Dataset:
    table = DeltaTable(
        table_uri=connection.table_uri,
        version=version,
        storage_options=connection.storage_options,
    )
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    logger.debug("Connection timeout duration %s", connection.storage_options.get("timeout"))

    partition_expr = None
    if table_slice.partition_dimensions is not None:
        partition_filters = partition_dimensions_to_dnf(
            partition_dimensions=table_slice.partition_dimensions,
            table_schema=table.schema(),
            input_dnf=True,
            date_format=date_format,
        )
        if partition_filters is not None:
            partition_expr = filters_to_expression([partition_filters])

    logger.debug("Dataset input predicate %s", partition_expr)
    dataset = table.to_pyarrow_dataset(parquet_read_options=parquet_read_options)
    if partition_expr is not None:
        dataset = dataset.filter(expression=partition_expr)

    return dataset
