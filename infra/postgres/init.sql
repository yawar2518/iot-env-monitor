-- =============================================================
-- TimescaleDB Initialisation
-- Runs automatically on first PostgreSQL container boot.
-- Enables the TimescaleDB extension on the iot_monitor database.
-- =============================================================

-- Enable TimescaleDB extension.
-- Must run before any Django migrations that create hypertables.
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;