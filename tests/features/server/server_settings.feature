Feature: Server Settings

Scenario: A valid JSON settings is validated
  Given a Server Settings with valid JSON
  When the JSON is validated
  Then nothing happens

Scenario: An invalid JSON settings is validated
  Given a Server Settings with invalid JSON
  When the invalid JSON is validate
  Then it raises an InvalidServerSettings error
