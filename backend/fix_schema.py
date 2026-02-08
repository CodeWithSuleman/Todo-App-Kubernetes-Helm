"""
Quick script to fix the database schema for UUID types
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Drop all tables and recreate with correct UUID types
    conn.execute(text("DROP TABLE IF EXISTS message CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS conversation CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS todos CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))

    # Recreate users table with UUID
    conn.execute(text("""
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255),
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Recreate todos table with UUID
    conn.execute(text("""
        CREATE TABLE todos (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES users(id),
            title VARCHAR(255) NOT NULL,
            description VARCHAR(1000),
            completed BOOLEAN DEFAULT FALSE,
            priority VARCHAR(20) DEFAULT 'medium',
            due_date VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Recreate conversation table
    conn.execute(text("""
        CREATE TABLE conversation (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES users(id),
            title VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Recreate message table
    conn.execute(text("""
        CREATE TABLE message (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES users(id),
            conversation_id UUID NOT NULL REFERENCES conversation(id),
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Create indexes
    conn.execute(text("CREATE INDEX idx_todo_user_id ON todos(user_id)"))
    conn.execute(text("CREATE INDEX idx_todo_completed ON todos(completed)"))
    conn.execute(text("CREATE INDEX idx_todo_created_at ON todos(created_at)"))
    conn.execute(text("CREATE INDEX idx_todo_user_completed ON todos(user_id, completed)"))

    conn.commit()
    print("All tables recreated with UUID type")

print("Database schema fixed successfully!")
