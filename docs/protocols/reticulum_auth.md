# ReticulumAuth Protocol Specification

## Overview
ReticulumAuth is a decentralized authentication protocol designed for mesh networks using Reticulum. It provides secure authentication and authorization without requiring centralized servers.

## Protocol Version
- Version: 1.0
- Status: Draft

## Core Concepts

### 1. Identity
- Each node maintains a unique identity derived from a public/private key pair
- Identity format: `<public_key_hash>.<node_id>`
- Identities are self-sovereign and cryptographically verifiable

### 2. Authentication Flow
Client Authenticating Node
| |
|--- 1. Authentication Request ------------------------->|
| {id, nonce, timestamp, signature} |
| |
|<-- 2. Challenge --------------------------------------|
| {challenge_data, challenge_nonce} |
| |
|--- 3. Challenge Response ---------------------------- >|
| {response, signature} |
| |
|<-- 4. Auth Token ------------------------------------|
| {token, expires_at, permissions} |

### 3. Message Formats

#### Authentication Request
```json
{
    "type": "auth_request",
    "version": "1.0",
    "data": {
        "id": "<node_identity>",
        "nonce": "<random_32_bytes>",
        "timestamp": "<iso8601_timestamp>",
        "scope": ["requested:scope", "another:scope"]
    },
    "signature": "<ed25519_signature>"
}
```

#### Challenge
```json
{
    "type": "auth_challenge",
    "version": "1.0",
    "data": {
        "challenge": "<random_challenge_data>",
        "nonce": "<random_32_bytes>",
        "timestamp": "<iso8601_timestamp>"
    },
    "signature": "<ed25519_signature>"
}
```

#### Challenge Response
```json
{
    "type": "challenge_response",
    "version": "1.0",
    "data": {
        "response": "<challenge_solution>",
        "nonce": "<original_nonce>",
        "timestamp": "<iso8601_timestamp>"
    },
    "signature": "<ed25519_signature>"
}
```

#### Auth Token
```json
{
    "type": "auth_token",
    "version": "1.0",
    "data": {
        "token": "<encrypted_token_data>",
        "expires_at": "<iso8601_timestamp>",
        "permissions": ["granted:scope"],
        "refresh_token": "<encrypted_refresh_token>"
    },
    "signature": "<ed25519_signature>"
}
```

### Security Considerations

1. Cryptographic Requirements
- All signatures must use Ed25519
- All encryption must use ChaCha20-Poly1305
- Nonces must be cryptographically random
- Timestamps must be within 5 minutes of current time

2. Token Security
- Tokens are encrypted using ChaCha20-Poly1305
- Token lifetime should not exceed 24 hours
- Refresh tokens may be valid for up to 30 days
- All tokens must include:
- Issuer identity
- Subject identity
- Issuance timestamp
- Expiration timestamp
- Granted permissions
- Cryptographic signature

3. Permission Scopes
```python
STANDARD_SCOPES = {
    "auth:basic": "Basic authentication",
    "auth:refresh": "Ability to refresh tokens",
    "storage:read": "Read from storage",
    "storage:write": "Write to storage",
    "site:publish": "Publish website content",
    "site:update": "Update existing content"
}
```
### Implementation Guide

1. Node Setup
```python

class ReticulumAuthNode:
    def __init__(self):
        self.identity = self.generate_identity()
        self.key_pair = self.generate_keypair()
        self.storage = TokenStorage()
        
    def generate_identity(self):
        # Generate node identity
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        node_id = hash(public_key.public_bytes())
        return f"{node_id}.{random_node_suffix()}"

```

2. Authentication Implementation

```python
class AuthenticationHandler:
    async def handle_auth_request(self, request):
        # Verify request signature
        if not self.verify_signature(request):
            raise InvalidSignatureError()
            
        # Generate challenge
        challenge = self.generate_challenge()
        
        # Store challenge for verification
        await self.store_challenge(request.id, challenge)
        
        return self.create_challenge_response(challenge)
        
    async def handle_challenge_response(self, response):
        # Verify challenge solution
        if not await self.verify_challenge(response):
            raise InvalidChallengeError()
            
        # Generate auth token
        token = await self.generate_auth_token(response.id)
        
        return self.create_token_response(token)
```

3. Token Management

```python
class TokenManager:
    def generate_token(self, subject, permissions):
        token_data = {
            "sub": subject,
            "iss": self.node_id,
            "iat": current_timestamp(),
            "exp": current_timestamp() + TOKEN_LIFETIME,
            "perms": permissions
        }
        
        # Encrypt and sign token
        encrypted = self.encrypt_token(token_data)
        signature = self.sign_token(encrypted)
        
        return {
            "token": encrypted,
            "signature": signature
        }
```

### Error Handling
#### Error Codes
```python
AUTH_ERRORS = {
    "AUTH001": "Invalid signature",
    "AUTH002": "Invalid challenge response",
    "AUTH003": "Token expired",
    "AUTH004": "Invalid permissions",
    "AUTH005": "Rate limit exceeded"
}
```

### Error Response Format

```json
{
    "type": "auth_error",
    "code": "<error_code>",
    "message": "<error_message>",
    "timestamp": "<iso8601_timestamp>"
}
```

### Example Usage
#### Authentication Request

```python
async def authenticate_node():
    # Create authentication request
    request = create_auth_request(
        identity=node.identity,
        scope=["storage:read", "site:publish"]
    )
    
    # Send request and handle challenge
    challenge = await send_auth_request(request)
    response = solve_challenge(challenge)
    
    # Get auth token
    token = await send_challenge_response(response)
    
    return token
```

### Protocol Extensions
1. Peer Validation
Optional extension for peer-to-peer trust validation:

```python
class PeerValidation:
    def validate_peer(self, peer_id, proof):
        # Verify peer's proof of identity
        if not self.verify_peer_proof(peer_id, proof):
            raise InvalidPeerError()
            
        # Add to trusted peers
        self.trusted_peers.add(peer_id)
```

2. Group Authentication
Support for group-based authentication:

```python
class GroupAuth:
    def create_group(self, name, members):
        group_id = generate_group_id()
        group_key = generate_group_key()
        
        return {
            "id": group_id,
            "key": group_key,
            "members": members
        }
```

### Testing
#### Test Vectors

```python
TEST_VECTORS = {
    "challenge": {
        "input": "test_challenge_data",
        "expected": "expected_response"
    },
    "signature": {
        "message": "test_message",
        "key": "test_key",
        "expected": "expected_signature"
    }
}
```
### Reference Implementation
See src/auth/reticulum_auth.py for the reference implementation.

