
EVAL_NETWORK_FILE = 'eval_ntwk_edge_list_1000.txt'
FOOD_NETWORK_FILE = 'food_ntwk_edge_list_1000.txt'

evalFile = open(EVAL_NETWORK_FILE, "r")
foodFile = open(FOOD_NETWORK_FILE, "r")

for line in foodFile:
  arr = line.split()
  arr[0]