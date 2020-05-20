UPDATE
    metric.account_activity
SET
    added = added + 1
WHERE
    activity_dt = current_date
