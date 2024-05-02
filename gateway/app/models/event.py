from datetime import datetime
from typing import Optional, Self, Annotated
from uuid import UUID

from pydantic import BaseModel, UUID4, AfterValidator, Field
from pytz import utc

from app.generated.event_service.event_service_pb2 import GrpcEvent
from app.generated.event_service.event_service_pb2 import Interval as GrpcInterval


class Interval(BaseModel):
    """
    Interval model

    Attributes
    ----------
    years : int
        Amount of years
    months : int
        Amount of months
    weeks : int
        Amount of weeks
    days : int
        Amount of days
    hours : int
        Amount of hours
    minutes : int
        Amount of minutes
    seconds : int
        Amount of seconds

    Methods
    -------
    to_proto()
        Converts the interval to proto.
    from_proto()
        Get Interval instance from proto.

    """
    years: Annotated[int, Field(0, ge=0)]
    months: Annotated[int, Field(0, ge=0)]
    weeks: Annotated[int, Field(0, ge=0)]
    days: Annotated[int, Field(0, ge=0)]
    hours: Annotated[int, Field(0, ge=0)]
    minutes: Annotated[int, Field(0, ge=0)]
    seconds: Annotated[int, Field(0, ge=0)]

    def to_proto(self) -> GrpcInterval:
        """
        Converts the interval to proto.

        Returns
        -------
        GrpcInterval
            Proto interval

        """
        return GrpcInterval(
            years=self.years,
            months=self.months,
            weeks=self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
        )

    @classmethod
    def from_proto(cls, interval: GrpcInterval) -> Self:
        """
        Get Interval instance from proto

        Parameters
        ----------
        interval : GrpcInterval
            Proto interval

        Returns
        -------
        Interval
            Interval instance

        """
        return cls(
            years=interval.years,
            months=interval.months,
            weeks=interval.weeks,
            days=interval.days,
            hours=interval.hours,
            minutes=interval.minutes,
            seconds=interval.seconds,
        )


class Event(BaseModel):
    """
    Event dataclass

    Attributes
    ----------
    id : UUID4 | str
        Event ID
    title : str
        Event title
    start : datetime
        Event start time
    end : datetime
        Event end time
    author_id : str
        Event author ID
    created_at : datetime
        Event created time
    description : Optional[str]
        Event description
    color : Optional[str]
        Event color
    repeating_delay : Optional[datetime]
        Event repeating delay
    deleted_at : Optional[datetime]
        Event deleted time

    Methods
    -------
    static from_proto(proto)
        Get Event instance from proto
    to_proto()
        Get Event proto from Event instance

    """
    id: UUID4 | Annotated[str, AfterValidator(lambda x: UUID(x, version=4))]
    title: str
    start: datetime
    end: datetime
    author_id: str
    created_at: datetime
    description: Optional[str] = None
    color: Optional[str] = None
    repeating_delay: Optional[Interval] = None
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_proto(cls, proto: GrpcEvent) -> Self:
        """
        Get Event instance from proto

        Parameters
        ----------
        proto : GrpcEvent
            Event proto

        Returns
        -------
        Event
            Event instance

        """
        return cls(
            id=proto.id,
            title=proto.title,
            start=datetime.fromtimestamp(proto.start.seconds + proto.start.nanos / 1e9),
            end=datetime.fromtimestamp(proto.end.seconds + proto.end.nanos / 1e9),
            author_id=proto.author_id,
            created_at=datetime.fromtimestamp(
                proto.created_at.seconds + proto.created_at.nanos / 1e9
            ),
            description=proto.description if proto.WhichOneof("optional_description") is not None else None,
            color=proto.color if proto.WhichOneof("optional_color") is not None else None,
            repeating_delay=Interval.from_proto(proto.repeating_delay)
            if proto.WhichOneof("optional_repeating_delay") is not None
            else None,
            deleted_at=datetime.fromtimestamp(
                proto.deleted_at.seconds + proto.deleted_at.nanos / 1e9
            )
            if proto.WhichOneof("optional_deleted_at") is not None
            else None,
        )

    def to_proto(self) -> GrpcEvent:
        """
        Get Event proto from Event instance

        Returns
        -------
        GrpcEvent
            Event proto

        """
        event = GrpcEvent(
            id=str(self.id),
            title=self.title,
            author_id=self.author_id,
            description=self.description if self.description is not None else None,
            color=self.color if self.color is not None else None,
            repeating_delay=self.repeating_delay.to_proto() if self.repeating_delay is not None else None,
        )

        event.created_at.FromDatetime(self.created_at.astimezone(utc))
        event.start.FromDatetime(self.start)
        event.end.FromDatetime(self.end)
        if self.deleted_at is not None:
            event.deleted_at.FromDatetime(self.deleted_at.astimezone(utc))

        return event
