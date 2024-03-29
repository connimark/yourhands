
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.sql import delete
#import migrate.changeset
#from migrate.changeset.constraint import ForeignKeyConstraint
from sqlalchemy.schema import CreateTable
from sqlalchemy import event, DDL

import sys,os,datetime
import string
import types
import urllib

# the libraries
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
# the models
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../" )))
# the generators
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../" )))

import powlib
from PowBaseObject import PowBaseObject

import generate_model

x = PowBaseObject()

Base = declarative_base(bind=x.__engine__, metadata = x.__metadata__)
Base.metadata.reflect()

class BaseUser(Base):
    #
    # Class: A BaseModelCLass
    #
    __table__ = Base.metadata.tables['users']
    
    pbo = x
    session = None
    t = None
    has_accessor_methods = False
    #__mapper_args__ = {}
    #__mapper__.add_properties({'posts': relationship(con.model.__mapper__)})

    properties_list = []
    modelname = 'User'

    def __init__(self):
        self.session = self.pbo.getSession()
        self.generate_accessor_methods()
        self.t = self.__table__
        self.setup_properties()
    
    def setup_properties(self):
        for elem in self.properties_list:
            modelname = string.capitalize(powlib.singularize(elem))
            rel_model = powlib.load_class(modelname, modelname)
            self.__mapper__.add_properties({ elem : relationship(rel_model.__mapper__) })
        
    def find_by(self, att, val, first=True):
        mstr = "self.session.query(Base" + self.__class__.__name__ +").filter_by(" + str(att) + "=val)"
        if first == True:
            mstr += ".first()"
        print " -- ", mstr
        res= eval(mstr)
        #res.__init__()
        return res

    def find_all(self):
        mstr = "self.session.query(Base" + self.__class__.__name__ + ").all()"
        print " -- ", mstr
        res= eval(mstr)
        #for elem in res:
        #    elem.__init__()
        return res
    
    def find_first(self):
        mstr = "self.session.query(Base" + self.__class__.__name__ + ").first()"
        print " -- ", mstr
        res= eval(mstr)
        #for elem in res:
        #    elem.__init__()
        return res
    
    def will_paginate(page=1, per_page=10):
        res = self.find_all()
        start = page * per_page
        end = (page*per_page)+per_page
        return res[start:end]    
    
    def get(self, name):
        return eval("self.get_"+ str(name)+"()")

    def set(self,name,val):
        #val = urllib.unquote(val)
        #print " -- Model, setting: ", name, " -> ", val, " # ", type(val)
        funcname = "self.set_%s" % (name)
        func = eval(funcname)
        #eval("self.set_"+ str(name)+"(\""+ val + "\")" )
        #statement = "self.%s=u'%s'" % (name,val)
        #exec(statement)
        #print type(func)
        #print func
        func(val)
        return

    def getColumns(self):
        rlist = []
        for col in self.__table__.columns:
            rlist.append( string.split(str(col), ".")[1])
        return rlist

    def getColumn(self, name):
        return eval("self.__table__.c." + name)

    def getName(self):
        return self.__class__.__name__

    def generate_accessor_methods(self):
        #
        # generates the convenient getAttribute() and setAttribute Methods
        # and sets them as accessors for the variable
        mstr = ""
        self.has_accessor_methods = True
        for item in self.__table__.columns:
            #getter
            mstr = ""
            method_name = "get_"+ item.name
            setter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self):" + powlib.newline
            mstr += powlib.tab + "return self." + str(item.name) + powlib.newline
            #print mstr
            exec(mstr)
            self.__dict__[method_name] = types.MethodType(foo,self)
            
            
            # setter
            mstr = ""
            method_name = "set_"+ item.name
            getter = method_name
            tmp_meth_name = "foo"
            mstr +=     "def foo(self, value):" + powlib.newline
            mstr += powlib.tab + "self." + str(item.name) + " = value " + powlib.newline
            #print mstr
            exec(mstr)
            self.__dict__[method_name] = types.MethodType(foo,self)
            
            #cmd_str = "self.__table__." + item + "=property(" + getter + "," + setter + ")"
            #eval(cmd_str)
            
    def generate_find_by( self ):
        pass

    def get_by_name(self, name):
        return eval("self." + str(name))


    def __repr__(self):
        ostr=""
        ostr += str(type(self)) + powlib.newline
        ostr += "-------------------------------" + powlib.newline
        for col in self.__table__.columns:
            ostr += col.name + "-->" + str(self.get(col.name)) + powlib.newline
        return ostr

    def __reprhtml__(self):
        ostr=""
        ostr += str(type(self)) + "<br>"
        ostr += "<hr>"
        for col in self.__table__.columns:
            ostr += col.name + "-->" + str(self.get_by(col.name)) + "<br>"
        return ostr

    def update(self):
        dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
        dt = urllib.unquote(dt)
        self.set("last_updated", dt)
        self.session.merge(self)
        self.session.commit()

    def create(self):
        dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
        #dt = urllib.unquote(dt)
        self.set("created", dt)
        self.set("last_updated", dt)
        self.session.merge(self)
        self.session.commit()

    def delete(self, id):
        s = delete(self.__table__, self.__table__.columns.id==id)
        self.session.execute(s)
        self.session.commit()

    @orm.reconstructor
    def init_on_load(self):
        if self.session == None:
            self.session = self.pbo.getSession()
        if self.has_accessor_methods == False:
            self.generate_accessor_methods()

    def belongs_to(self,rel_table):
        """ Description:
                Creates the foreign_key for the table relation. 
                Remark: The old table is dropped. 
            input parameters:    
                rel_table (type:string) Name of the table to be related.
        """
        #
        # Now creating the foreign_key
        #
        fkey = powlib.pluralize(rel_table) + ".id"
        if fkey in self.__table__.foreign_keys:
            err_msg = " already has a belongs_to relation to table "
            print "Table ", self.__table__.name, err_msg , rel_table
            raise StandardError( "Table " + self.__table__.name +  err_msg +  rel_table)
        else:
            fkey = ""
            #cons = ForeignKeyConstraint([table.c.fkey], [othertable.c.id])
            modelname = string.capitalize(rel_table)
            #print " -- loading model: ", modelname
            rel_model = powlib.load_class(modelname, modelname)
            #col = rel_model.getColumn(self.__table__.name + "_id")
            #print rel_model.getColumns()
            #print str(CreateTable(rel_model.__table__))
            self.__table__.append_column(Column(rel_model.__table__.name + "_id", Integer, ForeignKey(rel_model.__table__.name +".id")))
            cts = str(CreateTable(self.__table__))
            create_table_ddl = DDL(cts)    
            print cts
            self.__table__.drop()
            self.pbo.getConnection().execute(create_table_ddl)
        return

    def release_belongs_to(self,rel_table):
        return

    def release_has_many(self,rel_table, prefix_path="./"):
        
        if rel_table in self.properties_list:
            # remove raltion from the living model
            self.properties_list.remove(rel_table)
            print "properties_list after release_has_many:" , self.properties_list 
            mod = powlib.load_module( "generate_model" )
            # daclaration of render_model: def render_model(modelname, force, comment, properties=None, nomig=False):
            # remove relation from the persistent model
            mod.render_model( str.lower(self.modelname), True, "", prefix_path, str(self.properties_list) )
        else:
            print "Model: ", self.modelname, " has no has_many relation to ", rel_table
        return


    def has_many(self,rel_table, prefix_path="./"):
        """ Description:
                Creates the relation property in the model class text definition.                  
            input parameters:    
                rel_table     (type:string) Name of the table to be related.
                prefix_path   (type:string) The new model code will be generated into
                                            prefix_path/models/ 
        """
        ### has_many property is the plural form of the modelname
        #modelname = string.capitalize(powlib.singularize(rel_table))
        #rel_model = powlib.load_class(modelname, modelname)
        #self.__mapper__.add_properties({rel_table: relationship(rel_model.__mapper__)})
        #generate_model.render_model(modelname, noforce, comment, properties=None):
        #return
        if rel_table in self.properties_list:
            print "Model: ", self.modelname, " already has a has_many relation to ", rel_table
            return
        else:
            self.properties_list.append(rel_table)
            mod = powlib.load_module( "generate_model" )
            # daclaration of render_model: def render_model(modelname, force, comment, properties=None, nomig=False):
            mod.render_model( str.lower(self.modelname), True, "", prefix_path, str(self.properties_list))
            #def render_model(modelname, force, comment, prefix_path, properties=None):
            return
        
if __name__ == "__main__":
    pass