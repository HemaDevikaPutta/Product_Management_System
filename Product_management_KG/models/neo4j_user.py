from flask_login import UserMixin
from extensions import neo4j_driver
from utils.neo4j_helpers import run_read_query

class Neo4jUser(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


    @staticmethod
    def get_by_id(user_id):
        query = """
        MATCH (u:User {id: $id})
        RETURN u LIMIT 1
        """
        result = run_read_query(query, {"id": user_id})
        if result:
            user_data = result[0]['u']
            return Neo4jUser(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                role=user_data['role'],
                password=user_data.get('password')
            )
        return None

    @staticmethod
    def get_by_email(email):
        query = """
        MATCH (u:User {email: $email})
        RETURN u LIMIT 1
        """
        result = run_read_query(query, {"email": email})
        if result:
            user_data = result[0]['u']
            return Neo4jUser(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                role=user_data['role'],
                password=user_data.get('password')
            )
        return None
    

def load_user(user_id):
    query = "MATCH (u:User {id: $id}) RETURN u LIMIT 1"
    result = run_read_query(query, {"id": user_id})
    if result:
        u = result[0]['u']
        return Neo4jUser(id=u['id'], name=u['name'], email=u['email'], role=u['role'])
    return None