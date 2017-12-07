Feature: Server State

Scenario: User checks on the server while it isn't running
  Given a flask test-client
  When the user checks on the server and it isn't running
  Then the response is a not-found
  And it has the expected message
