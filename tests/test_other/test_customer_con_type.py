from datetime import datetime, timedelta, timezone

import pytest
from pydantic import BaseModel, ValidationError

from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.customer_validator import _now_default_factory, set_now_default_factory


class TestCustomerConTimedelta:
    def test_contimedelta_const(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_const=timedelta(days=1))  # type: ignore

        Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(minutes=1))

    def test_contimedelta_ge(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_ge=timedelta(days=1))  # type: ignore

        Demo(demo=timedelta(days=2))
        Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(minutes=0))

    def test_contimedelta_gt(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_gt=timedelta(days=1))  # type: ignore

        Demo(demo=timedelta(days=2))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(minutes=0))

    def test_contimedelta_le(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_le=timedelta(days=2))  # type: ignore

        Demo(demo=timedelta(days=2))
        Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=3))

    def test_contimedelta_lt(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_lt=timedelta(days=2))  # type: ignore

        Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=2))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=3))

    def test_contimedelta_in(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_in=[timedelta(days=2), timedelta(minutes=1)])  # type: ignore

        Demo(demo=timedelta(days=2))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=1))
        Demo(demo=timedelta(minutes=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(minutes=2))

    def test_contimedelta_not_in(self) -> None:
        class Demo(BaseModel):
            demo: contimedelta(duration_not_in=[timedelta(days=2), timedelta(minutes=1)])  # type: ignore

        Demo(demo=timedelta(days=1))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(days=2))
        Demo(demo=timedelta(minutes=2))
        with pytest.raises(ValidationError):
            Demo(demo=timedelta(minutes=1))


class TestCustomerConTimestamp:
    def test_contimestamp_const(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_const=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))
        Demo(demo=1600000000)
        Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=1600000001)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_ge(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_ge=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))  # type: ignore

        for timestamp in [1600000000, 1600000001]:
            Demo(demo=datetime.fromtimestamp(timestamp).astimezone(tz=timezone.utc))
            Demo(demo=timestamp)
            Demo(demo=datetime.fromtimestamp(timestamp).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1500000000).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=1500000000)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1500000000).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_gt(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc))
        Demo(demo=1600000001)
        Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=1600000000)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_le(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_le=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))  # type: ignore

        for timestamp in [1600000000, 1500000001]:
            Demo(demo=datetime.fromtimestamp(timestamp).astimezone(tz=timezone.utc))
            Demo(demo=timestamp)
            Demo(demo=datetime.fromtimestamp(timestamp).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=1600000001)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_lt(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))  # type: ignore

        Demo(demo=datetime.fromtimestamp(1500000001).astimezone(tz=timezone.utc))
        Demo(demo=1500000001)
        Demo(demo=datetime.fromtimestamp(1500000001).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=1600000000)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_gt_now_by_default(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt_now=True)  # type: ignore

        Demo(demo=datetime.now() + timedelta(days=1))

        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() - timedelta(days=1))

    def test_contimestamp_gt_now_by_default_factory(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt_now=lambda: datetime.now().astimezone(tz=timezone.utc))  # type: ignore

        now_timestamp: int = int(datetime.now().astimezone(tz=timezone.utc).timestamp() + 1)
        Demo(demo=datetime.fromtimestamp(now_timestamp).astimezone(tz=timezone.utc))
        Demo(demo=now_timestamp)
        Demo(demo=datetime.fromtimestamp(now_timestamp).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp - 10).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=now_timestamp - 10)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp - 10).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_lt_now_by_default(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt_now=True)  # type: ignore

        Demo(demo=datetime.now() - timedelta(days=1))

        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() + timedelta(days=1))

    def test_contimestamp_lt_now_by_default_factory(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt_now=lambda: datetime.now().astimezone(tz=timezone.utc))  # type: ignore

        now_timestamp: int = int(datetime.now().astimezone(tz=timezone.utc).timestamp() - 10)
        Demo(demo=datetime.fromtimestamp(now_timestamp).astimezone(tz=timezone.utc))
        Demo(demo=now_timestamp)
        Demo(demo=datetime.fromtimestamp(now_timestamp).astimezone(tz=timezone.utc).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp + 20).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=now_timestamp + 20)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp + 20).astimezone(tz=timezone.utc).isoformat())

    def test_contimestamp_in(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_in=[datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc)])  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc))

    def test_contimestamp_not_in(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_not_in=[datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc)])  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000001).astimezone(tz=timezone.utc))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).astimezone(tz=timezone.utc))

    def test_contimestamp_within(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_within=timedelta(seconds=1))  # type: ignore

        Demo(demo=datetime.now())
        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() + timedelta(minutes=1))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() - timedelta(minutes=1))

    def test_set_now_default_factory(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_within=timedelta(seconds=1))  # type: ignore

        default_now_default_factory = _now_default_factory
        try:
            set_now_default_factory(lambda: datetime.now().astimezone(tz=timezone.utc))
            Demo(demo=datetime.now().astimezone(tz=timezone.utc))
            with pytest.raises(ValidationError):
                Demo(demo=datetime.now().astimezone(tz=timezone.utc) + timedelta(minutes=1))
            with pytest.raises(ValidationError):
                Demo(demo=datetime.now().astimezone(tz=timezone.utc) - timedelta(minutes=1))
        finally:
            set_now_default_factory(default_now_default_factory)

    def test_contimestamp_ignore_tz(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_not_in=[datetime.fromtimestamp(1600000000)])  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000001))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000))
