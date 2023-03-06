Feature: Verify the behavior of custom statuses and priorities

  @AddStatusAndPriority
  Scenario: Agent should be able to create status and priority
    Given the agent with username "Agent" and password "Agent@123" logs in to the Agent portal
    When the agent creates a new "Pending" behavior status with name "Issue created" in Statuses page
    Then the new status with name "Issue created" should be added to the Statuses table
    And the agent creates a new priority with name "Assistance required" and description "Priority of the newly created tickets" in Priorities page
    Then the new priority with name "Assistance required" should be added to Priorities table

  @NewTicketWithDefaultStatusAndPriority
  Scenario: New ticket should always be created with default status and priority
    Given the agent with username "Agent" and password "Agent@123" logs in to the Agent portal
    And marks "Issue created" status as default
    And marks "Assistance required" priority as default
    When the customer creates a new ticket on support center
    Then the new ticket should be created with marked default status and priority on agent portal
    When the agent replies to the ticket using canned response, "Reply to Customer Query"
    Then the ticket properties, "Status", "Priority" and "Tags" gets changed

    @RemoveStatusAndPriority
    Scenario: Agent should be able to Delete the custom status and priority
      Given the agent with username "Agent" and password "Agent@123" logs in to the Agent portal
      When the agent removes the status "Issue created"
      Then the status should be deleted and should no longer be displayed on the statuses table
      When the agent removes the priority "Assistance required"
      Then the priority should be deleted and should no longer be displayed on the priorities table


