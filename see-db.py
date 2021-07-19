#!/usr/bin/env python

from sqlitedict import SqliteDict  # type: ignore

DB_FILE = 'results.db'


def main() -> None:
    db = SqliteDict(DB_FILE)
    for key in db:
        print(key)
    db.close()


if __name__ == '__main__':
    main()
