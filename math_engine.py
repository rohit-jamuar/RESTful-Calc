#!/usr/bin/python

from flask import Flask, request, jsonify
from datetime import datetime
from time import mktime
from cPickle import load, dump
from os.path import isfile

APP = Flask(__name__)

DATA_STORE = []
if isfile('stored.data'):
    DATA_STORE = load(open('stored.data', 'rb'))

def get_minute_diff(t_1, t_2):
    '''
    Returns the time-difference (in minutes) between two datetime objects
    '''
    for time_obj in [t_1, t_2]:
        if type(time_obj) != datetime:
            return False
    t_1 = mktime(t_1.timetuple())
    t_2 = mktime(t_2.timetuple())
    return (t_2 - t_1) / 60

@APP.route('/api', methods = ['POST'])
def compute():
    '''
    The API endpoint with which the user interacts to get sum and
    product of list of numbers passed (as arguments in POST request).
    '''
    if u'values' in request.json:
        current_sum, current_product = 0, 1
        for item in request.json[u'values']:
            if type(item) != int:
                return jsonify({'Error' : 'All the items must be integers!'})
            else:
                current_sum += item
                current_product *= item
        
        DATA_STORE.append( { "ip" : "%s"%request.remote_addr, 
            "timestamp" : datetime.now(), 
            "sum" : current_sum, "product" : current_product,
            "values" :  request.json[u'values'] } )

        dump(DATA_STORE, open('stored.data', 'wb'))
        return jsonify({'sum' : current_sum, 'product' : current_product})
    else:
        return jsonify({'Error' : 'Values not passed!'})

@APP.route('/get_stored', methods = ['POST'])
def get_stored_data():
    '''
    The API endpoint which returns a list of previous responses, which have a 
    timestamp greater than 'minutes', w.r.t current time -  this parameter is
    passed by user along with the POST request.
    '''
    if u'minutes' in request.json:
        minutes = request.json[u'minutes']
        if type(minutes) == int and minutes >= 0:
            t_now = datetime.now()
            final = []
            for stored_q in DATA_STORE:
                t_stored = stored_q['timestamp']
                diff_result = get_minute_diff(t_stored, t_now)
                if diff_result:
                    if diff_result >= minutes:
                        temp = {}
                        for key in stored_q:
                            if key != "timestamp":
                                temp[key] = stored_q[key]
                            else:
                                temp[key] = stored_q[key].strftime("%m-%d-%YT%H:%M:%S")
                        final.append(temp)
                    else:
                        break
                else:
                    return jsonify({'Error' : 'Invalid datetime object passed'})
            return jsonify({'Response' : final})
        else:
            return jsonify({'Error' : '"minutes" passed improperly!'})
    else:
        return jsonify({'Error' : '"minutes" not passed!'})

if __name__ == '__main__':
    APP.run(debug = True)
