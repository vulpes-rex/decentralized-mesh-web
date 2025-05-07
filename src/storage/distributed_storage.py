import asyncio
from datetime import datetime

class DistributedStorageManager:
    def __init__(self):
        self.peers = {}
        self.content_index = {}
        self.replication_factor = 3
        
    async def store_distributed(self, key, data, options=None):
        options = options or {}
        
        # Find suitable peers
        peers = await self.find_storage_peers(
            count=options.get('replication_factor', self.replication_factor)
        )
        
        # Store on each peer
        results = []
        for peer in peers:
            try:
                result = await self.store_on_peer(peer, key, data)
                results.append(result)
            except Exception as e:
                print(f"Failed to store on peer {peer}: {e}")
                
        # Update content index
        self.content_index[key] = {
            'peers': [p.id for p in peers],
            'timestamp': datetime.now().isoformat(),
            'size': len(data)
        }
        
        return {
            'key': key,
            'stored_copies': len(results),
            'peers': [p.id for p in peers]
        }
        
    async def retrieve_distributed(self, key):
        if key not in self.content_index:
            raise KeyError(f"Content {key} not found")
            
        peer_ids = self.content_index[key]['peers']
        
        # Try each peer until successful
        for peer_id in peer_ids:
            try:
                peer = self.peers.get(peer_id)
                if peer:
                    data = await self.retrieve_from_peer(peer, key)
                    return data
            except Exception as e:
                continue
                
        raise Exception(f"Failed to retrieve {key} from any peer")