from rememerme.games.models import PartyMember
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

class GamePermissions():
    """
        Object-level permission to only allow members of the game's party to
        have access to it.
    """
    @staticmethod
    def has_object_permission(request, obj):
        try:
            members = set(PartyMember.filterByParty(obj.party_id))
            return PartyMember(user_id=request.user.pk) in members
        except CassaNotFoundException:
            # Instance must have an attribute named `owner`.
            return False
        
