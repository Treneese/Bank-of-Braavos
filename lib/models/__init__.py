import sqlite3
import ipdb
ipdb.set_trace()
sqlite3.connect('lib/bank.db')
CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()