from mongoengine import StringField, ReferenceField, ListField
from panic.mongo import BaseDocument, EnumField

# Move this to a utils
def enum(name, *sequential, **named):
    values = dict(zip(sequential, range(len(sequential))), **named)

    # NOTE: Yes, we *really* want to cast using str() here.
    # On Python 2 type() requires a byte string (which is str() on Python 2).
    # On Python 3 it does not matter, so we'll use str(), which acts as
    # a no-op.
    return type(str(name), (), values)

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





