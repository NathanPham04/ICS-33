import sqlite3
from p2app.events import *

class AppLevelHandler:
    def __init__(self, engine: 'Engine') -> None:
        self.engine = engine

    def handle_quit(self, quit_event: QuitInitiatedEvent) -> EndApplicationEvent:
        """Handle the quit application event"""
        if self.engine.connection:
            self.engine.connection.close()
        yield EndApplicationEvent()

    def handle_open(self, open_event: OpenDatabaseEvent) -> 'connection':
        """Handle the open database event"""
        path = open_event.path()
        if path.is_dir():
            yield from ()
            return
        try:
            connection = sqlite3.connect(path)
            self.engine.set_connection(connection)
            cursor = self.engine.connection.execute(
                '''SELECT name FROM sqlite_schema'''
                """ WHERE type = 'table';"""
            )
            tables = cursor.fetchall()
            cursor.close()
            tables = set(map(' '.join, tables))
            if 'region' in tables and 'country' in tables and 'continent' in tables:
                yield DatabaseOpenedEvent(path)
            else:
                yield ErrorEvent("Database doesn't have region, country, or continent tables.")
        except Exception as e:
            yield DatabaseOpenFailedEvent('Something went wrong opening the database: ' + str(e))

    def handle_close(self, close_event: CloseDatabaseEvent) -> DatabaseClosedEvent:
        """Handle the close database event"""
        if self.engine.connection:
            self.engine.connection.close()
            self.engine.connection = None
            yield DatabaseClosedEvent()
        else:
            yield ErrorEvent('No connection to database to close')

if __name__ == '__main__':
    pass

