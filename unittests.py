
# Library imports
import unittest

# Project imports
from couched import Couched

URL = "127.0.0.1:5984"
USER = "admin"
PASSW = "pineapple"


class UnitTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Couched(url=URL, username=USER, password=PASSW)
        self.coll = self.db.create_collection("test_collection")

    def tearDown(self) -> None:
        try:
            self.db.delete_collection("test_collection")
            self.db.delete_collection("test_collection2")
        except:
            pass

    def test_create_get_delete_list_collection(self):
        coll_name = "test_collection2"
        prev_num_coll = len(self.db.collections())
        self.db.create_collection(coll_name)
        coll = self.db.get_collection(coll_name)
        self.assertEqual(coll_name, coll.name)
        self.assertEqual(len(self.db.collections()), prev_num_coll + 1)
        self.db.delete_collection(coll_name)
        self.assertEqual(len(self.db.collections()), prev_num_coll)

    def test_put_get_document(self):
        doc = {"type": "fruit", "name": "apple"}
        id = self.coll.put(doc)["id"]
        doc2 = self.coll.get(id)
        del doc2["_id"]
        del doc2["_rev"]
        self.assertDictEqual(doc, doc2)

    def test_update_document(self):
        doc = {"type": "fruit", "name": "apple"}
        update_doc = {"type": "fruit", "name": "apple", "color": ["red", "green"]}
        d = self.coll.put(doc)
        rev = d["rev"]
        id = d["id"]
        doc2 = self.coll.get(id)
        del doc2["_id"]
        del doc2["_rev"]
        self.assertDictEqual(doc, doc2)
        self.coll.update(id, doc=update_doc, rev=rev)
        doc3 = self.coll.get(id)
        del doc3["_id"]
        del doc3["_rev"]
        self.assertDictEqual(update_doc, doc3)

    def test_delete_find_document(self):
        doc = {"type": "fruit", "name": "apple"}
        d = self.coll.put(doc)
        results = self.coll.find(selector={"name": "apple"}, fields=["type", "name"], limit=10)
        self.assertDictEqual(doc, results[0])
        self.coll.delete(d["id"], d["rev"])
        results = self.coll.find(selector={"name": "apple"}, fields=["type", "name"], limit=10)
        self.assertEqual(len(results), 0)

    def test_count_documents(self):
        self.assertEquals(self.coll.count(), 0)
        doc = {"type": "fruit", "name": "apple"}
        self.coll.put(doc)
        self.coll.put(doc)
        self.coll.put(doc)
        self.assertEquals(self.coll.count(), 3)



if __name__ == "__main__":

    unittest.main()