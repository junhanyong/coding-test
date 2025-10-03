Jelper Club Coding Test

Task: Create a Todo list API handling CRUD operations using FastAPI and SQLAlchemy, with SQLite for the database. 

CRUD Operations:
1. create_todo: User inputs the title for the Todo, and an entry for Todo is created in the DB where the ID and completion status of the entry are automatically set. 
   
2.1 read_todo: User inputs an ID, and the Todo entry is returned.

2.2 read_todos: All the entries in the DB are returned.

3. update_todo: User inputs an ID, and the boolean value for whether the Todo is completed is updated to "True".
  
4. delete_todo: User inputs an ID, and the corresponding entry in the DB is deleted.

For the the RUD operations, a HTTPS 404 error response is sent back to the client in the event where the user input ID does not exist.

Video demonstration: https://youtu.be/R3JsEXgcrJM
