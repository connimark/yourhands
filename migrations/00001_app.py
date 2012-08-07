#
#
# This file was autogenerated by python_on_wheels.
# But YOU CAN EDIT THIS FILE SAFELY
# It will not be overwtitten by python_on_wheels
# unless you force it with the -f or --force option
# 


# date created: 	2012-07-10

from sqlalchemy import *
from sqlalchemy.schema import CreateTable
from sqlalchemy import event, DDL

import sys
import os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
import powlib
from PowTable import PowTable
from BaseMigration import BaseMigration

class Migration(BaseMigration):
    table_name="apps"
    table = None
        
    def up(self):
            #
            # here is where you define your table (Format see example below)
            # the columns below are just examples.
            # Remember that PoW automatically adds an id and a timestamp column (ID,TIMESTAMP)
        self.table = PowTable(self.table_name, self.__metadata__,
            
            Column('currentversion', Integer ),
            Column('name', String(50)),
            Column('path', String(50)),
            Column('maxversion', Integer )
            
            #Column('user_id', Integer, ForeignKey('users.id'))
        )
        self.create_table()
        #print CreateTable(self.table)
        
    def down(self):
        self.drop_table()