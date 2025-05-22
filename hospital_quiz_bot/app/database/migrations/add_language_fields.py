"""
Migration script to add language fields to users and quiz_responses tables.
"""

import asyncio
import aiosqlite
from sqlalchemy import text
from hospital_quiz_bot.config.settings import settings

# SQL statements for adding the columns
add_language_to_users = """
ALTER TABLE users
ADD COLUMN language VARCHAR;
"""

add_language_to_quiz_responses = """
ALTER TABLE quiz_responses
ADD COLUMN language VARCHAR DEFAULT 'uk' NOT NULL;
"""

async def run_migration():
    """Run the migration to add language fields."""
    # Connect to the database
    db_path = settings.database.url.replace("sqlite:///", "")
    async with aiosqlite.connect(db_path) as db:
        # Add language column to users table
        try:
            await db.execute(add_language_to_users)
            print("Added language column to users table")
        except Exception as e:
            print(f"Error adding language column to users table: {e}")
            # Continue with other migrations if this one fails

        # Add language column to quiz_responses table
        try:
            await db.execute(add_language_to_quiz_responses)
            print("Added language column to quiz_responses table")
        except Exception as e:
            print(f"Error adding language column to quiz_responses table: {e}")
        
        # Commit the changes
        await db.commit()
        print("Migration completed successfully")

if __name__ == "__main__":
    asyncio.run(run_migration()) 