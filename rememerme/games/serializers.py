from models import Game, Party, PartyMember, Round, Nomination
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    '''
        The Game serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Game
        fields = ('game_id', 'party_id', 'current_round_id', 'date_created', 'last_modified')
        
class PartySerializer(serializers.ModelSerializer):
    '''
        The Party serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Party
        fields = ('party_id', 'leader_id', 'date_created', 'last_modified')
        
class PartyMemberSerializer(serializers.ModelSerializer):
    '''
        The Party Member serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PartyMember
        fields = ('party_member_id', 'user_id', 'party_id', 'date_created', 'last_modified')      
        
class RoundSerializer(serializers.ModelSerializer):
    '''
        The Round serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Round
        fields = ('round_id', 'selector_id', 'selection_id', 'game_id', 'phrase_card_id', 'date_created', 'last_modified')
        
class NominationSerializer(serializers.ModelSerializer):
    '''
        The Nomination serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Nomination
        fields = ('nomination_id', 'round_id', 'nominator_id', 'nomination_card_id', 'date_created', 'last_modified') 

