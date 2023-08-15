
# Library imports
import requests
import uuid
from typing import List, Optional, Dict, Union, Tuple


class __RequestHelper:
    @staticmethod
    def _put(url: str, data: Optional[Dict] = None, params: Optional[List[Tuple]] = None) -> Union[Dict, List]:
        response = requests.put(url, json=data, params=params)
        if not response:
            raise Exception(f"{response.status_code}: {response.text}")
        return response.json()

    @staticmethod
    def _get(url: str, params: Optional[List[Tuple]] = None) -> Union[Dict, List]:
        response = requests.get(url, params=params)
        if not response:
            raise Exception(f"{response.status_code}: {response.text}")
        return response.json()

    @staticmethod
    def _delete(url: str, data: Optional[Dict] = None, params: Optional[List[Tuple]] = None) -> Union[Dict, List]:
        response = requests.delete(url, data=data, params=params)
        if not response:
            raise Exception(f"{response.status_code}: {response.text}")
        return response.json()

    @staticmethod
    def _post(url: str, data: Dict, params: Optional[List[Tuple]] = None) -> Union[Dict, List]:
        response = requests.post(url, json=data, params=params)
        if not response:
            raise Exception(f"{response.status_code}: {response.text}")
        return response.json()


class CouchedCollection(__RequestHelper):

    def __init__(self, url: str, name: str):
        self._url = f"{url}/{name}"
        self.name = name

    def put(self, doc: Dict) -> Dict:
        return self._put(f"{self._url}/{self._uuid()}", data=doc)

    def get(self, _id: str) -> Dict:
        return self._get(f"{self._url}/{_id}")

    def update(self, _id: str, doc: Dict, rev: str):
        return self._put(f"{self._url}/{_id}", data=doc, params=[("rev", rev)])

    def delete(self, _id: str, rev: str):
        return self._delete(f"{self._url}/{_id}", params=[("rev", rev)])

    def find(self, selector: Dict, fields: Optional[List] = None, limit: int = 0) -> List:
        data = {"selector": selector}
        if fields:
            data["fields"] = fields
        if limit:
            data["limit"] = limit
        return self._post(f"{self._url}/_find", data=data).get("docs", [])

    def count(self) -> int:
        return self._get(self._url).get("doc_count", -1)

    @staticmethod
    def _uuid() -> str:
        return uuid.uuid4().hex


class Couched(__RequestHelper):

    def __init__(self, url: str, username: str, password: str):
        self._url = f"http://{username}:{password}@{url}"

    def collections(self) -> List[CouchedCollection]:
        return [CouchedCollection(self._url, col) for col in self._get(f"{self._url}/_all_dbs")]

    def create_collection(self, name: str):
        self._put(f"{self._url}/{name}")
        return CouchedCollection(self._url, name)

    def get_collection(self, name: str):
        return CouchedCollection(self._url, name)

    def delete_collection(self, name: str):
        return self._delete(f"{self._url}/{name}")


if __name__ == "__main__":

    couch = Couched(url="127.0.0.1:5984", username="admin", password="pineapple")

    d1 = couch.create_collection("dummy1")

    assert(d1.count() == 0)

    apple = d1.put({"type": "fruit", "name": "apple"})
    banana = d1.put({"type": "fruit", "name": "banana"})
    cherry = d1.put({"type": "fruit", "name": "cherry"})

    assert(d1.count() == 3)

    d1.update(apple["id"], {"type": "fruit", "name": "apfel"}, rev=apple["rev"])

    assert(d1.get(apple["id"])["name"] == "apfel")



    d1.delete(cherry["id"], cherry["rev"])

    assert(len(d1.find({"type": "fruit"})) == 2)

    couch.delete_collection("dummy1")


    pass

