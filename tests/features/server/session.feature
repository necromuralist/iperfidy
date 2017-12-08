Feature: A Server Session

Scenario: A server session is called
  Given valid settings and a built Server Session
  When the server session is called
  Then it creates a server
  And it adds the settings to the server
  And it runs it
  And it returns the JSON
