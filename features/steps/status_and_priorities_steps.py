from behave import *


@given(u'the agent with username "{agent_username}" and password "{agent_password}" logs in to the Agent portal')
def login_as_agent(context, agent_username, agent_password):
    context.driver.get("https://interview2.supporthive.com/staff/")
    print("vendugundu")


@when(u'the agent creates a new {Pending} behavior status with name {StatusName} in Statuses page')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the agent creates a new {Pending} behavior status with name {StatusName} in Statuses page')


@then(u'the new status with name {StatusName} should be added to the Statuses table')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the new status with name {StatusName} should be added to the Statuses table')


@then(u'the agent creates a new {PriorityName} priority in Priorities page')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the agent creates a new {PriorityName} priority in Priorities page')


@then(u'the new priority with name {PriorityName} should be added to Priorities table')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the new priority with name {PriorityName} should be added to Priorities table')
