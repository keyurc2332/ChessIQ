from sqlalchemy import text
from database import SessionLocal

db = SessionLocal()

print('=== Game Analysis Status ===\n')

# Check analyzed vs unanalyzed
result = db.execute(text('SELECT is_analyzed, COUNT(*) as count FROM games GROUP BY is_analyzed'))
for row in result:
    status = 'Analyzed' if row[0] == 1 else 'Unanalyzed'
    print(f'{status}: {row[1]} games')

print()

# Check moves count
result = db.execute(text('SELECT COUNT(*) FROM moves'))
moves_count = result.scalar()
print(f'Total moves in database: {moves_count}')

print()

# Check a sample game
result = db.execute(text('''
    SELECT game_id, is_analyzed, accuracy, avg_centipawn_loss 
    FROM games 
    LIMIT 5
'''))

print('Sample games:')
for row in result:
    print(f'  {row[0][:8]}... - Analyzed: {row[1]}, Accuracy: {row[2]}, CPL: {row[3]}')

db.close()
