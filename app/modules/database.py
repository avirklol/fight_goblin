import os
import asyncio
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        # Get MongoDB URI from environment variable or use default
        self.mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        self.client = AsyncMongoClient(self.mongo_uri)
        self.db = self.client['fight_goblin']  # Your database name

    async def insert_fight(self, fight_data: Dict) -> str:
        """Insert a single fight into the fights collection"""
        collection = self.db.fights
        result = await collection.insert_one(fight_data)
        return str(result.inserted_id)

    async def insert_event(self, event_data: Dict) -> str:
        """Insert a UFC event with all its fights"""
        collection = self.db.events
        result = await collection.insert_one(event_data)
        return str(result.inserted_id)

    async def get_event(self, event_url: str) -> Optional[Dict]:
        """Retrieve an event by its URL"""
        collection = self.db.events
        return await collection.find_one({'url': event_url})

    async def get_fight(self, fight_id: str) -> Optional[Dict]:
        """Retrieve a specific fight by ID"""
        collection = self.db.fights
        return await collection.find_one({'_id': fight_id})

    async def update_fight(self, fight_id: str, update_data: Dict) -> bool:
        """Update a fight's data"""
        collection = self.db.fights
        result = await collection.update_one(
            {'_id': fight_id},
            {'$set': update_data}
        )
        return result.modified_count > 0

    async def get_all_events(self) -> List[Dict]:
        """Retrieve all events"""
        collection = self.db.events
        return list(await collection.find())

    async def close(self):
        """Close the database connection"""
        await self.client.close()
