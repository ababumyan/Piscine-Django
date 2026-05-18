from psycopg2 import connect ,OperationalError, DataError,ProgrammingError
from django.conf import settings
from django.http import JsonResponse, HttpResponse


class SqlService:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = connect(
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
                database=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD']
            )
            self.conn.cursor().execute('SELECT 1')  # Test the connection
            return True
        except OperationalError as e:
            print(f"Operational error: {e}")
            return False
        except DataError as e:
            print(f"Data error: {e}")
            return False
        except ProgrammingError as e:
            print(f"Programming error: {e}")
            return False
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def run_query(self,query):
        if not self.conn:
            raise Exception("Not connected to the database")
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Query execution failed: {e}")
            raise OperationalError(f"Query execution failed: {e}")

    
        
