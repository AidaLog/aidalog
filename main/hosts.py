from django_hosts import patterns, host

host_patterns = patterns(
  '',
  host(r'', 'main.urls', name=' '),  # no subdomain
  host(r'ner', 'ner.urls', name='NER'),  # Entity Recognition
)