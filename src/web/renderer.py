import asyncio
from bs4 import BeautifulSoup
import markdown2

class WebRenderer:
    def __init__(self):
        self.processors = {
            'html': self.process_html,
            'markdown': self.process_markdown,
            'text': self.process_text
        }
        
    async def render(self, content, resources=None):
        #\"\"\"Render content based on type\"\"\"
        content_type = content.get('type', 'html')
        processor = self.processors.get(content_type, self.process_text)
        
        # Process main content
        processed_content = await processor(content['content'])
        
        # Process resources if present
        if resources:
            processed_content = await self.inject_resources(
                processed_content,
                resources
            )
            
        return processed_content
        
    async def process_html(self, content):
        #\"\"\"Process HTML content\"\"\"
        if isinstance(content, bytes):
            content = content.decode('utf-8')
            
        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Process elements
        await self.process_elements(soup)
        
        return str(soup)
        
    async def process_markdown(self, content):
        #\"\"\"Process Markdown content\"\"\"
        if isinstance(content, bytes):
            content = content.decode('utf-8')
            
        # Convert to HTML
        html = markdown2.markdown(content)
        
        # Process as HTML
        return await self.process_html(html)
        
    async def process_text(self, content):
        #\"\"\"Process plain text content\"\"\"
        if isinstance(content, bytes):
            content = content.decode('utf-8')
            
        # Wrap in basic HTML
        html = f"<pre>{content}</pre>"
        return html
        
    async def process_elements(self, soup):
        #\"\"\"Process HTML elements\"\"\"
        # Process images
        for img in soup.find_all('img'):
            await self.process_image(img)
            
        # Process links
        for link in soup.find_all('a'):
            await self.process_link(link)
            
        # Process styles
        for style in soup.find_all('link', rel='stylesheet'):
            await self.process_style(style)
            
    async def inject_resources(self, content, resources):
        #\"\"\"Inject resources into content\"\"\"
        soup = BeautifulSoup(content, 'html.parser')
        
        # Inject styles
        for path, resource in resources.items():
            if resource['type'] == 'text/css':
                style = soup.new_tag('style')
                style.string = resource['content'].decode('utf-8')
                soup.head.append(style)
                
        return str(soup)