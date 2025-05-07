import asyncio
import json
from datetime import datetime
from ..storage.remote_storage import RemoteStorageSystem
from ..transport.secure_transport import SecureReticulumTransport

class ContentManager:
    def __init__(self):
        self.storage = RemoteStorageSystem()
        self.transport = SecureReticulumTransport()
        self.content_index = {}
        self.site_manifests = {}
        
    async def publish_site(self, site_data):
        #\"\"\"Publish website to the mesh network\"\"\"
        # Generate site ID
        site_id = self.generate_site_id(site_data)
        
        # Process and store resources
        resources = await self.process_resources(site_data.get('resources', {}))
        
        # Create site manifest
        manifest = {
            'site_id': site_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'pages': await self.process_pages(site_data.get('pages', {})),
            'resources': resources,
            'metadata': site_data.get('metadata', {})
        }
        
        # Store manifest
        await self.storage.store_data(
            f"/sites/{site_id}/manifest.json",
            json.dumps(manifest),
            {'encrypt': True}
        )
        
        # Store in index
        self.site_manifests[site_id] = manifest
        
        return {
            'site_id': site_id,
            'manifest': manifest
        }
        
    async def process_pages(self, pages):
        #\"\"\"Process and store page content\"\"\"
        processed_pages = {}
        
        for path, content in pages.items():
            # Store page content
            page_id = self.generate_content_id(content)
            stored = await self.storage.store_data(
                f"/content/{page_id}",
                content['content'],
                {
                    'encrypt': True,
                    'type': content.get('type', 'html')
                }
            )
            
            processed_pages[path] = {
                'id': page_id,
                'type': content.get('type', 'html'),
                'storage_path': stored['path']
            }
            
        return processed_pages
        
    async def process_resources(self, resources):
        #\"\"\"Process and store site resources\"\"\"
        processed_resources = {}
        
        for path, resource in resources.items():
            # Store resource
            resource_id = self.generate_content_id(resource)
            stored = await self.storage.store_data(
                f"/resources/{resource_id}",
                resource['content'],
                {
                    'encrypt': True,
                    'type': resource.get('type', 'binary')
                }
            )
            
            processed_resources[path] = {
                'id': resource_id,
                'type': resource.get('type', 'binary'),
                'storage_path': stored['path']
            }
            
        return processed_resources
        
    def generate_site_id(self, site_data):
        #\"\"\"Generate unique site ID\"\"\"
        import hashlib
        import uuid
        
        # Create unique identifier
        unique_data = f"{site_data.get('title', '')}-{uuid.uuid4()}"
        return hashlib.sha256(unique_data.encode()).hexdigest()[:16]
        
    def generate_content_id(self, content):
        #"\"\"Generate unique content ID\"\"\"
        import hashlib
        return hashlib.sha256(str(content).encode()).hexdigest()[:16]