UPDATE
    metric.account_activity
SET
    deleted = deleted + 1
WHERE
    activity_dt = current_date
