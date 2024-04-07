from sqlalchemy import create_engine

engine = create_engine('postgresql:///boardmarket')

try:
    connection = engine.connect()
    print("Connection to database was successful!")
except Exception as e:
    print("Failed to connect to database.")
    print(e)
finally:
    connection.close()