from infi.clickhouse_orm import (
    Database,
    Model,
    DateTimeField,
    DateField,
    Int8Field,
    UInt8Field,
    UInt16Field,
    UInt64Field,
    UUIDField,
    StringField,
    FixedStringField,
    MergeTree,
    SummingMergeTree,
    CollapsingMergeTree,
)


class Views(Model):
    counter_id = UInt16Field()
    view_id = UUIDField()
    visit_id = UUIDField()
    visitor_unique_key = UUIDField()
    referer = StringField()
    device_type = StringField()
    browser_type = StringField()
    user_agent = StringField()
    os_type = StringField()
    ip = FixedStringField(16)
    language = FixedStringField(2)
    created_at = DateTimeField()

    engine = MergeTree("created_at", ("created_at",))


class VisitorInDay(Model):
    counter_id = UInt16Field()
    count_visitors = UInt64Field()
    date = DateField()
    created_time = DateTimeField()
    sign = Int8Field()

    engine = CollapsingMergeTree(
        "date",
        (
            "counter_id",
            "date",
        ),
        "sign",
    )


class UniqueVisitors(Model):
    counter_id = UInt16Field()
    visitor_unique_key = UUIDField()
    date = DateField()

    engine = MergeTree(
        "date",
        (
            "counter_id",
            "date",
        ),
    )


class VisitInDay(Model):
    counter_id = UInt16Field()
    count_visits = UInt64Field()
    date = DateField()
    created_time = DateTimeField()
    sign = Int8Field()

    engine = CollapsingMergeTree(
        "date",
        (
            "counter_id",
            "date",
        ),
        "sign",
    )


class UniqueVisits(Model):
    counter_id = UInt16Field()
    visit_id = UUIDField()
    date = DateField()

    engine = MergeTree(
        "date",
        (
            "counter_id",
            "date",
        ),
    )


class ViewInDay(Model):
    counter_id = UInt16Field()
    count_views = UInt64Field()
    date = DateField()
    created_time = DateTimeField()
    sign = Int8Field()

    engine = CollapsingMergeTree(
        "date",
        (
            "counter_id",
            "date",
        ),
        "sign",
    )
