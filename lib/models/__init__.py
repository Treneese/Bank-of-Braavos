import sqlite3
import ipdb
ipdb.set_trace()
sqlite3.connect('bank.db')
CONN = sqlite3.connect('bank.db')
CURSOR = CONN.cursor()