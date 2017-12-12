Feature: Server API

Scenario: The queue_server is called
  Given the server API
  When the queue_server is called
  Then it starts the server
  And stores the id in redis
  And returns the expected response

Scenario: start_server is called
  Given the server API
  When start_server is called
  Then it updates the state
  And starts the ServerSession
  And returns the output of the server session
