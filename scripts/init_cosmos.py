import os
import sys
from pathlib import Path

from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

ENDPOINT = os.getenv("COSMOS_ENDPOINT")
KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "SentinelForgeDB")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "Items")


def init_db():
    if not ENDPOINT or not KEY:
        print("❌ Error: COSMOS_ENDPOINT or COSMOS_KEY not set in .env")
        return

    print(f"🚀 Initializing Cosmos DB at {ENDPOINT}...")

    try:
        client = CosmosClient(ENDPOINT, credential=KEY)

        # 1. Create Database
        db = client.create_database_if_not_exists(id=DATABASE_NAME)
        print(f"   ✅ Database '{DATABASE_NAME}' ready.")

        # 2. Create Container
        # We use /partitionKey as the partition key path based on backend/api.py logic
        container = db.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/partitionKey"),
            offer_throughput=400,
        )
        print(f"   ✅ Container '{CONTAINER_NAME}' ready (PK: /partitionKey).")

    except exceptions.CosmosHttpResponseError as e:
        print(f"   ❌ Cosmos DB Error: {e.message}")
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")


if __name__ == "__main__":
    init_db()
