### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?  
  open source program that allows us to create and modify SQL databases.

- What is the difference between SQL and PostgreSQL?  
  SQL is the language for querying databases, postgreSQL is the program that we access those databases through

- In `psql`, how do you connect to a database?  
  psql db_name, or \c db_name depending on where you are connecting from

- What is the difference between `HAVING` and `WHERE`?  
  having is used in aggregate functions

- What is the difference between an `INNER` and `OUTER` join?  
  inner only includes the rows that match on both tables, outer includes all rows from one or both tables

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?  
  left shows all rows from the first table, right shows all rows from the second

- What is an ORM? What do they do?  
  object relational mapper.  they use models in a programming language to work with database tables

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?  
  server side is necessary if same-origin policy, easier for server to store and process data, more secure if password is required.

- What is CSRF? What is the purpose of the CSRF token?  
  cross-site request forgery.  it verifies that post data came from the correct form and not through some sort of hack attempt

- What is the purpose of `form.hidden_tag()`?  
  it hides a form element, particularly the CSRF token