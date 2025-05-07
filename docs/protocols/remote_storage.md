# RemoteStorage Protocol Specification for Mesh Networks

## Overview
A decentralized implementation of remoteStorage protocol adapted for mesh networks using Reticulum/LoRa, providing user-owned data storage and synchronization capabilities without central servers.

## Protocol Version
- Version: 1.0
- Status: Draft
- Extensions: Mesh Network Support, Offline-First Operations

## Core Concepts

### 1. Storage Architecture
```
User Data Space
├── public/
│ ├── {module1}/
│ └── {module2}/
├── private/
│ ├── {module1}/
│ └── {module2}/
└── shared/
├── {module1}/
└── {module2}/
```


### 2. Data Categories
```python
STORAGE_CATEGORIES = {
    "public": {
        "encryption": False,
        "permissions": ["READ_ALL"],
        "sync": "broadcast"
    },
    "private": {
        "encryption": True,
        "permissions": ["OWNER_ONLY"],
        "sync": "owner_nodes"
    },
    "shared": {
        "encryption": True,
        "permissions": ["OWNER", "SPECIFIED_USERS"],
        "sync": "authorized_nodes"
    }
}
```
### Protocol Operations
1. Storage Operations
```python
STORAGE_OPERATIONS = {
    "GET": {
        "path": "/<category>/<module>/<path>",
        "headers": {
            "Authorization": "Bearer <token>",
            "If-None-Match": "<etag>"
        },
        "response": {
            "Content-Type": "application/json",
            "ETag": "<etag>",
            "Content-Length": "<length>"
        }
    },
    "PUT": {
        "path": "/<category>/<module>/<path>",
        "headers": {
            "Authorization": "Bearer <token>",
            "Content-Type": "application/json",
            "If-Match": "<etag>"
        }
    },
    "DELETE": {
        "path": "/<category>/<module>/<path>",
        "headers": {
            "Authorization": "Bearer <token>",
            "If-Match": "<etag>"
        }
    }
}
```
2. Message Formats
Storage Request
```json

{
    "type": "storage_request",
    "version": "1.0",
    "operation": "GET|PUT|DELETE",
    "path": "/<category>/<module>/<path>",
    "headers": {
        "Authorization": "Bearer <token>",
        "Content-Type": "application/json",
        "If-Match": "<etag>",
        "If-None-Match": "<etag>"
    },
    "data": "<encrypted_data>",
    "timestamp": "<iso8601_timestamp>",
    "signature": "<ed25519_signature>"
}
```

### Storage Response

```json

{
    "type": "storage_response",
    "version": "1.0",
    "status": 200,
    "headers": {
        "Content-Type": "application/json",
        "ETag": "<etag>",
        "Content-Length": "<length>"
    },
    "data": "<encrypted_data>",
    "timestamp": "<iso8601_timestamp>",
    "signature": "<ed25519_signature>"
}
```

### Synchronization Protocol
1. Change Detection
```python

class ChangeDetection:
    def __init__(self):
        self.vector_clock = VectorClock()
        self.change_log = ChangeLog()
        
    def detect_changes(self, local_state, remote_state):
        # Compare vector clocks
        if self.vector_clock.compare(local_state, remote_state):
            return self.change_log.get_changes(
                since=remote_state.timestamp
            )
```
2. Sync Message Format
```json

{
    "type": "sync_request",
    "version": "1.0",
    "vector_clock": {
        "node_id": "<timestamp>",
        "peers": {
            "<peer_id>": "<timestamp>"
        }
    },
    "changes": [
        {
            "path": "/<category>/<module>/<path>",
            "operation": "PUT|DELETE",
            "timestamp": "<iso8601_timestamp>",
            "etag": "<etag>"
        }
    ]
}
```
### Offline Support
1. Offline Storage
```python

class OfflineStorage:
    def __init__(self):
        self.local_store = LocalStore()
        self.change_queue = ChangeQueue()
        
    async def store_offline(self, operation):
        # Store operation in change queue
        await self.change_queue.add(operation)
        
        # Update local store
        await self.local_store.apply(operation)
```
2. Change Queue
```python

class ChangeQueue:
    def __init__(self):
        self.pending_changes = []
        self.applied_changes = []
        
    async def process_queue(self):
        while self.pending_changes:
            change = self.pending_changes.pop(0)
            try:
                await self.apply_change(change)
                self.applied_changes.append(change)
            except Exception as e:
                await self.handle_failed_change(change, e)
```
### Security
1. Encryption
```python

class StorageEncryption:
    def __init__(self):
        self.crypto = CryptoHandler()
        
    def encrypt_data(self, data, key):
        # Generate random IV
        iv = os.urandom(12)
        
        # Encrypt data
        encrypted = self.crypto.encrypt(data, key, iv)
        
        return {
            "iv": iv,
            "data": encrypted,
            "key_id": key.id
        }
```
2. Access Control
```python

class AccessControl:
    def __init__(self):
        self.acl = AccessControlList()
        
    def check_access(self, user, path, operation):
        category = self.get_category(path)
        module = self.get_module(path)
        
        return self.acl.check_permission(
            user=user,
            category=category,
            module=module,
            operation=operation
        )
```
### Mesh Network Integration
1. Node Discovery
```python

class StorageNodeDiscovery:
    def __init__(self):
        self.mesh = ReticulumMeshNetwork()
        
    async def announce_storage(self):
        announcement = {
            "type": "storage_node",
            "capabilities": ["store", "sync"],
            "space_available": self.get_available_space(),
            "timestamp": datetime.now().isoformat()
        }
        
        await self.mesh.announce(announcement)
```
2. Data Distribution
```python

class DataDistribution:
    def __init__(self):
        self.replication_factor = 3
        self.storage_nodes = {}
        
    async def distribute_data(self, data, path):
        # Find suitable storage nodes
        nodes = await self.find_storage_nodes(
            count=self.replication_factor
        )
        
        # Store data on each node
        results = []
        for node in nodes:
            result = await self.store_on_node(node, path, data)
            results.append(result)
            
        return results
```
### Implementation Guide
1. Storage Node Setup
```python

class StorageNode:
    def __init__(self):
        self.storage = LocalStorage()
        self.sync = SyncManager()
        self.mesh = MeshNetwork()
        
    async def initialize(self):
        # Initialize storage
        await self.storage.initialize()
        
        # Start sync manager
        await self.sync.start()
        
        # Join mesh network
        await self.mesh.join()
```
2. Client Implementation
```python

class StorageClient:
    def __init__(self):
        self.auth = ReticulumAuth()
        self.storage = RemoteStorage()
        
    async def store_data(self, path, data):
        # Get authorization
        token = await self.auth.get_token(
            scope=f"storage:write:{path}"
        )
        
        # Store data
        result = await self.storage.put(
            path=path,
            data=data,
            token=token
        )
        
        return result
```
### Error Handling
#### Error Codes
```python

STORAGE_ERRORS = {
    "STORE001": "Path not found",
    "STORE002": "Access denied",
    "STORE003": "Storage full",
    "STORE004": "Invalid data",
    "STORE005": "Sync conflict"
}
```
#### Error Response Format
```json

{
    "type": "storage_error",
    "code": "<error_code>",
    "message": "<error_message>",
    "path": "<affected_path>",
    "timestamp": "<iso8601_timestamp>"
}
```
### Testing
#### Test Categories
- Basic Storage Operations
- Sync Functionality
- Offline Operations
- Security Features
- Mesh Network Integration
Example Test
```python

@pytest.mark.asyncio
async def test_storage_operations():
    storage = RemoteStorage()
    
    # Test data storage
    test_data = {"key": "value"}
    result = await storage.put(
        path="/private/test/data",
        data=test_data
    )
    
    assert result.status == 200
    
    # Test data retrieval
    retrieved = await storage.get("/private/test/data")
    assert retrieved.data == test_data
```
#### Reference Implementation
See src/storage/remote_storage.py for the reference implementation.