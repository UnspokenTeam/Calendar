from typing import Self, Annotated
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field
from app.generated.interval.interval_pb2 import Interval as GrpcInterval


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

    def to_relative_delta(self) -> relativedelta:
        return relativedelta(
            years=self.years,
            months=self.months,
            weeks=self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds
        )
