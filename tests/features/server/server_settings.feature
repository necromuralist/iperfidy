Feature: Server Settings

Scenario: A valid JSON settings is validated
  Given a Server Settings with valid JSON
  When the JSON is validated
  Then nothing happens

Scenario: An invalid JSON settings is validated
  Given a Server Settings with invalid JSON
  When the invalid JSON is validated
  Then it raises an InvalidServerSettings error

Scenario: An iperf object is passed to the settings
  Given a Server Settings with valid JSON
  When the Settings object is passed an iperf object
  Then it validates the settings
  And transfers the settings to the iperf object

Scenario: An iperf object is passed to partial settings
  Given a Server Settings with an empty bind-address
  When the invalid JSON is validated
  Then it raises an InvalidServerSettings error
