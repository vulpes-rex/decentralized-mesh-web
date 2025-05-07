import os
import json
from datetime import datetime
from ..utils.crypto import CryptoHandler
from ..utils.sync import SyncManager

class RemoteStorageSystem:
    def __init__(self):
        self.crypto = CryptoHandler()
        self.sync = SyncManager()
        self.storage_path = "/var/mesh/storage"  # Default path
        
    async def store_data(self, path, data, options=None):
        options = options or {}
        
        # Encrypt if needed
        if options.get('encrypt', True):
            data = self.crypto.encrypt_data(data)
            
        # Generate storage path
        storage_path = os.path.join(
            self.storage_path,
            path.lstrip('/')
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        # Store data
        with open(storage_path, 'wb') as f:
            f.write(data)
            
        # Store metadata
        metadata = {
            'path': path,
            'created_at': datetime.now().isoformat(),
            'encrypted': options.get('encrypt', True),
            'version': options.get('version', 1)
        }
        
        metadata_path = f"{storage_path}.meta"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
            
        # Queue for sync if needed
        if options.get('sync', True):
            await self.sync.queue_sync({
                'id': path,
                'type': 'store',
                'timestamp': metadata['created_at']
            })
            
        return {
            'path': path,
            'metadata': metadata
        }
        
    async def retrieve_data(self, path):
        storage_path = os.path.join(
            self.storage_path,
            path.lstrip('/')
        )
        
        if not os.path.exists(storage_path):
            raise FileNotFoundError(f"No data found at {path}")
            
        # Read metadata
        metadata_path = f"{storage_path}.meta"
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        # Read data
        with open(storage_path, 'rb') as f:
            data = f.read()
            
        # Decrypt if needed
        if metadata.get('encrypted', True):
            data = self.crypto.decrypt_data(data)
            
        return {
            'data': data,
            'metadata': metadata
        }