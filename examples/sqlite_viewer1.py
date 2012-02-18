import logging
import sqlite3
import sys
sys.path.append("..")

from os.path import exists

from irenicurse.widget import FullListWidget
from irenicurse import run


class TablesViewerWidget(FullListWidget):
    def __init__(self, database_connection):
        logging.debug("[TablesViewerWidget] init with connection: %s" % database_connection)
        self.database_connection = database_connection
        FullListWidget.__init__(self, self.get_table_list())

    def get_table_list(self):
        return [x[0] for x in self.database_connection.execute("select name from sqlite_master where type = 'table';").fetchall()]

    def get_title(self):
        return "SQLite Viewer example 1"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print >>sys.stderr, "give the path to the database as first argument"
        sys.exit(1)

    if not exists(sys.argv[1]):
        print >>sys.stderr, "file doesn't exist, stop"

    run(TablesViewerWidget(sqlite3.connect(sys.argv[1])))
