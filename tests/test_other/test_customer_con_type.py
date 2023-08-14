from datetime import datetime, timedelta

import pytest
from pydantic import BaseModel, ValidationError

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.customer_con_type import contimedelta, contimestamp
from protobuf_to_pydantic.customer_validator.rule import _now_default_factory, set_now_default_factory

_diff_utc_second: float = datetime.now().astimezone().utcoffset().total_seconds()  # type: ignore


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
            demo: contimestamp(timestamp_const=1600000000, ignore_tz=True)  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000000))
        Demo(demo=1600000000 + _diff_utc_second)

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001))
        with pytest.raises(ValidationError):
            Demo(demo=1600000001 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).isoformat())

    def test_contimestamp_ge(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_ge=1600000000, ignore_tz=True)  # type: ignore

        for timestamp in [1600000000, 1600000001]:
            Demo(demo=datetime.fromtimestamp(timestamp))
            Demo(demo=timestamp + _diff_utc_second)
            Demo(demo=datetime.fromtimestamp(timestamp).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1500000000))
        with pytest.raises(ValidationError):
            Demo(demo=1500000000 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1500000000).isoformat())

    def test_contimestamp_gt(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt=1600000000, ignore_tz=True)  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000001))
        Demo(demo=1600000001 + _diff_utc_second)
        Demo(demo=datetime.fromtimestamp(1600000001).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000))
        with pytest.raises(ValidationError):
            Demo(demo=1600000000 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).isoformat())

    def test_contimestamp_le(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_le=1600000000, ignore_tz=True)  # type: ignore

        for timestamp in [1600000000, 1500000001]:
            Demo(demo=datetime.fromtimestamp(timestamp))
            Demo(demo=timestamp + _diff_utc_second)
            Demo(demo=datetime.fromtimestamp(timestamp).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001))
        with pytest.raises(ValidationError):
            Demo(demo=1600000001 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001).isoformat())

    def test_contimestamp_lt(self) -> None:

        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt=1600000000, ignore_tz=True)  # type: ignore

        Demo(demo=datetime.fromtimestamp(1500000001))
        Demo(demo=1500000001 + _diff_utc_second)
        Demo(demo=datetime.fromtimestamp(1500000001).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000))
        with pytest.raises(ValidationError):
            Demo(demo=1600000000 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000).isoformat())

    def test_contimestamp_gt_now_by_default(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt_now=True)  # type: ignore

        Demo(demo=datetime.now() + timedelta(days=1))

        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() - timedelta(days=1))

    def test_contimestamp_gt_now_by_default_factory(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_gt_now=lambda: datetime.now(), ignore_tz=True)  # type: ignore

        now_timestamp: int = int(datetime.now().timestamp() + 1)
        Demo(demo=datetime.fromtimestamp(now_timestamp))
        Demo(demo=now_timestamp + _diff_utc_second)
        Demo(demo=datetime.fromtimestamp(now_timestamp).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp - 10))
        with pytest.raises(ValidationError):
            Demo(demo=now_timestamp - 10 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp - 10).isoformat())

    def test_contimestamp_lt_now_by_default(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt_now=True)  # type: ignore

        Demo(demo=datetime.now() - timedelta(days=1))

        with pytest.raises(ValidationError):
            Demo(demo=datetime.now() + timedelta(days=1))

    def test_contimestamp_lt_now_by_default_factory(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_lt_now=lambda: datetime.now(), ignore_tz=True)  # type: ignore

        now_timestamp: int = int(datetime.now().timestamp() - 10)
        Demo(demo=datetime.fromtimestamp(now_timestamp))
        Demo(demo=now_timestamp + _diff_utc_second)
        Demo(demo=datetime.fromtimestamp(now_timestamp).isoformat())

        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp + 20))
        with pytest.raises(ValidationError):
            Demo(demo=now_timestamp + 20 + _diff_utc_second)
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(now_timestamp + 20).isoformat())

    def test_contimestamp_in(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_in=[1600000000], ignore_tz=True)  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000000))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000001))

    def test_contimestamp_not_in(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_not_in=[1600000000], ignore_tz=True)  # type: ignore

        Demo(demo=datetime.fromtimestamp(1600000001))
        with pytest.raises(ValidationError):
            Demo(demo=datetime.fromtimestamp(1600000000))

    def test_contimestamp_within(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(timestamp_within=timedelta(seconds=1), ignore_tz=True)  # type: ignore

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
            set_now_default_factory(lambda: datetime.now())
            Demo(demo=datetime.now())
            with pytest.raises(ValidationError):
                Demo(demo=datetime.now() + timedelta(minutes=1))
            with pytest.raises(ValidationError):
                Demo(demo=datetime.now() - timedelta(minutes=1))
        finally:
            set_now_default_factory(default_now_default_factory)

    def test_contimestamp_ignore_tz(self) -> None:
        class Demo(BaseModel):
            demo: contimestamp(ignore_tz=True)  # type: ignore

        assert Demo(demo=datetime.fromtimestamp(1600000000)) == Demo(demo=1600000000 + _diff_utc_second)
