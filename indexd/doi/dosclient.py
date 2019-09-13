import json
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests


def json_dumps(data):
    return json.dumps({k: v for (k, v) in data.items() if v is not None})


def handle_error(resp):
    if 400 <= resp.status_code < 600:
        try:
            json = resp.json()
            resp.reason = json["error"]
        except:
            pass
        finally:
            resp.raise_for_status()


class DOSClient(object):

    def __init__(self, baseurl):
        self.url = baseurl

    def url_for(self, *path):
        return urljoin(self.url, "/".join(path))

    def get(self, did):
        """Return a document object corresponding to a single did"""
        try:
            response = self._get("dataobjects", did)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise e
        try:
            return Document(self, did, json=response.json())
        except ValueError as e:
            return None

    def _get(self, *path, **kwargs):
        resp = requests.get(self.url_for(*path), timeout=15, **kwargs)
        handle_error(resp)
        return resp

class Document(object):

    def __init__(self, client, did, json=None):
        self.client = client
        self.did = did
        self.urls = None
        self.alias = None
        self.sha1 = None
        self._fetched = False
        self._load(json)

    def _render(self, include_rev=True):
        if not self._fetched:
            raise RuntimeError("Document must be fetched from server before being rendered as json")
        json = {
            "urls": self.urls,
            "hashes": self.hashes,
            "size": self.size
        }
        if include_rev:
            json["rev"] = self.rev
        return json

    def to_json(self, include_rev=True):
        json = self._render(include_rev=include_rev)
        json["did"] = self.did
        return json

    def _load(self, json=None):
        """refresh the document contents from the server"""
        json = json or self.client._get(self.did).json()
        json = json["data_object"]
        assert json["id"].lower() == self.did.lower()
        self.urls = []
        if 'urls' in json:
            self.urls = [x['url'] for x in json['urls'] if 'url' in x]
            self.urls_metadata = {x['url']:x['user_metadata'] for x in json['urls'] if 'user_metadata' in x}

        if 'version' in json:
            self.rev = json['version']

        if 'updated' in json:
            self.updated_data = json['updated']

        if 'created' in json:
            self.created_data = json['created']

        if 'name' in json:
            self.file_name = json['name']

        if 'size' in json:
            self.size = int(json['size'])

        if 'aliases' in json:
            self.alias = json['aliases']

        self.hashes = {}
        if 'checksums' in json:
            self.hashes = {x['type']: x['checksum'] for x in json['checksums']}

        self._fetched = True
