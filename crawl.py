import asyncio, httpx, selectolax
from urllib.parse import urlparse, urljoin #bc httpx sucks
from selectolax.parser import HTMLParser


url = "https://github.com/?scrlybrkr=a8b9d5e3" 

#check if urls exist because it would suck if it didntt exist
def check(url):
    if not url or url == "None":
        
        return False # returns false        
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc # Because who needs reabadililility?

visited = set()  # because memory is a thing

async def crawl(url, depth):
    if depth <= 0:
        return  # recursion ends here. like my patience.

    if url in visited:
        return  # already been here. deja vu.

    visited.add(url)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
        except Exception as e:
            print(f"Request failed for {url}: {e}")
            return

        if response.status_code == 200:
            tree = HTMLParser(response.text)
            for node in tree.css('a'):
                href = node.attributes.get('href')
                full_url = urljoin(url, href)
                if check(full_url):
                    print(full_url)
                    await crawl(full_url, depth - 1)  # go deeper. but not too deep.
        else:
            print(f"There was an error getting {url} (code: {response.status_code})")

async def fetch(url):
    
    async with httpx.AsyncClient() as client: # async request. you dont know how long it took me to figure out that 'await' goes inside the variable -_-

        response = await client.get(url)
        
        if response.status_code == 200:
            tree = HTMLParser(response.text) # parses html
            crawl(tree, url)
            
        else:
            print(f"There was an error getting the URL (code: {response.status_code})")
            # so you can figure out what error you got via useless numbers
            # because why not?

asyncio.run(crawl("https://github.com/?scrlybrkr=a8b9d5e3", depth=2))  # depth = how brave you feel
