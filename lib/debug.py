#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from account import Account
from client import Client
import ipdb

def reset_database():
    Account.drop_table()
    Client.drop_table()
    Account.create_table()
    Client.create_table()

reset_database()
ipdb.set_trace()