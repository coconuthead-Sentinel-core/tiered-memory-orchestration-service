import os
from typing import Any, Dict, Optional

from azure.cosmos import PartitionKey, exceptions
from azure.cosmos.aio import CosmosClient

# --- Configuration ---
# Best practice: Read from environment variables.
ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
KEY = os.environ.get("COSMOS_KEY")
DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME", "SentinelForgeDB")


class CosmosDBRepository:
    """
    A repository class to encapsulate all data access logic for Azure Cosmos DB.
    Follows the singleton pattern for the CosmosClient to ensure efficient connection management.
    """

    _instance: Optional["CosmosDBRepository"] = None
    _client: Optional[CosmosClient] = None

    def __new__(cls) -> "CosmosDBRepository":
        if cls._instance is None:
            if not all([ENDPOINT, KEY]):
                raise ValueError(
                    "COSMOS_ENDPOINT and COSMOS_KEY must be set in environment variables."
                )

            cls._instance = super(CosmosDBRepository, cls).__new__(cls)
            # Best practice: Use a single client instance for the application's lifetime.
            cls._client = CosmosClient(url=ENDPOINT, credential=KEY)
        return cls._instance

    async def get_or_create_database(self) -> Any:
        """Gets or creates the database."""
        if not self._client:
            raise RuntimeError("CosmosClient is not initialized.")
        return await self._client.create_database_if_not_exists(id=DATABASE_NAME)

    async def get_or_create_container(
        self, container_name: str, partition_key: str
    ) -> Any:
        """
        Gets or creates a container. A container holds items (like rows in a table).
        The partition_key is crucial for performance and scalability.
        """
        database = await self.get_or_create_database()
        return await database.create_container_if_not_exists(
            id=container_name, partition_key=PartitionKey(path=f"/{partition_key}")
        )

    async def upsert_item(
        self, container_name: str, item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new item or updates an existing one (if the 'id' matches).
        This is the primary method for saving data.
        """
        database = await self.get_or_create_database()
        container = database.get_container_client(container_name)
        return await container.upsert_item(body=item)

    async def get_item(
        self, container_name: str, item_id: str, partition_key: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieves a single item by its ID and partition key for maximum efficiency."""
        try:
            database = await self.get_or_create_database()
            container = database.get_container_client(container_name)
            return await container.read_item(item=item_id, partition_key=partition_key)
        except exceptions.CosmosResourceNotFoundError:
            return None


# --- Data Models (Conceptual) ---
# We will store user progress in a 'UserProgress' container.
# A sample item would look like this:
# {
#     "id": "user-shannon-kelly", # Unique ID for the item
#     "userId": "shannon-kelly",   # This will be our Partition Key for efficient lookups
#     "strikes_completed": 15,
#     "mastery_level": "Ha",
#     "last_active": "2024-10-27T10:00:00Z",
#     "chat_history": [
#         {"role": "user", "content": "What is Strike 1?"},
#         {"role": "assistant", "content": "Strike 1 is Context Acquisition..."}
#     ]
# }

# Create a single instance to be used throughout the application
datastore = CosmosDBRepository()
