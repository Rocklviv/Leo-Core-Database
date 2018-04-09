import os
import json
import logging
import rethinkdb as r
from rethinkdb.errors import ReqlDriverError, ReqlOpFailedError


class Database(object):
    def __init__(self, host=None, port=None, dbname=None):
        self.log = logging.getLogger('root')
        self.conn = None
        self.db_exists = 0
        self.host = host or os.getenv('DB_HOST')
        self.port = port or os.getenv('DB_PORT')
        self.dbname = dbname or os.getenv('DB_NAME')

    def connect(self):
        """
        Creates a connection to database.
        :return:
        """
        try:
            self.log.info('Connecting to database: {}:{}'.format(self.host, self.port))
            self.conn = r.connect(self.host, self.port).repl()
            self.conn.use(self.dbname)
            if self.db_exists == 0:
                self.create_database(self.dbname)
        except ReqlDriverError as e:
            self.log.error(e)
        except Exception as e:
            self.log.error(e)

    def create_database(self, dbname):
        """
        Create database.
        :param dbname: string Database name.
        :return:
        """
        try:
            r.db_create(dbname).run(self.conn)
            self.log.info("Database {} successfully created".format(dbname))
            self.db_exists = 1
        except ReqlOpFailedError as e:
            self.log.debug("Could not create DB: {}. Probably Database already exists.".format(dbname))
            self.db_exists = 1

    def select(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        table = None
        data = []
        if args:
            for value in args:
                table = value
        query = kwargs.get('query')
        self.log.debug('QUERY: {}'.format(query))

        if type(query) is str:
            cursor = r.table(table).get(query).run(self.conn)
        elif type(query) is dict:
            cursor = r.table(table).filter(query).run(self.conn)
        else:
            cursor = r.table(table).run(self.conn)

        if len(cursor.items) > 0:
            for document in cursor:
                data.append(document)
            return data
        else:
            return False

    def insert(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        table = None
        if args:
            for value in args:
                table = value
        query = kwargs.get('query')
        if query:
            cursor = r.table(table).insert(query).run(self.conn)
            if cursor.get('inserted') > 0:
                return True
            elif cursor.get('error'):
                return cursor.get('first_error')
            else:
                return False
        else:
            return False

    def update(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        table = None
        if args:
            for value in args:
                table = value
        query = kwargs.get('query')
        if query:
            cursor = r.table(table).update(query).run(self.conn)
            if cursor:
                return True
            else:
                return False
        else:
            return False, json.dumps({'status': 11, 'message': 'Cannot update document without a query.'})

    def delete(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        table = None
        if args:
            for value in args:
                table = value
        query = kwargs.get('query')
        if query:
            cursor = r.table(table).get(query).delete().run(self.conn)
            if cursor.get('deleted') > 0:
                return True
            else:
                return False
        else:
            return False, json.dumps({'status': 12, 'message': 'Cannot delete document without query.'})

    def insert_or_update(self, *args, **kwargs):
        pass

    def getField(self, *args, **kwargs):
        table = None
        data = []
        if args:
            for value in args:
                table = value
        cursor = r.table(table).get_field(kwargs.get('field')).run(self.conn)
        if len(cursor.items) > 0:
            for document in cursor:
                return document
        else:
            return int(0)

    def table_list(self):
        """

        :return:
        """
        return r.db(self.dbname).table_list()