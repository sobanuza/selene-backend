INSERT INTO
    metric.account_activity (
        added,
        deleted,
        active,
        active_open_dataset,
        active_member
    )
VALUES
    (
        %(added)s,
        %(deleted)s,
        %(active)s,
        %(active_open_dataset)s,
        %(active_member)s
    )
