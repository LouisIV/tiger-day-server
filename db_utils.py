import os
from urllib import parse
import psycopg2


class util:
    def __init__(self):
        self.conn = None
        self.curr_cursor = None

    def connect(self):
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

    def __create_cursor(self):
        if self.conn:
            self.curr_cursor = None
            self.curr_cursor = self.conn.cursor()

    def __close_cursor(self):
        if self.curr_cursor:
            self.curr_cursor.close()

    def __write_changes(self):
        if self.conn:
            self.conn.commit()

    def __close_connection(self):
        if self.conn:
            self.__close_cursor()
            self.conn.close()

    def execute_command(self, command):
        
