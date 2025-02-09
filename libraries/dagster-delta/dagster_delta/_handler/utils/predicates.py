from datetime import datetime
from typing import Optional

from deltalake.table import FilterLiteralType


def create_predicate(
    partition_filters: list[FilterLiteralType],
    target_alias: Optional[str] = None,
) -> str:
    partition_predicates = []
    for part_filter in partition_filters:
        column = f"{target_alias}.{part_filter[0]}" if target_alias is not None else part_filter[0]
        value = part_filter[2]
        if isinstance(value, (int, float, bool)):
            value = str(value)
        elif isinstance(value, str):
            value = f"'{value}'"
        elif isinstance(value, list):
            value = str(tuple(v for v in value))
        elif isinstance(value, datetime):
            value = str(
                int(value.timestamp() * 1000 * 1000),
            )  # convert to microseconds
        partition_predicates.append(f"{column} {part_filter[1]} {value}")

    return " AND ".join(partition_predicates)
