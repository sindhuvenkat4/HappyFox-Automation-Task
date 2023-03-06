from behave import *

from page_objects.login_page import LoginPage
from page_objects.priorities_page import PrioritiesPage
from page_objects.statuses_page import StatusesPage


@given(u'the agent with username "{agent_username}" and password "{agent_password}" logs in to the Agent portal')
def login_as_agent(context, agent_username, agent_password):
    LoginPage(context.driver).login(agent_username, agent_password)
    context.agent_username = agent_username
    context.agent_password = agent_password


@when(u'the agent creates a new "{status_behaviour}" behavior status with name "{status_name}" in Statuses page')
def create_status(context, status_behaviour, status_name):
    statuses_page = StatusesPage(context.driver) \
        .navigate_to_statuses_page() \
        .add_status(status_name, status_behaviour)
    context.statuses_page = statuses_page


@then(u'the new status with name "{status_name}" should be added to the Statuses table')
def check_new_status_is_added(context, status_name):
    context.statuses_page.check_status_is_displayed_in_table(status_name)


@then(
    u'the agent creates a new priority with name "{priority_name}" and description "{description}" in Priorities page')
def create_priority(context, priority_name, description):
    priorities_page = PrioritiesPage(context.driver) \
        .navigate_to_priorities_page() \
        .add_priority(priority_name, description)
    context.priorities_page = priorities_page


@then(u'the new priority with name "{priority_name}" should be added to Priorities table')
def check_new_priority_is_added(context, priority_name):
    context.priorities_page.check_priorities_table_has_priority(priority_name) \
        .logout()


@when(u'the agent removes the status "{status_name}"')
def remove_status(context, status_name):
    StatusesPage(context.driver) \
        .navigate_to_statuses_page() \
        .remove_status(status_name)
    context.removed_status = status_name


@then(u'the status should be deleted and should no longer be displayed on the statuses table')
def check_status_is_not_displayed(context):
    StatusesPage(context.driver) \
        .check_status_is_not_displayed_in_table(context.removed_status)


@when(u'the agent removes the priority "{priority_name}"')
def remove_priority(context, priority_name):
    PrioritiesPage(context.driver) \
        .navigate_to_priorities_page() \
        .remove_priority(priority_name)
    context.removed_priority = priority_name


@then(u'the priority should be deleted and should no longer be displayed on the priorities table')
def check_priority_is_not_displayed(context):
    PrioritiesPage(context.driver) \
        .check_priority_is_not_displayed_in_table(context.removed_priority) \
        .logout()
