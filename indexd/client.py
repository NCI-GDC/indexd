try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests


def handle_error(resp):
    if 400 <= resp.status_code < 600:
        try:
            json = resp.json()
            resp.reason = json["error"]
        except KeyError:
            pass
        finally:
            resp.raise_for_status()


class IndexClient(object):

    def __init__(self, baseurl, version="v0", auth=None):
        self.auth = auth
        self.url = baseurl
        self.version = version

    def url_for(self, *path):
        return urljoin(self.url, "/".join(path))


    def global_get(self, did, no_dist=False):
        """
        Makes a web request to the Indexd service global endpoint to retrieve
        an index document record.

        :param str did:
            The UUID for the index record we want to retrieve.

        :param boolean no_dist:
            *optional* Specify if we want distributed search or not

        :returns: A Document object representing the index record
        """
        try:
            if no_dist:
                response = self._get(did, params={'no_dist': ''})
            else:
                response = self._get(did)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise e

        return Document(self, did, json=response.json())

    def get(self, did):
        """
        Makes a web request to the Indexd service to retrieve an index document record.

        :param str did:
            The UUID for the index record we want to retrieve.

        :returns: A Document object representing the index record
        """
        try:
            response = self._get("index", did)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise e

        return Document(self, did, json=response.json())

    def _get(self, *path, **kwargs):
        resp = requests.get(self.url_for(*path), **kwargs)
        handle_error(resp)
        return resp


class Document(object):

    def __init__(self, client, did, json=None):
        self.client = client
        self.did = did
        self._fetched = False
        self._deleted = False
        self._load(json)

    def __eq__(self, other_doc):
        """
        equals `==` operator overload
        """
        return self.did == other_doc.did

    def __ne__(self, other_doc):
        """
        not equals `!=` operator overload
        """
        return self.did != other_doc.did

    def __hash__(self):
        return hash(self.did)

    def __lt__(self, other_doc):
        return self.did < other_doc.did

    def __gt__(self, other_doc):
        return self.did > other_doc.did

    def __repr__(self):
        """
        String representation of a Document

        Example:
            <Document(size=1, form=object, file_name=filename.txt, ...)>
        """
        attributes = ', '.join([
            '{}={}'.format(attr, self.__dict__[attr])
            for attr in self._attrs
        ])
        return '<Document(' + attributes + ')>'