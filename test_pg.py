from config.credentials import get_auth_credentials
from utils.pg_utils import PgPersistence


test_row = ['uno','dos','tres']
auth_dict = get_auth_credentials()
pg = PgPersistence(auth_dict)
pg.insert_row(test_row)
