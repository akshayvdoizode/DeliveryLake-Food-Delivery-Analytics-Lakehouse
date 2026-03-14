-- =====================================================
-- Lakehouse Infrastructure Bootstrap
-- Creates metadata schema and pipeline state table
-- =====================================================

-- Create metadata database
CREATE DATABASE IF NOT EXISTS bronze;
CREATE DATABASE IF NOT EXISTS silver;
CREATE DATABASE IF NOT EXISTS gold;
CREATE DATABASE IF NOT EXISTS metadata;

CREATE TABLE IF NOT EXISTS metadata.pipeline_state (
    table_name STRING,
    watermark_column STRING,
    last_watermark TIMESTAMP,
    last_run_time TIMESTAMP
)
USING DELTA
LOCATION 's3a://deliverylake/metadata/pipeline_state';