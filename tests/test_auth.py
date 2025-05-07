import pytest
import asyncio
from src.auth import ReticulumAuth, StorageAuth

@pytest.mark.asyncio
async def test_reticulum_auth():
    auth = ReticulumAuth()
    
    # Test authentication
    result = await auth.authenticate(
        user_id="test_user",
        scope="site:read"
    )
    
    assert result is not None
    assert 'token' in result
    assert 'session_id' in result
    
    # Test token verification
    verified = await auth.verify_token(result['token'])
    assert verified is not False
    assert verified['user_id'] == "test_user"

@pytest.mark.asyncio
async def test_storage_auth():
    auth = StorageAuth()
    
    # Test access authorization
    result = await auth.authorize_access(
        user_id="test_user",
        path="/test/path",
        mode="read"
    )
    
    assert result is not None
    assert 'token' in result
    
    # Test access validation
    valid = await auth.validate_access(
        token=result['token'],
        path="/test/path",
        mode="read"
    )
    
    assert valid is True

@pytest.mark.asyncio
async def test_invalid_token():
    auth = ReticulumAuth()
    
    # Test invalid token
    verified = await auth.verify_token("invalid_token")
    assert verified is False