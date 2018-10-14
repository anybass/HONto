# Context Selection in a Heterogeneous Legal Ontology

This code allows for a user-driven context selection within a previously generated concept hierarchy using the *HONto* code (see HONto folder).

## Prerequisites
* Python 3
* [Neo4j community server](https://neo4j.com/download-center/#releases)
* [ElasticSearch](https://www.elastic.co/de/downloads/elasticsearch)
* [GraphAware Neo4j Elasticsearch Integration (Neo4j Module)](https://github.com/graphaware/neo4j-to-elasticsearch)
  * Follow their guidelines to install the plugin
  * We added our configuration files for your reference within the *neo4j-conf* folder. They are important to generate a correct mapping from neo4j to elasticsearch.
  
## Quick Start Guide
1. Run `python graph_relationships.py`. It will generate from the *features.json* file two new files:
 
 * features_entities.csv
 * features_relationships.csv
 
2. Those files are ready for use with the neo4j [import tool](https://neo4j.com/docs/operations-manual/current/tutorial/import-tool/). Follow the instructions on that documentation page to import your entities and relationships (as the process may change in future versions of neo4j). 

3. Check in the [neo4j browser](http://localhost:7474/browser/) whether everything has been imported successfully. Then stop the neo4j server and start elasticsearch. After everything has initialized, start neo4j again. (It sometimes requires multiple tries to get replication working)
 
4. Run `python context_selector.py` and you can navigate within the concept hierarchy. It basically takes your search keywords and provides you all the contexts they appear in. After you choose one context and the level of abstraction to get related concepts, the output will be linked legal texts along with the context path from the concept hierarchy. 

  

