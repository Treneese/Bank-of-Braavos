#!/usr/bin/env python3
# lib/debug.py
from models.__init__ import CONN, CURSOR
from models.account import Account
from models.client import Client
import ipdb
ipdb.set_trace()
def reset_database():
    Account.drop_table()
    Client.drop_table()
    Account.create_table()
    Client.create_table()
                
arya = Client.create( "Arya Stark", "123 main", 19981019, "arya.stark@gmail.com", "123452232", 84039, "770", "284927493")
john = Client.create( "John Snow", "324 grove", 19881125, "john.snow@gmail.com", "273025389", 44000, "650", "3759837593")
acc1 = Account.create( "375926486374", "639505725", "Saving", "1200")
acc2 = Account.create( "275936254860", "275967255", "Checking", "385")


#reset_database()
