from typing import Annotated, Self

from app.generated.interval.interval_pb2 import Interval as GrpcInterval

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field


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
        """
        Translates the interval to relative delta.

        Returns
        -------
        relativedelta
            Relative delta

        """
        return relativedelta(
            years=self.years,
            months=self.months,
            weeks=self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            raise NotImplemented

        self_dict = self.dict()
        other_dict = other.dict()

        return all([self_dict[key] == other_dict[key] for key in self.dict().keys()])
