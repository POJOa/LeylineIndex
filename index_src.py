#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import re
import requests as r
import simplejson as json
import dns.resolver
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import Response
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from secret import get_secret
from tld import get_tld
import datetime
from flask_bcrypt import Bcrypt


from flask_jwt_extended import JWTManager, jwt_required,\
    create_access_token, get_jwt_identity

app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)

app.secret_key = get_secret()
jwt = JWTManager(app)

CORS(app,automatic_options=False)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=365)
client = MongoClient('mongodb://localhost:27017/')
db = client.src_index
site_collection = db.NewSites
user_collection = db.Users

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def toBeReplacedWithNGinx(path):
    return app.send_static_file(path)

@app.route('/sites/search', methods = ['POST'])
def hybridSearch():
    findObject = {}

    query = request.get_json()
    query_page_size = query.get('page_size')
    query_page = query.get('page')
    query_groups = query.get('groups')
    query_owned = query.get('owned')
    query_domain = query.get('domain')
    query_keyword = query.get('keyword')
    query_sort = query.get('sort')


    if query_page_size is None or query_page_size<=0 :
        page_size = 50
    else :
        page_size = query_page_size

    if query_page is None or query_page<0 :
        page = 0
    else :
        page = query['page']

    skip = page_size * page

    if query_groups is not None and query_groups!='全部':
        findObject['groups'] = query_groups


    if query_owned is not None:
        if type(query_owned) is bool:
            findObject['owned'] = {"$exists":query_owned}
        else:
            findObject['owned'] = query_owned


    findObject['$and'] = []
    if query_domain is not None:
        if query_domain[0] != u'others':
            orObj = {'$or':[]}
            for suffix in query_domain:
                orObj['$or'].append({"url":{"$regex":'\\'+suffix}})
            if len(orObj['$or'])>0:
                findObject['$and'].append(orObj)
        else:
            andObj = {'$and':[]}
            for i in range(1,len(query_domain)):
                regexStr = '\\' + query_domain[i]
                andObj['$and'].append({"url":{'$not' :re.compile(regexStr)}})
            if len(andObj['$and'])>0:
                findObject['$and'].append(andObj)


    if query_keyword is not None:
        regex = {"$regex":'.*'+query_keyword+'.*'}
        orObj = {'$or':[{'title':regex}
            ,{'url':regex}
            ,{'meta.description':regex}
            ,{'meta.keywords':regex}
            ,{'meta.author':regex}]}
        if len(orObj['$or'])>0:
            findObject['$and'].append(orObj)

    if len(findObject['$and'])<1:
        del findObject['$and']

    cursor = site_collection.find(findObject).skip(skip).limit(page_size)

    if query_sort is not None and len(query_sort)>0:
        query_sort_tupple = []
        query_sort_tupple.append(('owned', pymongo.DESCENDING))
        for e in query_sort:
            for k in e.items():
                query_sort_tupple.append(k)

        cursor = cursor.sort(query_sort_tupple)
    else:
        cursor = cursor.sort('owned',pymongo.DESCENDING)



    count = int(cursor.count() / page_size)
    res = {"pages":count,"res":cursor}
    return dumps(res)

@app.route('/site/<string:hash>', methods = ['DELETE'])
def delete(hash):
    site_collection.delete_one({"_id":ObjectId(hash)})
    return 'true'

@app.route('/site/<string:id>', methods = ['POST'])
def update(id):
    updateInfo = request.get_json()
    try:
        res = dumps(site_collection.find_one_and_update({'_id':ObjectId(id)},updateInfo,return_document=ReturnDocument.AFTER))
    except Exception as e:
        res = str(e)
    return res

@app.route('/owned/phase2/<string:url>/add', methods = ['POST'])
@jwt_required
def add(url):
    current_user = get_jwt_identity()
    site = request.json

    try:
        urlWithHTTP = 'http://'+url
        rootDomain = get_tld(urlWithHTTP)
        res = r.get(urlWithHTTP)
        res.raise_for_status()
        existed = site_collection.find({"url": {"$regex": rootDomain}})
        if len(existed) > 0:
            for e in existed:
                if (get_tld(e['url']) == rootDomain):
                    return '{"err":true}'
    except:
        return '{"err":true}'


    if len(url.split('/'))<2:
        new_site = {
            "url":url,
            "valid":False,
            "createdAt": datetime.now(),
            "owned":current_user
        }
        try:
            res = dumps(site_collection.insert(new_site))
            return res
        except Exception as e:
            return '{"err":true}'
    return '{"err":true}'

@app.route('/owned/phase3', methods = ['POST'])
@jwt_required
def phase3():
    current_user = get_jwt_identity()
    site = request.json

    try:
        site_entity = site_collection.find_one({"_id":ObjectId(site.get('_id').get('$oid'))})
        owner = site_entity['owned']
        if owner != current_user:
            return '{"err":true}'
        site_entity['thumb'] = site.get('thumb')
        site_entity['friendsPage'] = site.get('friendsPage')
        site_entity['groups'] = site.get('groups')
        user_collection.find_one_and_update({"_id":ObjectId(current_user)},{"$set":{"snsInfo":site.get('snsInfo')}},
                                                            return_document=ReturnDocument.AFTER)
        return dumps(site_collection.update({"_id":ObjectId(site.get('_id').get('$oid'))},site_entity))

    except Exception as e:
        return '{"err":true}'


@app.route('/owned/phase2/<string:id>/claim', methods = ['GET'])
@jwt_required
def phase2claim(id):
    try:
        res = {}
        res['veriToken'] = get_jwt_identity()
        expected = site_collection.find_one({"_id":ObjectId(id)})
        res['veriDomain'] = get_tld(expected['url'])
        res['veriSiteId'] = expected['_id']
        return dumps(res)
    except:
        return '{"err":true}'


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    expected = user_collection.find_one({"username":username})

    if expected is None or not bcrypt.check_password_hash(expected['password'],password):
        return json.dumps({"msg": "Bad username or password"}), 401

    userId = str(expected['_id'])

    # Identity can be any data that is json serializable
    ret = {'access_token': create_access_token(identity=userId)}
    return json.dumps(ret), 200

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token
@app.route('/owned/<string:id>/file', methods=['GET'])
@jwt_required

def checkOwnedFile(id):
    current_user = get_jwt_identity()
    site = site_collection.find_one({"_id":ObjectId(id)})
    owned = False
    if site is not None:
        try:
            res = r.get('http://'+get_tld(site['url'])+'/'+current_user+'.txt')
            if current_user in res.text:
                owned = True
        except:
            try:
                res = r.get('http://www.'+get_tld(site['url'])+'/'+current_user+'.txt')
                if current_user in res.text:
                    owned = True
            except:
                try:
                    res = r.get('http://blog.'+get_tld(site['url'])+'/'+current_user+'.txt')
                    if current_user in res.text:
                        owned = False
                    else:
                        owned = False
                except:
                    owned = False
        if(owned):

            res = dumps(site_collection.find_one_and_update({'_id': ObjectId(id)}, {"$set":{"owned":current_user}},
                                                            return_document=ReturnDocument.AFTER))
            return res
        else:
            return '{"err":true}'

@app.route('/owned/gen', methods=['GET'])
@jwt_required
def genTxt():
    current_user = get_jwt_identity()
    return Response(current_user,
                    mimetype="text/plain",
                    headers={"Content-Disposition":
                                 "attachment;filename="+current_user+".txt"})


@app.route('/owned/<string:id>/cname', methods=['GET'])
@jwt_required
def checkOwned(id):
    try:
        current_user = get_jwt_identity()
        site = site_collection.find_one({"_id":ObjectId(id)})
        url = current_user+'.'+get_tld(site['url'])
        cname = dns.resolver.query(url, 'CNAME')
        owned = False
        for i in cname.response.answer:
            for j in i.items:
                if 'leyline.cc' in j.to_text():
                    owned = True
                    break
        if (owned):
            res = dumps(site_collection.find_one_and_update({'_id': ObjectId(id)}, {"$set": {"owned": current_user}},
                                                            return_document=ReturnDocument.AFTER))
            return res
        else:
            return '{"err":true}'
    except:
        return '{"err":true}'


@app.route('/like/<string:id>', methods=['GET'])
@jwt_required
def like(id):
    current_user = get_jwt_identity()
    site = site_collection.find_one({"_id":ObjectId(id)})
    if site is not None:
        res = dumps(user_collection.find_one_and_update({'_id': ObjectId(current_user)},{"$push":{"liked":[site['_id']]}},
                                                        return_document=ReturnDocument.AFTER))
        return res
    return '{"err":true}'

@app.route('/follow/<string:id>', methods=['GET'])
@jwt_required
def follow(id):
    current_user = get_jwt_identity()
    user_to_follow = user_collection.find_one({"_id":ObjectId(id)})
    if user_to_follow is not None:
        res = dumps(user_collection.find_one_and_update({'_id': ObjectId(current_user)},{"$push":{"following":[user_to_follow['_id']]}},
                                                        return_document=ReturnDocument.AFTER))
        return res
    return '{"err":true}'

@app.route('/owned/<string:id>/meta', methods=['GET'])
@jwt_required
def checkOwnedMeta(id):
    current_user = get_jwt_identity()
    site = site_collection.find_one({"_id":ObjectId(id)})

    url = "http://"+get_tld(site['url'])
    urlWithWWW = "http://www."+get_tld(site['url'])
    urlWithBlog = "http://blog."+get_tld(site['url'])

    try:
        res = r.get(url)
    except:
        try:
            res = r.get(urlWithWWW)
        except:
            try:
                res = r.get(urlWithBlog)
            except:
                return '{"err":true}'

    soup = BeautifulSoup(res.text, "lxml")

    meta = soup.find("meta", {"name":"leyline-verify"})

    if meta is not None and meta.get('content') is not None and current_user in meta.get('content'):
        res = dumps(site_collection.find_one_and_update({'_id': ObjectId(id)}, {"$set": {"owned": current_user}},
                                                        return_document=ReturnDocument.AFTER))
        return res
    else:
        return '{"err":true}'



@app.route('/reg', methods=['POST'])
def reg():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if checkNameExists(username):
        return '{"err":true}',403
    else:
        pw_hash = bcrypt.generate_password_hash(password)
        res = user_collection.insert({"username":username,"password":pw_hash})
        return dumps(res),200

@app.route('/reg/exists/<string:username>', methods=['GET'])
def checkNameExists(username):
    expected = user_collection.find_one({"username": username})
    return expected is not None


@app.route('/users/<string:id>', methods=['GET'])
def getUser(id):
    expected = user_collection.find_one({"_id": ObjectId(id)},{"password":0})
    return dumps(expected)

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return json.dumps({'hello_from': current_user}), 200


if __name__ == '__main__':
    app.run()
