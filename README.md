# Couched
### Introduction
Simple pythonic CouchDB bindings, inspired by pyMongoDB API. 

For simplicity the DMS is referred to as a singular Database, and the next layer of organsiation is referred to as a
collection (instead of a database of databases). A collection is a, well collection, of documents.

Not all couchDB functionality has been implemented in the bindings, just the basic CRUD stuff you need.


### Usage
Here are some basic CRUD operations
```python
from couched import Couched

# Create couched database instance
couch = Couched(url="127.0.0.1:5984", username="admin", password="pineapple")

# Create a new collection within DB. It will return a CouchedCollection object. 
# All work with docs is performed at the collection level.
coll = couch.create_collection("fruit")

# Add some documents
apple = coll.put({"type": "fruit", "name": "apple"})
banana = coll.put({"type": "fruit", "name": "banana"})
cherry = coll.put({"type": "fruit", "name": "cherry"})

# Count number of docs in the collection
num_docs = coll.count()

# Update an existing doc (don't forget to pass the current rev id)
coll.update(apple["id"], {"type": "fruit", "name": "apfel"}, rev=apple["rev"])

# Delete a doc (provide current rev id again)
coll.delete(cherry["id"], cherry["rev"])

# Find docs with a query (https://docs.couchdb.org/en/stable/api/database/find.html#find-selectors)
for doc in coll.find({"type": "fruit"}):
    print(f"Fruit: {doc['name']}")

# Get another collection
coll2 = couch.get_collection("veg")

# Delete a collection (including all docs within it)
couch.delete_collection("fruit")
```
