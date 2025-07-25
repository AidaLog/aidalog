from django_hosts import patterns, host

host_patterns = patterns(
  '',
  host(r'', 'main.urls', name=' '),  # no subdomain
)