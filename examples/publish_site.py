import asyncio
from src.web import ContentManager
from src.auth import ReticulumAuth

async def publish_example_site():
    # Initialize components
    content_manager = ContentManager()
    auth = ReticulumAuth()
    
    # Example site content
    site_data = {
        "title": "Example Mesh Site",
        "pages": {
            "index.html": {
                "type": "html",
                "content": """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Mesh Network Site</title>
                    <link rel="stylesheet" href="style.css">
                </head>
                <body>
                    <div class="container">
                        <h1>Welcome to Mesh Network</h1>
                        <p>This site is distributed over Reticulum/LoRa.</p>
                        <nav>
                            <a href="about.html">About</a>
                            <a href="contact.html">Contact</a>
                        </nav>
                    </div>
                </body>
                </html>
                """
            },
            "about.html": {
                "type": "markdown",
                "content": """
                # About This Site

                This is an example of a decentralized website running on:
                
                * Reticulum mesh network
                * LoRa radio
                * Distributed storage
                
                ## How it Works
                
                Content is distributed across the mesh network...
                """
            }
        },
        "resources": {
            "style.css": {
                "type": "text/css",
                "content": """
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                nav {
                    margin: 20px 0;
                }
                nav a {
                    margin-right: 10px;
                }
                """
            }
        },
        "metadata": {
            "author": "Example Author",
            "created": "2024-01-01",
            "description": "Example mesh network site"
        }
    }
    
    try:
        # Authenticate (if needed)
        auth_result = await auth.authenticate(
            user_id="example_author",
            scope="site:publish"
        )
        
        # Publish site
        result = await content_manager.publish_site(site_data)
        
        print(f"Site published successfully!")
        print(f"Site ID: {result['site_id']}")
        print(f"Access URL: mesh://{result['site_id']}")
        
        return result
        
    except Exception as e:
        print(f"Error publishing site: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(publish_example_site())

