-- Create litellm database for LiteLLM proxy
CREATE DATABASE litellm;

-- Create erp_agent database for long-term memory store (if not exists)
-- Note: erp_agent may already be created by POSTGRES_DB env var
SELECT 'CREATE DATABASE erp_agent' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'erp_agent')\gexec
