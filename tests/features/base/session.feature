Feature: Iperf Session

Scenario: A child session doesn't implement the settings definition
  Given a child without a settings definition
  When the child is instantiated
  Then it raises a TypeError

Scenario: A child doesn't implement the iperf definition
  Given a child without an iperf definition
  When the child is instantiated
  Then it raises a TypeError

Scenario: A child retrieves the settings
  Given a child of the iperf session
  When the settings are retrieved
  Then the expected calls are made

Scenario: A child retrieves the iperf object
  Given a child of the iperf session
  When the iperf instance is retrieved
  Then it is the expected iperf object
  And the settings were added to it

Scenario: The child is called
  Given a child of the iperf session
  When the child is called
  Then the iperf is run
  And it returns the iperf's json
