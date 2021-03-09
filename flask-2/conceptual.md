### Conceptual Exercise

Answer the following questions below:

- What is RESTful routing?  
  standardized way of structuring routes that is not enforced by code, but is industry standard to make it easier to read and find routes.

- What is a resource?  
  object that comes after base url in restful routes, which is based on instance/methods in OO

- When building a JSON API why do you not include routes to render a form that when submitted creates a new user?  
  typically a form would be used to create a user object.  no objects in JSON.  requires extra steps (jsonify, serialization)

- What does idempotent mean? Which HTTP verbs are idempotent?  
  it can be done repeatedly with the same data and the results will be the same as if it was done once.  GET, PUT, PATCH, DELETE

- What is the difference between PUT and PATCH?  
  PUT updates entire resource, PATCH updates part of it

- What is one way encryption?  
  hashing a password so that it can't be reverse engineered.

- What is the purpose of a `salt` when hashing a password?  
  it ensures that two people with the same password will have different hashed results.

- What is the purpose of the Bcrypt module?  
  primary purpose is to create hashed passwords.  as a bonus, it also has built in methods for adding salt and authenticating logins

- What is the difference between authorization and authentication?  
  authorization is permission to do something, authentication is proving that someone is who they say they are