Feature: Server API

Scenario: start_server is called
  Given the server API
  When start_server is called
  Then it updates the state
  And starts the ServerSession
  And returns the output of the server session
