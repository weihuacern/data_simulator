from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from constants import SQL_SALES_TABLE_CATALOG

class SQLAlchemyDBConnection(object):
    """SQLAlchemy database connection"""
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.session = None
    def __enter__(self):
        engine = create_engine(self.connection_string)
        Session = sessionmaker()
        self.session = Session(bind=engine)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

class SQLGenerator(object):
    """Class to generate sql table, fill pii row into sql table"""
    def __init__(self, sql_uri):
        # mysql+pymysql://<user>:<password>@<host>[:<port>]/<dbname>
        self.sql_uri = sql_uri

    # Function to create the table with specific schema
    # Note, the key_col_name is required as we have requirement on scanner
    def sql_create_table(self, tab_name, key_col_name, col_name_list):
        # Generate columns
        # FIXME, for now, just support string type for all field
        sql_alchemy_key_cols = [Column(key_col_name, String(100), primary_key=True)]
        sql_alchemy_nokey_cols = [Column(col_name, String(100)) for col_name in col_name_list if col_name != key_col_name]
        sql_alchemy_cols = sql_alchemy_key_cols + sql_alchemy_nokey_cols

        # Create sql alchemy engine
        engine = create_engine(self.sql_uri)
        # Create a metadata instance
        metadata = MetaData(engine)
        # Declare a table
        table = Table(tab_name, metadata, *sql_alchemy_cols)
        # Create all tables
        metadata.create_all()

        for _t in metadata.tables:
            print("Table: ", _t)
        return

if __name__ == "__main__":
    mySQLGenerator = SQLGenerator("mysql+pymysql://root:Helios123@192.168.7.74:3306/customers_info")
    mySQLGenerator.sql_create_table("test_small", "ssn", SQL_SALES_TABLE_CATALOG)
