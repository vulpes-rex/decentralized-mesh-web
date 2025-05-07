import asyncio
from datetime import datetime
from ..storage.remote_storage import RemoteStorageSystem
from ..transport.secure_transport import SecureReticulumTransport
from .renderer import WebRenderer

class DecentralizedBrowser:
    def __init__(self):
        self.storage = RemoteStorageSystem()
        self.transport = SecureReticulumTransport()
        self.renderer = WebRenderer()
        self.cache = BrowserCache()
        self.history = []
        
    async def load_site(self, site_id):
        #\"\"\"Load and render website\"\"\"
        try:
            # Get site manifest
            manifest = await self.get_site_manifest(site_id)
            if not manifest:
                raise SiteNotFoundError(f"Site {site_id} not found")
                
            # Get main page content
            content = await self.get_page_content(manifest, "/index.html")
            
            # Process resources
            resources = await self.process_site_resources(manifest)
            
            # Render content
            rendered = await self.renderer.render(content, resources)
            
            # Update history
            self.update_history(site_id, manifest)
            
            return rendered
            
        except Exception as e:
            print(f"Error loading site: {e}")
            # Try loading from cache
            return await self.load_cached_site(site_id)
            
    async def get_site_manifest(self, site_id):
        #\"\"\"Get site manifest from storage\"\"\"
        try:
            manifest_data = await self.storage.retrieve_data(
                f"/sites/{site_id}/manifest.json"
            )
            return json.loads(manifest_data['data'])
        except Exception:
            return None
            
    async def get_page_content(self, manifest, path):
        #\"\"\"Get page content from storage\"\"\"
        page_info = manifest['pages'].get(path)
        if not page_info:
            raise PageNotFoundError(f"Page {path} not found")
            
        content = await self.storage.retrieve_data(
            page_info['storage_path']
        )
        
        return {
            'type': page_info['type'],
            'content': content['data']
        }
            
    async def process_site_resources(self, manifest):
        #\"\"\"Process and load site resources\"\"\"
        resources = {}
        
        for path, resource in manifest['resources'].items():
            try:
                resource_data = await self.storage.retrieve_data(
                    resource['storage_path']
                )
                resources[path] = {
                    'type': resource['type'],
                    'content': resource_data['data']
                }
            except Exception as e:
                print(f"Error loading resource {path}: {e}")
                
        return resources
        
    def update_history(self, site_id, manifest):
        #\"\"\"Update browser history\"\"\"
        self.history.append({
            'site_id': site_id,
            'title': manifest.get('metadata', {}).get('title', 'Untitled'),
            'timestamp': datetime.now().isoformat()
        })

class BrowserCache:
    def __init__(self):
        self.cache = {}
        self.max_size = 100 * 1024 * 1024  # 100MB
        
    async def store_site(self, site_id, data):
        #\"\"\"Store site data in cache\"\"\"
        self.cache[site_id] = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cleanup if needed
        await self.cleanup_cache()
        
    async def get_site(self, site_id):
        #\"\"\"Get site from cache\"\"\"
        cached = self.cache.get(site_id)
        if not cached:
            return None
            
        return cached['data']
        
    async def cleanup_cache(self):
        #\"\"\"Clean up cache if too large\"\"\"
        while self.get_cache_size() > self.max_size:
            # Remove oldest entry
            oldest = min(self.cache.items(), key=lambda x: x[1]['timestamp'])
            del self.cache[oldest[0]]
            
    def get_cache_size(self):
        #\"\"\"Calculate current cache size\"\"\"
        return sum(len(str(data['data'])) for data in self.cache.values())