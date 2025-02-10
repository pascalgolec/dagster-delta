from collections.abc import Sequence
from typing import Any

import dagster as dg
import pyarrow as pa
import pyarrow.dataset as ds
from dagster._core.storage.db_io_manager import DbTypeHandler

from dagster_delta._handler.base import ArrowTypes, DeltalakeBaseArrowTypeHandler
from dagster_delta.io_manager.base import (
    BaseDeltaLakeIOManager as BaseDeltaLakeIOManager,
)


class DeltaLakePyarrowIOManager(BaseDeltaLakeIOManager):  # noqa: D101
    @staticmethod
    def type_handlers() -> Sequence[DbTypeHandler]:  # noqa: D102
        return [_DeltaLakePyArrowTypeHandler()]


class _DeltaLakePyArrowTypeHandler(DeltalakeBaseArrowTypeHandler[ArrowTypes]):  # noqa: D101
    def from_arrow(self, obj: pa.RecordBatchReader, target_type: type[ArrowTypes]) -> ArrowTypes:  # noqa: D102
        if target_type == pa.Table:
            return obj.read_all()
        return obj

    def to_arrow(self, obj: ArrowTypes) -> tuple[ArrowTypes, dict[str, Any]]:  # noqa: D102
        if isinstance(obj, ds.Dataset):
            return obj.scanner().to_reader(), {}
        return obj, {}

    def get_output_stats(self, obj: ArrowTypes) -> dict[str, dg.MetadataValue]:  # noqa: ARG002
        """Returns output stats to be attached to the the context.

        Args:
            obj (ArrowTypes): Union[pa.Table, pa.RecordBatchReader, ds.Dataset]

        Returns:
            Mapping[str, MetadataValue]: metadata stats
        """
        return {}

    @property
    def supported_types(self) -> Sequence[type[object]]:
        """Returns the supported dtypes for this typeHandler"""
        return [pa.Table, pa.RecordBatchReader, ds.Dataset]
