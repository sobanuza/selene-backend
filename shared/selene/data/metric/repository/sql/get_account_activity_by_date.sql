SELECT
    added,
    deleted,
    active,
    active_open_dataset,
    active_member
FROM
    metric.account_activity
WHERE
    activity_dt = %(activity_date)s
