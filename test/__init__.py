from app.session import SessionStore

session = SessionStore()

session.initialize_connection()

session.add_interaction("token","hello,server","hello,client")
session.add_interaction("token","hello,server1","hello,client1")
data =  session.get_interaction("token")

print(data['requests'][1])