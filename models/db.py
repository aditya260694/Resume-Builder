# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'resumebuilder63@gmail.com'
mail.settings.login = 'resumebuilder63:4321tiii'

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

#request.requires_https()

db.define_table('details',
		db.Field('myid','integer',writable=False,readable=False),#default='auth.user_id'),
		db.Field('name','string',writable=False,readable=False),
		db.Field('current_year','string',requires=IS_IN_SET(['1st','2nd','3rd','4th','5th']),notnull=True),
		db.Field('cg','float',requires = IS_FLOAT_IN_RANGE(0, 10, dot=".",error_message='CG must be between 0 - 10'),label='Current CG',comment='(on a scale of 10)',notnull=True),
		db.Field('college','string',label='College Name',notnull=True),
		db.Field('branch','string',requires=IS_IN_SET(['CSE','ECE','CSD','ECD','CLD','CND','EHD']),notnull=True),
		db.Field('address','string'),
		db.Field('city','string'),
		db.Field('cstate','string',label='State'),		#check for resume upload v/s creation & provide radios and appropriate page loading.
		db.Field('picture','upload',autodelete=True,label='Picture of yourself',comment='(Optional)',default='photo.jpg'),
		db.Field('resume','upload',autodelete=True,label='Your Resume',comment='(Optional)')
		)
		
db.define_table('msg',
        db.Field('msg_date','date',writable=False,default=request.now,label='Date'),
        db.Field('sender','string',writable=False,readable=False),
        db.Field('name',requires=IS_IN_DB(db,'details.id','details.name'),notnull=True,label='To'),
        db.Field('sub','string',label='Subject'),
        db.Field('msg','text',notnull=True,label='Message'))
        
db.define_table('project',
        db.Field('myid','integer',writable=False,readable=False),
        db.Field('name','string',notnull=True),
        db.Field('org','string',notnull=True,label='Organisation'),
        db.Field('mentor','string'),
        db.Field('Description','text'),
        db.Field('skills_used','text',notnull=True),
        db.Field('relevant_links','string',requires=IS_URL()),
        db.Field('project_upload','upload'))
        
db.define_table('organisation',
        db.Field('myid','integer',writable=False,readable=False),
        db.Field('name','string',writable=False,readable=False,notnull=True),
        db.Field('logo','upload',label='Company Logo',notnull=True),
        db.Field('about','text',notnull=True))
        
db.define_table('vacancies',
        db.Field('myid','integer',writable=False,readable=False),
        db.Field('post','string',notnull=True),
        db.Field('description','text',),
        db.Field('requirements','string'),
        db.Field('docs','upload',label='Relevant Document'),
        db.Field('compid','integer',readable=False,writable=False))

db.define_table('achievements',
                db.Field('ctg','string',label='Category',requires=IS_IN_SET(['Academic','ExtraCurricular'])),
                db.Field('myid','integer',writable=False,readable=False),
                db.Field('what','text',label='Describe your achievement'))
                
                

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)
