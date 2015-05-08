from collections import defaultdict

from yosai import (
    RealmAttributesException,
)

from . import (
    ICompositeAccountId,
    ICompositeAccount,
)


class DefaultCompositeAccountId(ICompositeAccountId, object):

    def __init__(self):
        self.realm_accountids = defaultdict(set) 

    def get_realm_account_id(self, realm_name=None):
        return self.realm_accountids.get(realm_name, None)

    def set_realm_account_id(self, realm_name, accountid):
        self.realm_accountids[realm_name].add(accountid)

    def __eq__(self, other):
        if (other is self):
            return True
        
        if isinstance(other, DefaultCompositeAccountId):
            return self.realm_accountids == other.realm_accountids

        return False 
    
    def __repr__(self):
        return ', '.join(["{0}: {1}".format(realm, acctids) for realm, acctids 
                         in self.realm_accountids.items()])


class DefaultCompositeAccount(ICompositeAccount, object):

    def __init__(self, overwrite=True):
        self._account_id = DefaultCompositeAccountId()  # DG renamed 
        self._credentials = None
        self._merged_attrs = {}  # maybe change to OrderedDict() 
        self._overwrite = overwrite
        self._realm_attrs = defaultdict(dict)

    @property 
    def account_id(self):  # DG:  renamed from id
        return self._account_id 

    @property
    def attributes(self):
        return self._merged_attrs

    @property 
    def credentials(self):
        # not needed: all accounts added to a composite have already been 
        # authenticated -- included just to satisfy interface requirements
        return self._credentials 

    @property
    def realm_names(self):
        return self._realm_attrs.keys()

    def append_realm_account(self, realm_name, account):
        self._account_id.set_realm_account_id(realm_name, account.account_id)

        realm_attributes = account.attributes
        if (realm_attributes is None):
            realm_attributes = {} 

        try:
            self._realm_attrs[realm_name].update(realm_attributes)
        except (AttributeError, TypeError):
            msg = 'Could not update realm_attrs using ' + str(realm_attributes)
            raise RealmAttributesException(msg)

        for key, value in realm_attributes.items():
            if (self._overwrite):
                self._merged_attrs[key] = value 
            else:
                if (key not in self._merged_attrs):
                    self._merged_attrs[key] = value 
                
    def get_realm_attributes(self, realm_name):
        return self._realm_attrs.get(realm_name, dict())  # DG: no frozen dict


