import pyodbc
import urllib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


server = 'analyticalandnosql.database.windows.net'
database = 'nulplabssql'
username = 'olichkakr'
password = 'Olichka121'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()