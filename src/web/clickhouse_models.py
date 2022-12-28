from infi.clickhouse_orm import (
    Database,
    Model,
    DateTimeField,
    UInt16Field,
    UUIDField,
    StringField,
    FixedStringField,
    MergeTree,
)


class Views(Model):
    counter_id = UInt16Field()
    view_id = UUIDField()
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
