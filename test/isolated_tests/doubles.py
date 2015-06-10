from yosai import (
    CacheKeyRemovalException,
)

from yosai.account import (
    IAccount,
)

from yosai.authc import (
    IAuthenticationToken,
)

from yosai.cache import (
    ICache,
    ICacheManager,
)

from yosai.realm import (
    IAccountCacheHandler,
)

from yosai.account import (
    IAccountStore,
)


class MockCache(ICache):
    
    def __init__(self, keyvals={}):
        # keyvals is a dict
        self.kvstore = keyvals
    
    @property
    def values(self):
        return self.kvstore.values()

    def get(self, key):
        return self.kvstore.get(key, None) 

    def put(self, key, value):
        self.kvstore[key] = value 

    def remove(self, key):
        try:
            return self.kvstore.pop(key)
        except KeyError:
            raise CacheKeyRemovalException


class MockCacheManager(ICacheManager):

    def __init__(self, cache):
        self.cache = cache
   
    def get_cache(self, name):
        # regardless of the name, return the stock cache
        return self.cache


class MockToken(IAuthenticationToken, object):

    @property
    def principal(self):
        pass

    @property
    def credentials(self):
        pass


class MockAccountCacheHandler(IAccountCacheHandler, object):

    def __init__(self, account):
        self.account = account
   
    def get_cached_account(self, account):
        return self.account  # always returns the initialized account 


class MockAccount(IAccount):

    def __init__(self, account_id, credentials={}, attributes={}):
        self._account_id = account_id
        self._credentials = credentials
        self._attributes = attributes
        
    @property 
    def account_id(self):
        return self._account_id 

    @property 
    def credentials(self):
        return self._credentials 

    @property 
    def attributes(self):
        return self._attributes 

    def __eq__(self, other):
        try:
            result = (self._account_id == other._account_id and 
                      self.credentials == other.credentials and
                      self.attributes == other.attributes)
        except Exception:
            return False
        return result

    def __repr__(self):
        return "<MockAccount(id={0}, credentials={1}, attributes={2})>".\
            format(self.account_id, self.credentials, self.attributes)


class MockAccountStore(IAccountStore, object):
    
    def __init__(self, account=MockAccount(account_id='MAS123')):
        self.account = account

    def get_account(self, authc_token):
        return self.account  # always returns the initialized account


class MockPubSub(object):

    def isSubscribed(self, listener, topic_name):
        return True 

    def sendMessage(self, topic_name, **kwargs):
        pass  # True   just for testing, otherwise returns None in production 

    def subscribe(self, _callable, topic_name):
        return _callable, True

    def unsubscribe(self, listener, topic_name):
        return listener 

    def unsubAll(self):
        return [] 

    def __repr__(self):
        return "<MockPubSub()>"
