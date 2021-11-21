SELECT 
  dataset_id,
  count(*) AS tables,
  SUM(row_count) AS total_rows,
  SUM(size_bytes) AS size_bytes 
FROM data_set_name.__TABLES__
GROUP BY 1
ORDER BY size_bytes DESC