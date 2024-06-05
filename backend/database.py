from supabase import Client, create_client
from os import environ

_url = environ.get("SUPABASE_URL")
_key = environ.get("SUPABASE_KEY")
_url = "https://yugnoihrepzezgfyhqhl.supabase.co"
_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1Z25vaWhyZXB6ZXpnZnlocWhsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNjY0NDMzMiwiZXhwIjoyMDMyMjIwMzMyfQ.I2f-3Hg0lNcafX-EZpKTyjewNtf-tvKqRbtQV0q5EO8"

supabase: Client = create_client(_url, _key)