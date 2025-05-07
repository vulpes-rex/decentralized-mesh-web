import asyncio
from src.web import DecentralizedBrowser
from src.auth import ReticulumAuth

async def browse_example_site(site_id):
    # Initialize components
    browser = DecentralizedBrowser()
    auth = ReticulumAuth()
    
    try:
        # Optional authentication
        auth_result = await auth.authenticate(
            user_id="example_user",
            scope="site:read"
        )
        
        # Load site
        content = await browser.load_site(site_id)
        
        print("Site loaded successfully!")
        print("\\nContent preview:")
        print("=" * 40)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("=" * 40)
        
        return content
        
    except Exception as e:
        print(f"Error loading site: {e}")
        raise

if __name__ == "__main__":
    # Use site ID from publish_example_site
    SITE_ID = "your_site_id_here"
    asyncio.run(browse_example_site(SITE_ID))