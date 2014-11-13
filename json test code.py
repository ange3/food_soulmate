import json
from pprint import pprint

def load_data(file, data):
    infile = open(file, 'r')
    data = json.load(infile)
    pprint(data[0])
    infile.close()
    return data
    # http://stackoverflow.com/questions/11279331/what-does-the-u-symbol-mean-in-front-of-string-values
    
user_data = []
user_data = load_data('yelp_academic_dataset_user_comma_friends_only.json', user_data)
#print user_data[5]



#user_infile = open('yelp_academic_dataset_user_comma.json', 'r')
#
#user_data = json.load(user_infile)
#
#while True:
#    currline = user_infile.readline()
#    if not currline: #eof reached
#        break
#    print currline    
#    user_data.append(json.loads(currline))
#    
#pprint(user_data)
#user_infile.close()