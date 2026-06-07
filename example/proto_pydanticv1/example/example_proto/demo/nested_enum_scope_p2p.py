# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 1.10.7
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class VehiclePosition(BaseModel):
    """
    Reproduces sibling nested enum references used by nested messages.
    """

    class CarriageDetails(BaseModel):
        class Config:
            validate_all = True

        id: str = Field(default="")
        occupancy_status: "VehiclePosition.OccupancyStatus" = Field(default=0)

    class OccupancyStatus(IntEnum):
        EMPTY = 0
        MANY_SEATS_AVAILABLE = 1
        FEW_SEATS_AVAILABLE = 2

    class Config:
        validate_all = True

    occupancy_status: "VehiclePosition.OccupancyStatus" = Field(default=0)
    multi_carriage_details: typing.List["VehiclePosition.CarriageDetails"] = Field(default_factory=list)


class FeedMessage(BaseModel):
    vehicle: VehiclePosition = Field(default_factory=VehiclePosition)
