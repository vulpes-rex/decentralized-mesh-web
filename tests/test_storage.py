import pytest
import asyncio
from src.storage import RemoteStorageSystem, DistributedStorageManager

@pytest.mark.asyncio
async def test_remote_storage():
    storage = RemoteStorageSystem()
    
    # Test data storage
    test_data = b"Test content"
    result = await storage.store_data(
        path="/test/file.txt",
        data=test_data,
        options={'encrypt': True}
    )
    
    assert result is not None
    assert 'path' in result
    
    # Test data retrieval
    retrieved = await storage.retrieve_data("/test/file.txt")
    assert retrieved is not None
    assert retrieved['data'] == test_data

@pytest.mark.asyncio
async def test_distributed_storage():
    storage = DistributedStorageManager()
    
    # Test distributed storage
    test_data = b"Distributed test content"
    result = await storage.store_distributed(
        key="test_key",
        data=test_data,
        options={'replication_factor': 3}
    )
    
    assert result is not None
    assert 'stored_copies' in result
    assert result['stored_copies'] > 0
    
    # Test distributed retrieval
    retrieved = await storage.retrieve_distributed("test_key")
    assert retrieved == test_data

@pytest.mark.asyncio
async def test_storage_errors():
    storage = RemoteStorageSystem()
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        await storage.retrieve_data("/nonexistent/file.txt")