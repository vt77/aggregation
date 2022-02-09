import os,sys

from flask import Flask
from flask import jsonify,request
import gevent
from gevent import monkey
monkey.patch_all()

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir + "/lib")

from response import Response,Message
from aggregation.aggregator import DomainAggregator
from domains import processor as domianprocessor
from storage import storage

app = Flask(__name__)
#CORS(app)


from serilizer.json import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder

domains = domianprocessor(storage)

aggregations = {
    'min' : DomainAggregator(10,60),
    'hour' : DomainAggregator(10,3600),
}

@app.route('/domains/<aggregation_type>',methods = ['GET'])
def aggregation_get(aggregation_type):
    logger.info("[API]Getting top domains list for %s" % aggregation_type)
    if aggregation_type not in aggregations:
        return jsonify( 
                    Response( Message("Aggregation not found"), Response.ERROR) )    
    return jsonify( Response(aggregations[aggregation_type]) ) 

@app.route('/domains',methods = ['POST'])
def aggregation_post():
    domains_data = request.json
    logger.debug("[API]Process append request  %s" % domains_data )    
    timestamp = domains_data.pop('timestamp',None)
    if ( timestamp is None )  or ( not isinstance(timestamp,int) ):
        return jsonify( Response(
                            Message("Bad timestamp value"),
                            Response.ERROR) )
    for d,v in domains_data.items():
        logger.debug("[API]Add domain stats : %s => %s" % (d,v))
        domains.add(timestamp,d,v)

    return jsonify( Response( Message("OK") ) )
     
@app.route('/')
def index():
    return app.send_static_file('swaggerui.html')

@app.route('/openapi.js')
def openapi():
    return app.send_static_file('openapi.js')

@app.route('/readme')
def readme():
    return app.send_static_file('readme.html')


"""
    Green thread process to rebuild aggregation
    It can be thread / process as well if number of data big enough
"""

def aggregation_processor():
    while True:
        for k,a in aggregations.items():
            if a.want_rebuild():
                logger.debug("[APP]Rebuild aggregation %s" % k )
                "Use 10 seconds window to not loose corner entry"
                a.rebuild(domains.get(period=a.period + 10))
                logger.debug("[APP][%s]Top domains %s" % (k,dict(a)) )
        # Sleep one second
        gevent.sleep(1)

gevent.Greenlet.spawn(aggregation_processor)