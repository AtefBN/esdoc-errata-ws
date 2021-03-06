# -*- coding: utf-8 -*-
"""
.. module:: db.models.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - db tables.

.. moduleauthor:: Atef Bennasser <abenasser@ipsl.jussieu.fr>


"""
import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy import Enum

from errata.constants import WORKFLOW_NEW
from errata.constants import WORKFLOW_ON_HOLD
from errata.constants import WORKFLOW_RESOLVED
from errata.constants import WORKFLOW_WONT_FIX
from errata.constants import SEVERITY_LOW
from errata.constants import SEVERITY_MEDIUM
from errata.constants import SEVERITY_HIGH
from errata.constants import SEVERITY_CRITICAL
from errata.constants import STATE_CLOSED
from errata.constants import STATE_OPEN
from errata.db.utils import Entity



# Database schema.
_SCHEMA = 'errata'

# Issue workflow enumeration.
_WORKFLOW_ENUM = Enum(
    WORKFLOW_NEW,
    WORKFLOW_ON_HOLD,
    WORKFLOW_RESOLVED,
    WORKFLOW_WONT_FIX,
    schema=_SCHEMA,
    name="IssueWorkflowEnum"
    )

# Issue severity enumeration.
_SEVERITY_ENUM = Enum(
    SEVERITY_LOW,
    SEVERITY_MEDIUM,
    SEVERITY_HIGH,
    SEVERITY_CRITICAL,
    schema=_SCHEMA,
    name="IssueSeverityEnum"
    )

# Issue state enumeration.
_STATE_ENUM = Enum(
    STATE_CLOSED,
    STATE_OPEN,
    schema=_SCHEMA,
    name="IssueStateEnum"
    )


class Issue(Entity):
    """An issue raised by an institute post-publication.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_issue'
    __table_args__ = (
        {'schema': _SCHEMA}
    )

    # Column definitions.
    project = Column(Unicode(63), nullable=False)
    institute = Column(Unicode(63), nullable=False)
    uid = Column(Unicode(63), nullable=False, unique=True, default=uuid.uuid4())
    title = Column(Unicode(255), nullable=False)
    description = Column(Text, nullable=False)
    state = Column(_STATE_ENUM, nullable=False)
    severity = Column(_SEVERITY_ENUM, nullable=False)
    workflow = Column(_WORKFLOW_ENUM, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime)
    date_closed = Column(DateTime)
    url = Column(Unicode(1023))
    materials = Column(Text)

    def __repr__(self):
        return "<Issue(id={0}, uid={1}, title={2}, description=={3})>".format(self.id, self.uid, self.title,
                                                                              self.description)
# NON_CHANGEABLE_KEYS = ['title', 'project', 'institute', 'date_created', 'date_updated']

    def update_issue(self, other):
        if self.description != other.description:
            self.description = other.description
        elif self.severity != other.severity:
            self.severity = other.severity
        elif self.workflow != other.workflow:
            self.workflow = other.workflow
        elif self.materials != other.materials:
            self.materials = other.materials
        elif self.state != other.state:
            self.state = other.state
        elif self.url != other.url:
            self.url = other.url
        elif self.date_updated != other.date_updated:
            self.date_updated = other.date_updated
        elif self.date_closed != other.date_closed:
            self.date_closed = other.date_closed


class IssueDataset(Entity):
    """Associates an issue with a dataset.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_issue_dataset'
    __table_args__ = (
        UniqueConstraint('issue_id', 'dataset_id'),
        {'schema': _SCHEMA}
    )

    # Column definitions.
    issue_id = Column(
        Integer, ForeignKey('{}.tbl_issue.id'.format(_SCHEMA)), nullable=False)
    dataset_id = Column(Unicode(1023), nullable=False, index=True)
