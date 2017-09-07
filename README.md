# feed-ninja
A feed aggregator webservice with full unicode support, Build using Python + Django.

Features:
- Uses asyncio and aiohttp to download feeds asynchronously from a number of blogs.
- Uses feedparser to parse the downloaded feeds.
- Uses Django Rest Framework to serialize the send the response.
- User Authentication using JSON Web Tokens.
