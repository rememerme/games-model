from models import Game, GameMember, Round, Nomination
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    '''
        The Game serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = Game
        fields = ('game_id', 'party_id', 'current_round_id', 'date_created', 'last_modified')
        
class GameMemberSerializer(serializers.ModelSerializer):
    '''
        The Game Member serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = GameMember
        fields = ('game_member_id', 'user_id', 'game_id', 'status', 'date_created', 'last_modified')      
        
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

