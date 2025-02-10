from dagster_delta.io_manager.arrow import DeltaLakePyarrowIOManager
from dagster_delta.io_manager.base import (
    BaseDeltaLakeIOManager,
    SchemaMode,
    WriteMode,
    WriterEngine,
)

__all__ = [
    "WriteMode",
    "WriterEngine",
    "SchemaMode",
    "BaseDeltaLakeIOManager",
    "DeltaLakePyarrowIOManager",
]


try:
    from dagster_delta.io_manager.polars import DeltaLakePolarsIOManager  # noqa

    __all__.extend(["DeltaLakePolarsIOManager"])

except ImportError as e:
    if "polars" in str(e):
        pass
    else:
        raise e
