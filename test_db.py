from sqlalchemy import create_engine

# IMPORTANT: Replace YOUR_PASSWORD with your actual postgres password
DATABASE_URL = "postgresql://postgres:Gauranshi604#@localhost:5432/governance_db"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()
except Exception as e:
    print("Error connecting to database:")
    print(e)