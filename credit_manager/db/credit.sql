{% sql 'create', note='Create new credit record' %}
INSERT INTO admin.credit (client_name, description, start) VALUES
({{ client_name|guards.string }}, $${{ description }}$$, {{ start|guards.string }})
RETURNING *;
{% endsql %}


{% sql 'retrieve', note='Retrieve a credit record based on UID' %}
SELECT
  uid,
  client_name,
  description,
  start::date
FROM admin.credit
  WHERE uid = {{ uid|guards.string }};
{% endsql %}


{% sql 'update', note='Update a credit record based on UID' %}
UPDATE admin.credit SET
  client_name = {{ client_name|guards.string }},
  description = $${{ description }}$$,
  start = {{ start|guards.string }}
WHERE uid = {{ uid|guards.string }}
  RETURNING *;
{% endsql %}


{% sql 'delete', note='Delete a credit record' %}
DELETE FROM admin.credit WHERE  uid = {{ uid|guards.string }}
RETURNING *;
{% endsql %}


{% sql 'list', note='Filter credit collection' %}
SELECT
  uid,
  client_name,
  description,
  start::date
FROM admin.credit

  {% if start and stop %}
    WHERE start BETWEEN {{ start|guards.string }} AND {{ stop|guards.string }}
  {% endif %}
ORDER BY start;
{% endsql %}


{% sql 'exists', note='Check if credit record exists.' %}
SELECT EXISTS(
  SELECT 1 FROM admin.credit WHERE uid = {{ uid|guards.string }}
);
{% endsql %}