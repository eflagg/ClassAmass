from model import User, Course, Course_Favorited, Course_Taken, Course_Taking

def get_user_by_email(email):
    """Return user based on email of current_user in session."""

    return User.query.filter_by(email=email).first()


def get_user_by_session():
    """Return user based on email of current_user in session."""

    email = session.get("current_user")
    return User.query.filter_by(email=email).first()


def is_favorited(user, course_id):
    """Query that returns true if course is alreay favorited."""

    if Course_Favorited.query.filter_by(
                            user_id=user.user_id, course_id=course_id).first():
        return True

    return False


def is_taken(user, course_id):
    """Query that returns true if course is alreay in taken list."""

    if Course_Taken.query.filter_by(
                            user_id=user.user_id, course_id=course_id).first():
        return True

    return False


def is_enrolled(user, course_id):
    """Query that returns true if course is alreay in enrolled list."""

    if Course_Taking.query.filter_by(
                            user_id=user.user_id, course_id=course_id).first():
        return True

    return False