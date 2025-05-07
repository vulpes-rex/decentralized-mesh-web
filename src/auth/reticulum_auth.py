from datetime import datetime, timedelta
import uuid
from ..utils.crypto import CryptoHandler

class ReticulumAuth:
    def __init__(self):
        self.crypto = CryptoHandler()
        self.sessions = {}
        self.tokens = {}
        
    async def authenticate(self, user_id, scope):
        session_id = str(uuid.uuid4())
        session = {
            'user_id': user_id,
            'scope': scope,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=24)
        }
        self.sessions[session_id] = session
        
        token = await self.generate_token(session)
        self.tokens[token] = session_id
        
        return {
            'session_id': session_id,
            'token': token,
            'expires_at': session['expires_at']
        }
        
    async def generate_token(self, session):
        token_data = {
            'user_id': session['user_id'],
            'scope': session['scope'],
            'exp': int(session['expires_at'].timestamp())
        }
        return self.crypto.encrypt_data(str(token_data))
        
    async def verify_token(self, token):
        if token not in self.tokens:
            return False
        session_id = self.tokens[token]
        session = self.sessions.get(session_id)
        
        if not session:
            return False
            
        if session['expires_at'] < datetime.now():
            del self.sessions[session_id]
            del self.tokens[token]
            return False
            
        return session