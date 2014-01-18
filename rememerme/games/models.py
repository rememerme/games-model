'''
    The models and Cassandra serializers for the Game and 
    Requests models to be used in the Game, Requests, Received, and
    Sent APIs. 

    @author: Andy Oberlin, Jake Gregg
'''

from cassa import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid
from rest_framework import serializers

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('games', server_list=settings.CASSANDRA_NODES)

class Game(CassaModel):
    '''
        The Game model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'game')
    
    game_id = models.TextField(primary_key=True)
    party_id = models.TextField()
    current_round_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Game object from a map object with the properties.
        '''
        game = Game(**mapRep)
        return game

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Game object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['game_id'] = str(cassRep[0])
        
        return Game.fromMap(mapRep)
    
    @staticmethod
    def get(game_id=None):
        '''
            Method for getting a user's Game list from cassandra given the user_id.
        '''
        if game_id:
            return Game.getByID(game_id)
        
        return None
    
    @staticmethod
    def getByID(game_id):
        '''
            Gets the user's Game given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(game_id, uuid.UUID):
            game_id = uuid.UUID(game_id)
        return Game.fromCassa((str(game_id), Game.table.get(game_id)))
    
    def save(self):
        '''
            Saves a set of Game given by the cassandra in/output, which is
            a dictionary of values.
        
            @param users: The user and friend list to store.
        '''
        game_id = uuid.uuid1() if not self.game_id else uuid.UUID(self.game_id)
        Game.table.insert(game_id, CassaGameSerializer(self).data)
        self.game_id = str(game_id)
        

class CassaGameSerializer(serializers.ModelSerializer):
    '''
        The Game serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''

    class Meta:
        model = Game
        fields = ('party_id', 'current_round_id', 'date_created', 'last_modified')


class Party(CassaModel):
    '''
        The Game model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'party')
    
    party_id = models.TextField(primary_key=True)
    leader_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Party object from a map object with the properties.
        '''
        party = Party(**mapRep)
        return party

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Party object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['party_id'] = str(cassRep[0])
        
        return Party.fromMap(mapRep)
    
    @staticmethod
    def get(party_id=None):
        '''
            Method for getting a party by id.
        '''
        if party_id:
            return Party.getByID(party_id)
        
        return None
    
    @staticmethod
    def getByID(party_id):
        '''
            Gets the user's Party given an ID.
                    
            @param party_id: The uuid of the party.
        '''
        if not isinstance(party_id, uuid.UUID):
            party_id = uuid.UUID(party_id)
        return Party.fromCassa((str(party_id), Party.table.get(party_id)))
    
    def save(self):
        '''
            Saves a set of Party given by the cassandra in/output, which is
            a dictionary of values.
        '''
        party_id = uuid.uuid1() if not self.party_id else uuid.UUID(self.party_id)
        Party.table.insert(party_id, CassaGameSerializer(self).data)
        self.party_id = str(party_id)
        

class CassaPartySerializer(serializers.ModelSerializer):
    '''
        The Party serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''

    class Meta:
        model = Party
        fields = ('leader_id', 'date_created', 'last_modified')


class PartyMember(CassaModel):
    '''
        The Party Member model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'party_member')
    
    party_member_id = models.TextField(primary_key=True)
    user_id = models.TextField()
    party_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Party object from a map object with the properties.
        '''
        member = PartyMember(**mapRep)
        return member

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Party object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['party_member_id'] = str(cassRep[0])
        
        return PartyMember.fromMap(mapRep)
    
    @staticmethod
    def get(party_member_id=None):
        '''
            Method for getting a party member by id, party_id or user_id
        '''
        if party_member_id:
            return PartyMember.getByID(party_member_id)
        
        return None
    
    @staticmethod
    def filter(party_id=None, user_id=None):
        if party_id:
            return PartyMember.filterByParty(party_id)
        
        if user_id:
            return PartyMember.filterByUser(user_id)
    
    @staticmethod
    def getByID(party_member_id):
        '''
            Gets the Party members given an ID.
                    
            @param party_id: The uuid of the party.
        '''
        if not isinstance(party_member_id, uuid.UUID):
            party_member_id = uuid.UUID(party_member_id)
        return PartyMember.fromCassa((str(party_member_id), PartyMember.table.get(party_member_id)))
    
    @staticmethod
    def filterByParty(party_id):
        '''
            Gets the party members by party.
        '''
        if not isinstance(party_id, uuid.UUID):
            party_id = uuid.UUID(party_id)
            
        expr = pycassa.create_index_expression('party_id', party_id)
        clause = pycassa.create_index_clause([expr])
        ans = list(PartyMember.table.get_indexed_slices(clause))
        
        return [PartyMember.fromCassa(cassRep) for cassRep in ans]
    
    @staticmethod
    def filterByUser(user_id):
        '''
            Gets the party members by party.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
            
        expr = pycassa.create_index_expression('user_id', user_id)
        clause = pycassa.create_index_clause([expr])
        ans = list(PartyMember.table.get_indexed_slices(clause))
        
        return [PartyMember.fromCassa(cassRep) for cassRep in ans]
    
    def save(self):
        '''
            Saves a set of Party given by the cassandra in/output, which is
            a dictionary of values.
        '''
        party_member_id = uuid.uuid1() if not self.party_member_id else uuid.UUID(self.party_member_id)
        PartyMember.table.insert(party_member_id, CassaPartyMemberSerializer(self).data)
        self.party_member_id = str(party_member_id)
        

class CassaPartyMemberSerializer(serializers.ModelSerializer):
    '''
        The Party serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PartyMember
        fields = ('user_id', 'party_id', 'date_created', 'last_modified')

class Round(CassaModel):
    '''
        The Round model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'round')
    
    round_id = models.TextField(primary_key=True)
    selector_id = models.TextField()
    selection_id = models.TextField()
    phrase_card_id = models.TextField()
    game_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Party object from a map object with the properties.
        '''
        member = Round(**mapRep)
        return member

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Party object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['round_id'] = str(cassRep[0])
        
        return Round.fromMap(mapRep)
    
    @staticmethod
    def get(round_id=None):
        '''
            Method for getting a party member by id, party_id or user_id
        '''
        if round_id:
            return Round.getByID(round_id)
        
        return None
    
    @staticmethod
    def getByID(round_id):
        '''
            Gets the Party members given an ID.
                    
            @param party_id: The uuid of the party.
        '''
        if not isinstance(round_id, uuid.UUID):
            round_id = uuid.UUID(round_id)
        return Round.fromCassa((str(round_id), Round.table.get(round_id)))
    
    def save(self):
        '''
            Saves a set of Party given by the cassandra in/output, which is
            a dictionary of values.
        '''
        round_id = uuid.uuid1() if not self.round_id else uuid.UUID(self.round_id)
        Round.table.insert(round_id, CassaRoundSerializer(self).data)
        self.round_id = str(round_id)
        

class CassaRoundSerializer(serializers.ModelSerializer):
    '''
        The Party serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Round
        fields = ('selector_id', 'selection_id', 'game_id', 'phrase_card_id', 'date_created', 'last_modified')
        
        
class Nomination(CassaModel):
    '''
        The Nomination model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'nomination')
    
    nomination_id = models.TextField(primary_key=True)
    round_id = models.TextField()
    nominator_id = models.TextField()
    nomination_card_id = models.TextField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Nomination object from a map object with the properties.
        '''
        member = Nomination(**mapRep)
        return member

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Nomination object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['nomination_id'] = str(cassRep[0])
        
        return Round.fromMap(mapRep)
    
    @staticmethod
    def get(nomination_id=None):
        '''
            Method for getting a Nomination by id, party_id or user_id
        '''
        if nomination_id:
            return Nomination.getByID(nomination_id)
        
        return None
    
    @staticmethod
    def filter(round_id=None, nominator_id=None):
        if round_id:
            return Nomination.filterByRound(round_id)
        
        if nominator_id:
            return Nomination.filterByUser(nominator_id)
        
        return None
    
    @staticmethod
    def getByID(nomination_id):
        '''
            Gets the Nomination given an ID.
                    
            @param nomination_id: The uuid of the nomination.
        '''
        if not isinstance(nomination_id, uuid.UUID):
            nomination_id = uuid.UUID(nomination_id)
        return Nomination.fromCassa((str(nomination_id), Nomination.table.get(nomination_id)))
    
    @staticmethod
    def filterByRound(round_id):
        '''
            Gets the nomination by the round.
        '''
        if not isinstance(round_id, uuid.UUID):
            round_id = uuid.UUID(round_id)
            
        expr = pycassa.create_index_expression('round_id', round_id)
        clause = pycassa.create_index_clause([expr])
        ans = list(Nomination.table.get_indexed_slices(clause))
        
        return [Nomination.fromCassa(cassRep) for cassRep in ans]
    
    @staticmethod
    def filterByUser(user_id):
        '''
            Gets the nomination by the round.
        '''
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)
            
        expr = pycassa.create_index_expression('user_id', user_id)
        clause = pycassa.create_index_clause([expr])
        ans = list(Nomination.table.get_indexed_slices(clause))
        
        return [Nomination.fromCassa(cassRep) for cassRep in ans]
    
    def save(self):
        '''
            Saves a set of Nomination given by the cassandra in/output, which is
            a dictionary of values.
        '''
        nomination_id = uuid.uuid1() if not self.nomination_id else uuid.UUID(self.nomination_id)
        Round.table.insert(nomination_id, CassaRoundSerializer(self).data)
        self.nomination_id = str(nomination_id)
        

class CassaNominationSerializer(serializers.ModelSerializer):
    '''
        The Party serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Nomination
        fields = ('round_id', 'nominator_id', 'nomination_card_id', 'date_created', 'last_modified')