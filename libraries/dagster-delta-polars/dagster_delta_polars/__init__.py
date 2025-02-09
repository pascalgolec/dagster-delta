from warnings import warn

from .deltalake_polars_type_handler import (
    DeltaLakePolarsIOManager,
    DeltaLakePolarsTypeHandler,
)

__all__ = [
    "DeltaLakePolarsIOManager",
    "DeltaLakePolarsTypeHandler",
]


warn(
    """This library has been deprecated. Polars integration has moved into `dagster-delta`.
     This can be installed through `pip install dagster-delta[polars]`

     from dagster_delta.io_manager import DeltaLakePolarsIOManager

     """,
    DeprecationWarning,
    stacklevel=2,
)
