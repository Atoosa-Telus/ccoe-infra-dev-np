bq query --nouse_legacy_sql \
'SELECT 
  dataset_id,
  count(*) AS tables,
  SUM(row_count) AS total_rows,
  SUM(size_bytes) AS size_bytes 
FROM belgaroth_sink_data.__TABLES__
GROUP BY 1
ORDER BY size_bytes DESC'

bq query --nouse_legacy_sql \
'SELECT
     start_timestamp,
     error_code,
     SUM(total_requests) AS num_failed_requests
   FROM
     `region-us`.INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_PROJECT
   WHERE
     error_code IS NOT NULL
     AND start_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 30 MINUTE)
   GROUP BY
     start_timestamp,
     error_code
   ORDER BY
     1 DESC'