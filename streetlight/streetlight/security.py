from .models import DBSession, Admin


def groupfinder(userid, request):
    """Find user group.

    """
    admin = DBSession.query(Admin).filter_by(user_name=userid).first()
    return [admin.user_group]
