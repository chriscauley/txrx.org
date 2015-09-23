from django.test.runner import DiscoverRunner

class Runner(DiscoverRunner):
  # There is some weird recursive import (or something) that I can't track down.
  # It breaks creating a test database.
  # In the mean time I'm using the dev database (default)
  def setup_databases(self, **kwargs):
    return
  def teardown_databases(self, old_config, **kwargs):
    return
