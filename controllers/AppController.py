#
#
# DO NOT EDIT THIS FILE.
# This file was autogenerated by python_on_wheels.
# Any manual edits may be overwritten without notification.
#
# 

# date created:     2011-06-21

import sys
import os
from mako.template import Template
from mako.lookup import TemplateLookup
import datetime

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models/powmodels" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../controllers" )) )

import powlib
from powlib import uc
import PowObject
import BaseController
import datetime


class AppController(BaseController.BaseController):
    
    def __init__(self):
        self.modelname = "App"
        BaseController.BaseController.__init__(self)
        self.login_required = []
        self.locked_actions = [ "do_login"]
    
    def ajax( self, powdict ):
        print "AJAX-Request"
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        ret_str = uc("""<div class="alert alert-success">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                <strong>Yeah! AJAX with python rocks totally now:</strong>&nbsp %s &nbsp; %s 
              </div>""" % (now, powdict["REQ_BODY"] ))
        return ret_str 
        
    
    def welcome( self,powdict ):
        #return self.render(special_tmpl="hero.tmpl",model=self.model, powdict=powdict)
        return self.render(model=self.model, powdict=powdict)
        
    def thanks( self,powdict ):
        return self.render(model=self.model, powdict=powdict)
        
    def howto_start( self,powdict ):
        return self.render(model=self.model, powdict=powdict)
    
    def login( self, powdict):
        self.model.__init__()
        return self.render(model=self.model, powdict=powdict)
    
    def do_login( self, powdict ):
        user = User.User()
        session = powdict["SESSION"]
        if powdict["REQ_PARAMETERS"].has_key("loginname") and powdict["REQ_PARAMETERS"].has_key("password"):
            try:
                user = user.find_by("loginname",powdict["REQ_PARAMETERS"]["loginname"])
                if user.password == powdict["REQ_PARAMETERS"]["password"]:
                    #login ok
                    session["user.id"] = user.id
                    session["user.loginname"] = user.loginname
                    session.save()
                    powdict["FLASHTEXT"] = "You successfully logged in, %s " % (user.loginname)
                    powdict["FLASHTYPE"] = "success"
                    return self.redirect("welcome",powdict=powdict)
                else:
                    powdict["FLASHTEXT"] = "Error logging you in, %s " % (user.loginname)
                    powdict["FLASHTYPE"] = "error"
                    return self.redirect("login",powdict=powdict)
            except:
                powdict["FLASHTEXT"] = "Error logging you in " 
                powdict["FLASHTYPE"] = "error"
                return self.redirect("login", powdict=powdict)
        else:
            powdict["FLASHTEXT"] = "Error logging you in. You have to fill in username and password. " 
            powdict["FLASHTYPE"] = "error"
            return self.redirect("login", powdict=powdict)
        return
    
    def logout( self, powdict):
        session = powdict["SESSION"]
        session["user.id"] = 0
        session.save()
        return self.redirect("welcome", powdict=powdict)
        
    
