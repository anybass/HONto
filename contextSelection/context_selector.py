# -*- coding: utf8 -*-
import requests
import json
from collections import defaultdict
from py2neo import Graph,  Record,  NodeMatcher, RelationshipMatcher


def iter2list(pythonic_iterator):
    """
    Converts a neo4j.util.PythonicIterator to a list.
    """
    return [item for item in pythonic_iterator]


db = Graph("http://localhost:7474/db/data/", username="neo4j", password="neo4j")
elastic_url = 'http://localhost:9200/default-index-node/_search?scroll=3m'
scroll_api_url = 'http://localhost:9200/_search/scroll'
headers = {'Content-Type': 'application/json'}
result=[]


print("Please type in a reference query.")
args=input().split()
must_conditions=[]
must_conditions_fuzzy=[]

# First, use exact match query
for a in range(len(args)):
    must_conditions.append({'match': {'fieldstring': args[a] }})
query = {'size' : 3000,
  'query':
      {'bool':
           {'must':
                 must_conditions
            }}}
print(query)
r1 = requests.request(
    "POST",
    elastic_url,
    data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
    headers=headers
)

# If there are no exact matches, use fuzzy string matching
for a in range(len(args)):
    must_conditions_fuzzy.append({'fuzzy': {'fieldstring': args[a] }})
query_fuzzy = {'size' : 3000,
  'query':
      {'bool':
           {'must':
                 must_conditions_fuzzy
            }}}
print(query)
r1 = requests.request(
    "POST",
    elastic_url,
    data=json.dumps(query, ensure_ascii=False).encode("utf-8"),
    headers=headers
)

r2 = requests.request(
    "POST",
    elastic_url,
    data=json.dumps(query_fuzzy, ensure_ascii=False).encode("utf-8"),
    headers=headers
)
# first batch data
try:
    res_json = r1.json()
    print ("here")
    data = res_json['hits']['hits']
    _scroll_id = res_json['_scroll_id']
except KeyError:
    data = []
    _scroll_id = None
    print('Error: Elastic Search: %s' % str(r1.json()))
    pass
#print(len(data))
if len(data) == 0:
    print("No results found with exact match. Try to loosen match condition (irrelevant results may appear) Ok? y / n ")
    answer=input()
    if answer == "y":
        try:
            res_json = r2.json()
            data = res_json['hits']['hits']
            _scroll_id = res_json['_scroll_id']
        except KeyError:
            data = []
            _scroll_id = None
            print('Error: Elastic Search: %s' % str(r2.json()))
    else:
        print("No results found with exact match. Program will terminate.")
        exit()
result_no_dict = defaultdict(list)
while data:
    #print(data)
    result=data
# scroll to get next batch data
    scroll_payload = json.dumps({
        'scroll': '3m',
        'scroll_id': _scroll_id
    })
    scroll_res = requests.request(
        "POST", scroll_api_url,
        data=scroll_payload,
        headers=headers
    )
    try:
        res_json = scroll_res.json()
        data = res_json['hits']['hits']
        _scroll_id = res_json['_scroll_id']

    except KeyError:
        data = []
        _scroll_id = None
        err_msg = 'Error: Elastic Search Scroll: %s'
        print(err_msg % str(scroll_res.json()))

    print("resulting contexts:")

    # Show properties from reference node
    for i, r in enumerate(result):
        if r["_source"]["type"]=="Reference":
            #print(r["_source"].keys())
            result_no = i
            result_no_dict[i].append(id)
            id=r["_source"]["id"]
            print()
            #print("id")
            #print(id)
            print("Result No: "+ str(result_no) + ", " +r["_source"]["fieldstring"] )
            try:
                print("reason for citing: " + r["_source"]["property_1"]+", " +r["_source"]["property_2"])
            except KeyError:
                print("reason for citing: "  + r["_source"]["property_2"])
                pass


            # Now connect to graph db neo4j and traverse the tree to the top level to show higher abstraction levels
            try:

                n1 = db.nodes.match("Node", id=id).first()
                result_no_dict[i].append(n1)
                #print(n1)
                fs1=n1['fieldstring']
                #print(fs1)
                rfc = list(db.relationships.match((n1, None), r_type="partOf"))[0]["TARGET"]
                n2=db.nodes.match("Node", id=rfc).first()
                #print("n2")
                #print(n2)
                result_no_dict[i].append(n2)
               # print(n2)
                fs2 = n2['fieldstring']
              #  print(fs2)
                l1 = list(db.relationships.match((n2, None), r_type="partOf"))[0]["TARGET"]
                n3 = db.nodes.match("Node", id=l1).first()
                result_no_dict[i].append(n3)
              #  print(n3)
                fs3 = n3['fieldstring']
               # print(fs3)
                l2 = list(db.relationships.match((n3, None), r_type="partOf"))[0]["TARGET"]
                n4 = db.nodes.match("Node", id=l2).first()
                result_no_dict[i].append(n4)
               # print(n4)
                fs4 = n4['fieldstring']
                #print(fs4)
                l3 = list(db.relationships.match((n4, None), r_type="partOf"))[0]["TARGET"]
                n5 = db.nodes.match("Node", id=l3).first()
                result_no_dict[i].append(n5)
               # print(n5)
                fs5 = n5['fieldstring']
              #  print(fs5)
                l4 = list(db.relationships.match((n5, None), r_type="partOf"))[0]["TARGET"]
                n6 = db.nodes.match("Node", id=l4).first()
                result_no_dict[i].append(n6)
                # print(n6)
                fs6 = n6['fieldstring']
                #  print(fs6)
                l5 = list(db.relationships.match((n6, None), r_type="partOf"))[0]["TARGET"]
                n7 =db.nodes.match("Node", id=l5).first()
                result_no_dict[i].append(n7)
                # print(n6)
                fs7 = n7['fieldstring']
                #  print(fs6)
                print("Context by level of abstration: ")
                print("1: " + fs1 )#+ " " + str(n1))
                print("2: " +fs2)#+ " " + str(n2))
                print("3: " +fs3)#+ " " + str(n3))
                print("4: " +fs4)#+ " " + str(n4))
                print("5: " +fs5)#+ " " + str(n5))
                print("6: " +fs6)#+ " " + str(n6))
                print("7: " + fs7)  # + " " + str(n6))


               # q = 'start n=node(*) MATCH (n:Node)-[r:partOf]->(m:Node) WHERE n.id=11113 RETURN n, r'
                #results = db.query(q,  )
                #print(results.rows)

                ''' n1 = db.nodes.get(11097)
                print(n1)
                fs1 = n1['fieldstring']
                #  print(fs1)
                rfc = n1.traverse(types=[client.Outgoing.partOf])
                n2 = rfc[0]
                print(n2)'''
            except Exception as e:
                print(e)
                pass

    print("Would you like to get linked contexts? If yes, please type in one result number and the desired level of abstraction, for example '5 4' for result number 5 and all linked nodes starting from level 4.")
    res_num= input().split()
    #print(result_no_dict[12])
    #print(res_num[0])

    context=result_no_dict[int(res_num[0])]
    #print(context)
    print("context_node")
    context_node =  db.nodes.match("Node", id=context[0]).first()
    print(context_node)
    #node_id = db.nodes.get(context_node)["_source"]["id"]
    level = context[int(res_num[1])]
    print("level")
    print(level)
    print(level["id"])
    # how we name id in csv, we do not use internal ones
    print("You chose external node: " + str(context_node["id"]) + " with string: " + context_node["fieldstring"] + " and you start with node: " + level["fieldstring"])#)
    print("Starting to find linked incoming nodes now...")

    inc1=list(db.relationships.match((None, level), r_type="partOf"))

    try:
        for i in range(len(inc1)):

            nd1=db.nodes.match("Node", id=inc1[i]["SOURCE"]).first()
            print("1: "+ nd1["fieldstring"] + " at: "+ nd1["id"])
            inc2=list(db.relationships.match((None, nd1), r_type="partOf"))
            #print(inc2)
            if inc2:
                for j in range(len(inc2)):
                    nd2=db.nodes.match("Node", id=inc2[j]["SOURCE"]).first()
                    print("2: " + nd2["fieldstring"] + " at: " + nd2["id"])
                    inc3=list(db.relationships.match((None, nd2), r_type="partOf"))
                    if inc3:
                        for k in range(len(inc3)):
                            nd3 = db.nodes.match("Node", id=inc3[k]["SOURCE"]).first()
                            print("3: " + nd3["fieldstring"] + " at: " + nd3["id"])
                            inc4 = list(db.relationships.match((None, nd3), r_type="partOf"))
                            if inc4:
                                for l in range(len(inc4)):
                                    nd4 = db.nodes.match("Node", id=inc4[l]["SOURCE"]).first()
                                    print("4: " + nd4["fieldstring"] + " at: " + nd4["id"])
                                    inc5 = list(db.relationships.match((None, nd4), r_type="partOf"))
                                    if inc5:
                                        for m in range(len(inc5)):
                                            nd5 = db.nodes.match("Node", id=inc5[m]["SOURCE"]).first()
                                            print("5: " + nd5["fieldstring"] + " at: " + nd5["id"])
                                            inc6 = list(db.relationships.match((None, nd5), r_type="partOf"))
                                            if inc6:
                                                for n in range(len(inc6)):
                                                    nd6 = db.nodes.match("Node", id=inc6[n]["SOURCE"]).first()
                                                    print("6: " + nd6["fieldstring"] + " at: " + nd6["id"])
                                                    print("This is the last level.")
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
            else:
                pass
    except IndexError as I:
        print(I)

print()
print("The highest number indicates a leaf node, above that are reasons for citing and then table of contents elements. ")
#TODO better output format of linked nodes, for example visualization