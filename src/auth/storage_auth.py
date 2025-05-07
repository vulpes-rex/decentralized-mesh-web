from datetime import datetime, timedelta
import uuid

class StorageAuth:
    def __init__(self):
        self.permissions = {}
        self.access_tokens = {}
        
    async def authorize_access(self, user_id, path, mode='read'):
        permission_id = str(uuid.uuid4())
        permission = {
            'user_id': user_id,
            'path': path,
            'mode': mode,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=1)
        }
        
        self.permissions[permission_id] = permission
        token = await self.generate_access_token(permission)
        self.access_tokens[token] = permission_id
        
        return {
            'token': token,
            'expires_at': permission['expires_at']
        }
        
    async def generate_access_token(self, permission):
        return str(uuid.uuid4())  # In practice, use secure token generation
        
    async def validate_access(self, token, path, mode):
        if token not in self.access_tokens:
            return False
            
        permission_id = self.access_tokens[token]
        permission = self.permissions.get(permission_id)
        
        if not permission:
            return False
            
        if permission['expires_at'] < datetime.now():
            del self.permissions[permission_id]
            del self.access_tokens[token]
            return False
            
        return (permission['path'] == path and 
                permission['mode'] in ['write', 'read'] and
                (mode == 'read' or permission['mode'] == 'write'))