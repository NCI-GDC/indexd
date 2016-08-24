import abc
import uuid


class IndexDriverABC(object):
    '''
    Index Driver Abstract Base Class

    Driver interface for interacting with index backends.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def ids(self, limit=100, start='', size=None, urls=None, hashes=None):
        '''
        Returns a list of records stored by the backend.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def hashes_to_urls(self, size, hashes, start=0, limit=100):
        '''
        Returns a list of urls matching supplied size and hashes.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def add(self, form, size, urls=[], hashes={}):
        '''
        Creates record for given data.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def get(self, did):
        '''
        Gets a record given the record id.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def update(self, did, rev, size=None, urls=None, hashes=None):
        '''
        Updates record with new values.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def delete(self, did, rev):
        '''
        Deletes record.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def __contains__(self, did):
        '''
        Returns True if record is stored by backend.
        Returns False otherwise.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def __iter__(self):
        '''
        Returns an iterator over unique records stored by backend.
        '''
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def __len__(self):
        '''
        Returns the number of unique records stored by backend.
        '''
        raise NotImplementedError('TODO')
