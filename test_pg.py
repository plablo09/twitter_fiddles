from config.credentials import get_auth_credentials
from utils.pg_utils import PgPersistence
import time
from datetime import datetime

date_string = "10/27/2014 17:55:33"
ts = datetime.fromtimestamp(time.mktime(time.strptime(date_string,'%m/%f/%Y %H:%M:%S')))
coordinates = (-99.184835, 19.314062)
auth_dict = get_auth_credentials()
test_row = ['user','text',ts,coordinates]
pg = PgPersistence(auth_dict)
pg.insert_row(test_row)
