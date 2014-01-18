from rememerme.games.models import GameMember
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

class GamePermissions():
    """
        Object-level permission to only allow members of the game's party to
        have access to it.
    """
    @staticmethod
    def has_object_permission(request, obj):
        try:
            members = set(GameMember.filterByGame(obj.game_id))
            return GameMember(user_id=request.user.pk) in members
        except CassaNotFoundException:
            # Instance must have an attribute named `owner`.
            return False
        
