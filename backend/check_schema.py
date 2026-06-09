from sqlalchemy import text, inspect
from database import SessionLocal, engine

print('=== Database Schema ===\n')

# Get table info
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f'Tables: {tables}\n')

# Check games table columns
if 'games' in tables:
    columns = inspector.get_columns('games')
    print('Games table columns:')
    for col in columns:
        print(f'  - {col["name"]} ({col["type"]})')
    print()

# Check users table columns
if 'users' in tables:
    columns = inspector.get_columns('users')
    print('Users table columns:')
    for col in columns:
        print(f'  - {col["name"]} ({col["type"]})')
    print()

# Check moves table columns
if 'moves' in tables:
    columns = inspector.get_columns('moves')
    print('Moves table columns:')
    for col in columns:
        print(f'  - {col["name"]} ({col["type"]})')
    print()
else:
    print('Moves table: NOT FOUND\n')