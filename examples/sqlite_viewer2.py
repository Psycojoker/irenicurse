import logging
import sqlite3
import sys
sys.path.append("..")

from os.path import exists

from irenicurse.widget import FullListWidget, bind_to_key
from irenicurse import run


class TableListViewerWidget(FullListWidget):
    def __init__(self, database_connection):
        logging.debug("[TableListViewerWidget] init with connection: %s" % database_connection)
        self.database_connection = database_connection
        FullListWidget.__init__(self, self.get_table_list())

    def get_table_list(self):
        return [x[0] for x in self.database_connection.execute("select name from sqlite_master where type = 'table';").fetchall()]

    def get_title(self):
        return "SQLite Viewer example 2"

    def get_footer(self):
        return '"j", "k", "up", "down" to move, "q" to quit, "enter" to see the columns of the current table'

    @bind_to_key("enter")
    def show_columns_list(self):
        self.call(TableColumnsListViewerWidget(self.database_connection, self.get_current_item()))


class TableColumnsListViewerWidget(FullListWidget):
    def __init__(self, database_connection, table_name):
        self.database_connection = database_connection
        self.table_name = table_name
        FullListWidget.__init__(self, self.get_table_columns_list())

    def get_table_columns_list(self):
        return [x[1] for x in self.database_connection.execute("pragma table_info(%s)" % self.table_name).fetchall()]

    def get_title(self):
        return "Columns of table: %s" % self.table_name

    def get_footer(self):
        return '"j", "k", "up", "down" to move, "q" to return to table listing'


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print >>sys.stderr, "give the path to the database as first argument"
        sys.exit(1)

    if not exists(sys.argv[1]):
        print >>sys.stderr, "file doesn't exist, stop"

    run(TableListViewerWidget(sqlite3.connect(sys.argv[1])))
