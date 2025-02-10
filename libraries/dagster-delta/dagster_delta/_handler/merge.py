import logging
from typing import Any, Optional, TypeVar, Union

import pyarrow as pa
import pyarrow.dataset as ds
from deltalake import CommitProperties, DeltaTable, WriterProperties
from deltalake.table import FilterLiteralType

from dagster_delta._handler.utils import create_predicate
from dagster_delta.config import MergeType

T = TypeVar("T")
ArrowTypes = Union[pa.Table, pa.RecordBatchReader, ds.Dataset]


def merge_execute(
    dt: DeltaTable,
    data: Union[pa.RecordBatchReader, pa.Table],
    merge_config: dict[str, Any],
    writer_properties: Optional[WriterProperties],
    commit_properties: Optional[CommitProperties],
    custom_metadata: Optional[dict[str, str]],
    delta_params: dict[str, Any],
    merge_predicate_from_metadata: Optional[str],
    partition_filters: Optional[list[FilterLiteralType]] = None,
) -> dict[str, Any]:
    merge_type = merge_config.get("merge_type")
    error_on_type_mismatch = merge_config.get("error_on_type_mismatch", True)

    if merge_predicate_from_metadata is not None:
        predicate = str(merge_predicate_from_metadata)
    elif merge_config.get("predicate") is not None:
        predicate = str(merge_config.get("predicate"))
    else:
        raise Exception("merge predicate was not provided")

    target_alias = merge_config.get("target_alias")

    if partition_filters is not None:
        partition_predicate = create_predicate(partition_filters, target_alias=target_alias)

        predicate = f"{predicate} AND {partition_predicate}"
        logger = logging.getLogger()
        logger.setLevel("DEBUG")
        logger.debug("Using explicit MERGE partition predicate: \n%s", predicate)

    merger = dt.merge(
        source=data,
        predicate=predicate,
        source_alias=merge_config.get("source_alias"),
        target_alias=target_alias,
        error_on_type_mismatch=error_on_type_mismatch,
        writer_properties=writer_properties,
        commit_properties=commit_properties,
        custom_metadata=custom_metadata,
        **delta_params,
    )

    if merge_type == MergeType.update_only:
        return merger.when_matched_update_all().execute()
    elif merge_type == MergeType.deduplicate_insert:
        return merger.when_not_matched_insert_all().execute()
    elif merge_type == MergeType.upsert:
        return merger.when_matched_update_all().when_not_matched_insert_all().execute()
    elif merge_type == MergeType.replace_delete_unmatched:
        return merger.when_matched_update_all().when_not_matched_by_source_delete().execute()
    else:
        raise NotImplementedError
