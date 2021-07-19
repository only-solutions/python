import os
import json
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from pathlib import Path
from collections import namedtuple

UPLOAD_FOLDER = '/home/here/github/python/public-html/uploads'
JSON_DB = '/home/here/github/python/mydb.json'
DB_BACKUP = '/home/here/github/python/backups'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)

def updatedb(category,folder,tags,filenm):
     if os.path.isfile(JSON_DB):
         with open(JSON_DB) as jdb:
             jsondb_dict = json.load(jdb)
     else:
         jsondb_dict={'categories':[],'folders':[],'entries':[]}
     jsoncats = jsondb_dict['categories']
     jsonfolders = jsondb_dict['folders']
     jsoncats.append(category)
     jsonfolders.append(folder)
#use namedtuple to store record
     DBentry = namedtuple('DBentry',('category','folder', 'tags','filename'))
#example using last parameter as named parameter (not required, can be positional)
     newentry = DBentry(category,folder,tags,filename=filenm)
     jsondb_dict['categories'] = list(set(jsoncats))
     jsondb_dict['folders'] = list(set(jsonfolders))
#use _asdict() to make namedtuple into key/value dict format, to be transformed to json
     jsondb_dict['entries'].append(newentry._asdict())
#     print(jsondb_dict)
#      ff=json.loads(json.dumps(list(a))
     with open(JSON_DB, 'w') as jdb:
         json.dump(jsondb_dict, jdb)
     backupdb = get_unique_filename(DB_BACKUP,'dbbackup.json')
     with open(backupdb, 'w') as jdb:
         json.dump(jsondb_dict, jdb)

def updatedborig(category,folder,tags,filenm):
#    {'categories':['storage','pictures'],
#     'folders':['default','box1','jan20'],
#      'entries':[{'category':'storage', 'folder':'default',
#                 'tags':'papers,office','filename':'file1.jpg'},...]}
#    json_entry_dict = ...
     if os.path.isfile(JSON_DB):
         with open(JSON_DB) as jdb:
             jsondb_dict = json.load(jdb)
     else:
         jsondb_dict={'categories':[],'folders':[],'entries':[]}
     jsoncats = jsondb_dict['categories']
     jsonfolders = jsondb_dict['folders']
     jsoncats.append(category)
     jsonfolders.append(folder)
     newentry = {'category':category, 'folder':folder,'tags':tags,'filename':filenm}
     jsondb_dict['categories'] = list(set(jsoncats))
     jsondb_dict['folders'] = list(set(jsonfolders))
     jsondb_dict['entries'].append(newentry)
#     print(jsondb_dict) 
#      ff=json.loads(json.dumps(list(a))
     with open(JSON_DB, 'w') as jdb:
         json.dump(jsondb_dict, jdb)
     backupdb = get_unique_filename(DB_BACKUP,'dbbackup.json')
     with open(backupdb, 'w') as jdb:
         json.dump(jsondb_dict, jdb)
     

@app.route('/favicon.ico') 
def favicon(): 
    return "NOTHING"

def get_unique_filename(checkdir,origfilename):
    try:
        origsuffix = Path(origfilename).suffix
        filenumber=1
        maxfiles=999999
        while filenumber < maxfiles :
            retpath = os.path.join(checkdir,(''.join(['data',str(filenumber),origsuffix])))
            filenumber += 1
            if not os.path.exists(retpath):
                break
        if (filenumber < maxfiles):
            return retpath
        else:
            return '' 
    except Exception as e:
        print('exception: '+str(e))
        return ''
   
@app.route('/post', methods=['GET', 'POST'])
def post():
    try:
        print('entered post1')
        returnstr=''
        if request.method == 'POST' and 'file' in request.files:
            category = request.form['category']
            folder = request.form['folder']
            tags = request.form['tags']
            print('category is: '+category)
            print('folder is: '+folder)
            print('tags is: '+tags)
            fulldir = os.path.join(app.config['UPLOAD_FOLDER'],category,folder)
            if not os.path.exists(fulldir):
                os.makedirs(fulldir)
            returnstr = 'category:' + category + ' folder: '+folder+' tags: '+tags+' filenames:'
            for f in request.files.getlist('file'):
                origfilename = secure_filename(f.filename)
                filename = get_unique_filename(fulldir,origfilename)
                if filename != '':
#                   f.save(os.path.join(app.config['UPLOAD_FOLDER'],location,filename))
                    f.save(filename)
                    updatedb(category,folder,tags,filename)
                    returnstr = returnstr + filename + ','
                else:
                    print('could not upload: '+origfilename)
                    return 'FAIL'
            return 'Files uploaded: '+returnstr
        return redirect(request.url)
    except Exception as e:
        print('exception: '+str(e))
        return 'FAIL'

if __name__ == '__main__':
#    app.run(debug=True,host='192.168.1.8',port='5000')
    app.run(debug=True,host='localhost',port='5000')

