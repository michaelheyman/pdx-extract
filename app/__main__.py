import asyncio
from app import main

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main.run(None))
