Feature: A Server Session

Scenario: A server session is created
  Given a server session
  When the attributes are retrieved
  Then the settings are server settings
  And the iperf attribute is a server
