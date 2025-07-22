from models.user import User

# TODO: This is a temporary store for users. We will replace this with a database in the future.
# TODO: We will also add a password hash to the user model and UUID for the user.
users = [
    User(user_id=1, name="Sudhir", type="user"),
    User(user_id=2, name="Ranjan", type="staff"),
    User(user_id=3, name="Alexa", type="AI"),
    User(user_id=4, name="Fong", type="user"),
    User(user_id=5, name="Dan", type="user"),
    User(user_id=6, name="Maccy", type="staff"),
    User(user_id=7, name="Siri", type="AI"),
    User(user_id=8, name="Jane", type="user"),
    User(user_id=9, name="Wei", type="user"),
    User(user_id=10, name="Staff Bob", type="staff"),
    User(user_id=11, name="Nancy", type="AI"),
    User(user_id=12, name="David", type="user"),
]
