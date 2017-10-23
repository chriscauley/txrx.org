{% if error %}IMPORTANT: A ticket was not made. Here is the error!
Error: {{ error|safe }}{% endif %}

A new work request has been submitted:
{{ signature }}

{% for field in signature.get_fields %}{% if field.get_name != "files" %}{{ field.label }}: {{ field.value }}{% endif %}
{% endfor %}

{% if signature.get_files %}{% for file in signature.get_files %}
{{ settings.SITE_URL }}{{ file.src.url }}
{% endfor %}{% endif %}
