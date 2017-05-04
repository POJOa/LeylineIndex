from flask import Flask
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from bson.objectid import ObjectId
from flask import request
from pymongo import ReturnDocument
import re
import simplejson as json

app = Flask(__name__)
CORS(app,automatic_options=False)
client = MongoClient('mongodb://localhost:27017/')
db = client.src_index
collection = db.NewSites

@app.route('/sites/<int:page>')
def get(page):
    pagesize = 50
    cursor = collection.find().sort('createdAt',pymongo.ASCENDING).skip(page*50).limit(50)
    count = int(cursor.count() / pagesize)
    res = {"pages":count,"res":cursor}
    return dumps(res)


@app.route('/sites/group/<string:group>/page/<int:page>')
def getByGroup(group,page):
    pagesize = 50
    if(group == '全部'):
        return get(page)
    cursor = collection.find({"groups":group}).sort('createdAt',pymongo.ASCENDING).skip(page*50).limit(50)
    count = int(cursor.count() / pagesize)
    res = {"pages":count,"res":cursor}
    return dumps(res)

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


    if query_owned is not None and query_owned is True:
        findObject['owned'] = True

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
            for i in range(1,len(query_domain)-1):
                regexStr = '\\' + query_domain[i]
                andObj['$and'].append({"url":{'$not' :re.compile(regexStr)}})
            if len(andObj['$and'])>0:
                findObject['$and'].append(andObj)


    if query_keyword is not None:
        orObj = {'$or':[{'title':query['keyword']}
            ,{'url':query['keyword']}
            ,{'meta.description':query['keyword']}
            ,{'meta.keywords':query['keyword']}
            ,{'meta.author':query['keyword']}]}
        if len(orObj['$or'])>0:
            findObject['$and'].append(orObj)

    if len(findObject['$and'])<1:
        del findObject['$and']

    cursor = collection.find(findObject).skip(skip).limit(page_size)
    if query_sort is not None and len(query_sort)>0:
        query_sort_tupple = []
        for e in query_sort:
            for k in e.items():
                query_sort_tupple.append(k)
        query_sort_tupple.append(('owned', pymongo.DESCENDING))
        query_sort_tupple.append(('createdAt', pymongo.DESCENDING))

        cursor = cursor.sort(query_sort_tupple)


    count = int(cursor.count() / page_size)
    res = {"pages":count,"res":cursor}
    return dumps(res)

@app.route('/sites')
def getAll():
    return dumps(collection.find().sort('createdAt',pymongo.ASCENDING))

@app.route('/site/<string:hash>', methods = ['DELETE'])
def delete(hash):
    collection.delete_one({"_id":ObjectId(hash)})
    return 'true'

@app.route('/site/<string:id>', methods = ['POST','OPTIONS'])
def update(id):
    updateInfo = request.get_json()
    try:
        res = dumps(collection.find_one_and_update({'_id':ObjectId(id)},updateInfo,return_document=ReturnDocument.AFTER))
    except Exception as e:
        res = str(e)
    return res


if __name__ == '__main__':
    app.run()
