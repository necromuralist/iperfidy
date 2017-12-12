Feature: Server State

Scenario: User checks on the server and the job doesn't exist
  Given a flask test-client
  When the user checks on the server with a bad UUID
  Then the response is a not-found
  And it has the expected uuid
  And it has the expected ready state
  And it has the expected result
  And it has the expected state

Scenario: User checks on the server and the job failed
  Given a flask test-client
  When the user checks on a failed job
  Then the response is an error
  And it has the expected uuid
  And it has the expected ready state
  And it has the expected result
  And it has the expected state

Scenario: User checks on the server and it didn't fail
  Given a flask test-client
  When the user checks on a running or completed job
  Then the response is okay
  And it has the expected state
  And it has the expected uuid
  And it has the expected ready state
  And it has the expected result

