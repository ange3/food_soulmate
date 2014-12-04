import json

def loadJSON(fileName):
  user_data = []
  infile = open(fileName, 'r')
  data = json.load(infile)
  infile.close()
  return data 