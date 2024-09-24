import urllib
from sqlalchemy import create_engine

server = '6.tcp.us-cal-1.ngrok.io,16731' # to specify an alternate port
database = 'Test' 
username = 'webLogin' 
password = '1234567q'

params = urllib.parse.quote_plus('DSN='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

engine = ("mssql+pyodbc://"+username+":"+password+"@server")
