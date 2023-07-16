import sqlite3

from pathlib import Path
from typing import Any, Optional


ParamsType = Optional[tuple[Any, ...]]
QueryReturnType = tuple[tuple[str, ...], list[tuple[Any, ...]]]


class SQLiteMixin:
    """A mixin for SQLite3 querying."""

    def query(self, db: Path, query: str, params: ParamsType = None) -> QueryReturnType:
        """Query an SQLite3 database object, returns a tuple result of (column_names, rows).
        :param db: the path object to the sqlite3 file
        :param query: the query string (including any placeholders), for example:
                        'SELECT * FROM example WHERE foo = ?;'
        :param params: an optional tuple of all parameters for placeholder binding, for example:
                        ('Hello World')
                       the number of placeholders in this tuple must match the number of '?' placeholders
                       in the query string"""
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute(query, params if params else ())
        column_names = [colname[0] for colname in cursor.description]  # tuple with colname at index 0
        results = [row for row in cursor.fetchall()]
        connection.close()

        return (column_names, results)
