Feature: Verify the behavior of custom statuses and priorities

  @AddStatusAndPriority
  Scenario: Agent should be able to create status and priority
    Given the agent with username "Agent" and password "Agent@123" logs in to the Agent portal
    When the agent creates a new {Pending} behavior status with name {StatusName} in Statuses page
    Then the new status with name {StatusName} should be added to the Statuses table
    And the agent creates a new {PriorityName} priority in Priorities page
    Then the new priority with name {PriorityName} should be added to Priorities table

