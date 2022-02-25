import asyncio
from database.base import get_test_database

asyncio.run(get_test_database())
