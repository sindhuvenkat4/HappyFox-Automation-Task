from behave import *

from page_objects.login_page import LoginPage
from page_objects.new_ticket_page import NewTicketPage
from page_objects.priorities_page import PrioritiesPage
from page_objects.statuses_page import StatusesPage
from page_objects.ticket_detail_page import TicketDetailPage
from page_objects.tickets_page import TicketsPage


@given(u'marks "{status_name}" status as default')
def mark_default_status(context, status_name):
    StatusesPage(context.driver) \
        .navigate_to_statuses_page() \
        .mark_status_as_default(status_name)
    context.default_status = status_name


@given(u'marks "{priority_name}" priority as default')
def mark_default_priority_and_logout(context, priority_name):
    PrioritiesPage(context.driver) \
        .navigate_to_priorities_page() \
        .mark_priority_as_default(priority_name) \
        .logout()
    context.default_priority = priority_name


@when(u'the customer creates a new ticket on support center')
def create_new_ticket(context):
    ticket_title = "Unable to login to Portal"
    NewTicketPage(context.driver) \
        .create_new_ticket(ticket_title, "I'm not able to login. Says my account is invalid!", "HappyFoxBot",
                           "seleniumbot@happyfox.com")
    context.ticket_title = ticket_title


@then(u'the new ticket should be created with marked default status and priority on agent portal')
def check_default_status_priority_in_new_ticket(context):
    LoginPage(context.driver) \
        .login(context.agent_username, context.agent_password) \
        .navigate_to_page_from_nav_bar("Tickets")
    TicketsPage(context.driver) \
        .check_ticket_status_by_title(context.ticket_title, context.default_status) \
        .check_ticket_priority_by_title(context.ticket_title, context.default_priority)


@when(u'the agent replies to the ticket using canned response, "{canned_action_name}"')
def reply_to_ticket_with_canned_response(context, canned_action_name):
    TicketsPage(context.driver)\
        .open_ticket_by_title(context.ticket_title)
    TicketDetailPage(context.driver) \
        .check_ticket_status(context.default_status) \
        .check_ticket_priority(context.default_priority) \
        .reply_with_canned_response(context, canned_action_name)


@then(u'the ticket properties, "Status", "Priority" and "Tags" gets changed')
def check_status_priority_tags_gets_changed_as_canned_action(context):
    TicketDetailPage(context.driver) \
        .check_ticket_status(context.canned_response_status) \
        .check_ticket_priority(context.canned_response_priority) \
        .check_tags(context.canned_response_tag) \
        .logout()
