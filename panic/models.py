from mongoengine import StringField, ReferenceField, ListField, EmailField, DateTimeField

from .mongo import BaseDocument, EnumField
from .utils import enum

IncidentRoles = enum('IncidentRoles', COMMANDER='commander',
                     COMMUNICATIONS='communications',
                     TEAM_MEMBER='team_member')


class Organization(BaseDocument):

    name = StringField()


class Project(BaseDocument):

    name = StringField()
    organization = ReferenceField('Organization')


class User(BaseDocument):

    name = StringField()
    email = StringField()
    organization = ReferenceField('Organization')


class Incident(BaseDocument):

    name = StringField()
    project = ReferenceField('Project')
    severity = EnumField(('high', 'medium', 'low'))

    # Curious if this is the best way to do this.  Maybe we should
    # have a UserRole object.  So an incident has many UserRoles
    # and a UserRole says what role the user plays in the incident
    incident_commander = ReferenceField('User')
    communications = ReferenceField('User')
    team = ListField(ReferenceField('User'))
    sit_rep = ListField(ReferenceField('SituationReport'))

    start_time = DateTimeField()
    resolution_time = DateTimeField


class SituationReport(BaseDocument):
    """ A good sitrep provides information to active incident responders, helps new responders get quickly up to date
    about the situation, and gives context to other observers like customer support staff.

    The Content should markdown friendly
    """
    content = StringField()
    author = ReferenceField('User')


class Update(BaseDocument):
    """
    An Incident has many updates -- which are communications that go to users that are observing the projects
    """
    message = StringField()
    incident = ReferenceField('Incident')
    author = ReferenceField('User')


class Subscriber(BaseDocument):
    """Represents a user who is interested in getting updates about a certain project"""
    meta = {'allow_inheritance': True}
    project = ReferenceField('Project')


class EmailSubscriber(Subscriber):
    email = EmailField()


# class SMSSubscriber(Subscriber):
#     telephone_number = StringField()

# class SlackSubscriber(Subscriber)
#


