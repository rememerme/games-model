'''
    The models and Cassandra serializers for the Friends and 
    Requests models to be used in the Friends, Requests, Received, and
    Sent APIs. 

    @author: Andy Oberlin, Jake Gregg
'''

from cassa import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid
from rest_framework import serializers
import json

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('friends', server_list=settings.CASSANDRA_NODES)

'''
    The Friends model to support the API.
'''
class Friends(CassaModel):
    table = pycassa.ColumnFamily(POOL, 'friends')
    
    user_id = models.TextField(primary_key=True)
    friends_list = models.TextField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Friends object from a map object with the properties.
        '''
        friends = Friends(**mapRep)
        friends.friends_list = json.loads(friends.friends_list)
        return friends

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Friends object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['user_id'] = str(cassRep[0])
        
        return Friends.fromMap(mapRep)
    
    @staticmethod
    def get(user_id=None):
        '''
            Method for getting a user's friends list from cassandra given the user_id.
        '''
        if user_id:
            return Friends.getByID(user_id)
        
        return None
    
    @staticmethod
    def getByID(user_id):
        '''
            Gets the user's friends given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
        return Friends.fromCassa((str(user_id), Friends.table.get(user_id)))
    
    def save(self):
        '''
            Saves a set of friends given by the cassandra in/output, which is
            a dictionary of values.
        
            @param users: The user and friend list to store.
        '''
        user_id = uuid.uuid1() if not self.user_id else uuid.UUID(self.user_id)
        Friends.table.insert(user_id, CassaFriendsSerializer(self).data)
        self.user_id = str(user_id)
        

class CassaFriendsSerializer(serializers.ModelSerializer):
    '''
        The Friends serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    def transform_friends_list(self, obj, value):
        return json.dumps(value)

    class Meta:
        model = Friends
        fields = ('friends_list', )


'''
    The Received Requests model to support the API
'''
class ReceivedRequests(CassaModel):
    table = pycassa.ColumnFamily(POOL, 'received_requests')
    
    user_id = models.TextField(primary_key=True)
    requests = models.TextField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Requests object from a map object with the properties.
        '''
        received = ReceivedRequests(**mapRep)
        received.requests = json.loads(received.requests)
        return received

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Requests object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['user_id'] = str(cassRep[0])
        
        return ReceivedRequests.fromMap(mapRep)
    
    @staticmethod
    def get(user_id=None):
        '''
            Method for getting a user's friend requests list from cassandra given the user_id.
        '''
        if user_id:
            return ReceivedRequests.getByID(user_id)
        
        return None
    
    @staticmethod
    def getByID(user_id):
        '''
            Gets the user's friend requests given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
        return ReceivedRequests.fromCassa((str(user_id), ReceivedRequests.table.get(user_id)))
    
    def save(self):
        '''
            Saves a set of friend requests given by the cassandra in/output, which is
            a dictionary of values.
        
            @param users: The set of users to save to the user store.
        '''
        user_id = uuid.uuid1() if not self.user_id else uuid.UUID(self.user_id)
        ReceivedRequests.table.insert(user_id, CassaReceivedRequestsSerializer(self).data)
        self.user_id = str(user_id)
        
        
class CassaReceivedRequestsSerializer(serializers.ModelSerializer):
    '''
        The Requests serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    def transform_requests(self, obj, value):
        return json.dumps(value)
    
    class Meta:
        model = ReceivedRequests
        fields = ('requests', )    
    
'''
    The Received Requests model to support the API
'''
class SentRequests(CassaModel):
    table = pycassa.ColumnFamily(POOL, 'sent_requests')
    
    user_id = models.TextField(primary_key=True)
    requests = models.TextField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Requests object from a map object with the properties.
        '''
        received = SentRequests(**mapRep)
        received.requests = json.loads(received.requests)
        return received

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Requests object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['user_id'] = str(cassRep[0])
        
        return SentRequests.fromMap(mapRep)
    
    @staticmethod
    def get(user_id=None):
        '''
            Method for getting a user's friend requests list from cassandra given the user_id.
        '''
        if user_id:
            return SentRequests.getByID(user_id)
        
        return None
    
    @staticmethod
    def getByID(user_id):
        '''
            Gets the user's friend requests given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
        return SentRequests.fromCassa((str(user_id), SentRequests.table.get(user_id)))
    
    def save(self):
        '''
            Saves a set of friend requests given by the cassandra in/output, which is
            a dictionary of values.
        
            @param users: The set of users to save to the user store.
        '''
        user_id = uuid.uuid1() if not self.user_id else uuid.UUID(self.user_id)
        SentRequests.table.insert(user_id, CassaReceivedRequestsSerializer(self).data)
        self.user_id = str(user_id)
        
        
class CassaSentRequestsSerializer(serializers.ModelSerializer):
    '''
        The Requests serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    def transform_requests(self, obj, value):
        return json.dumps(value)
    
    class Meta:
        model = SentRequests
        fields = ('requests', ) 
