# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[0.0.0](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.5.3
import typing
from datetime import datetime

from google.protobuf.message import Message  # type: ignore
from pydantic import Field, model_validator

from example.populate_by_name_plugin_config import MyBaseSchema
from protobuf_to_pydantic.customer_validator import check_one_of


class GeoLocation(MyBaseSchema):
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)
    altitude_meters: typing.Optional[float] = Field(default=0.0)


class ReportData(MyBaseSchema):
    """
    Annotations are used in runtime mode
    """

    _one_of_dict = {
        "ReportData.data": {"fields": {"locationValue", "location_value", "timeValue", "time_value"}, "required": True}
    }
    one_of_validator = model_validator(mode="before")(check_one_of)
    location_value: typing.Optional[GeoLocation] = Field(default=None)
    time_value: datetime = Field(default_factory=datetime.now)


class Report(MyBaseSchema):
    source_id: typing.Optional[str] = Field(default="")
    data: ReportData = Field()
