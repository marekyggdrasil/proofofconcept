#!/opt/local/bin/python
# Physics Equation Graph
# Ben Payne <ben.is.located@gmail.com>
# builds the JSON for d3js
# use: python bin/build_connections_JSON.py

# files required as input: 
#    lib_physics_graph.py
#    connections_database.csv
# output: 

# current bugs:

import random
#import re # regular expressions
#import subprocess
#import yaml # used to read "config.input"
import os.path
import sys
lib_path = os.path.abspath('lib')
db_path = os.path.abspath('databases')
output_path = os.path.abspath('output')
sys.path.append(lib_path) # this has to proceed use of physgraph

import lib_physics_graph as physgraf

expressionsDB=db_path+'/expressions_database.csv'
connectionsDB=db_path+'/connections_database.csv'
feedDB       =db_path+'/feed_database.csv'
infruleDB    =db_path+'/inference_rules_database.csv'

expressions_list_of_dics=physgraf.convert_expressions_csv_to_list_of_dics(expressionsDB)
feeds_list_of_dics=physgraf.convert_feed_csv_to_list_of_dics(feedDB)
connections_list_of_dics=physgraf.convert_connections_csv_to_list_of_dics(connectionsDB)
infrule_list_of_dics=physgraf.convert_infrule_csv_to_list_of_dics(infruleDB)

list_of_infrules=[]
for this_infrule in infrule_list_of_dics:
  list_of_infrules.append(this_infrule["inference rule"])

list_of_expr=[]
for this_expr in expressions_list_of_dics:
  list_of_expr.append(this_expr["permanent index"])

list_of_feeds=[]
for this_feed in feeds_list_of_dics:
  list_of_feeds.append(this_feed["temp index"])

[connection_feeds,connection_expr_perm,connection_expr_temp,\
connection_infrules,connection_infrule_temp]=\
physgraf.separate_connection_lists(connections_list_of_dics)


expr_perm_indx=physgraf.find_new_indx(list_of_expr,1000000000,9999999999,"expression permanent index: ")
feed_temp_indx=physgraf.find_new_indx(list_of_feeds,1000000,9999999,"feed temporary index: ")
expr_temp_indx=physgraf.find_new_indx(connection_expr_temp,1000000,9999999,"expression temporary index: ")
infrule_temp_indx=physgraf.find_new_indx(connection_infrule_temp,1000000,9999999,"inf rule temp indx")

print('expression permanent index: '+str(expr_perm_indx))
print('expression temporary index: '+str(expr_temp_indx))
print('feed temporary index      : '+str(feed_temp_indx))
print('inf rule temporary index  : '+str(infrule_temp_indx))

physgraf.find_duplicates(list_of_infrules,"inference rules")
physgraf.find_duplicates(list_of_expr,"expressions")
physgraf.find_duplicates(list_of_feeds,"feeds")

physgraf.find_mismatches(connection_feeds,list_of_feeds,connection_expr_perm,\
                    list_of_expr,connection_infrules,list_of_infrules)

physgraf.check_connection_DB_steps_for_single_inf_rule(connections_list_of_dics)
