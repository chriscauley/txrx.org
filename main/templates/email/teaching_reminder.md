{% load i18n %}{% autoescape off %}

This is a reminder that you are teaching tomorrow at {{ settings.SITE_NAME }}.

{% for classtime in classtimes %}
* **{{ classtime.session.course }}**: {{ classtime.start|date:"F d @ P" }}
{% endfor %}

If you would like to not receive these notifications, please use one of the links below.

Unsubscribe from class reminders: {{ SITE_URL }}{% url "unsubscribe" "classes" user.id %}?LA_KEY={{ la_key.key }}

Unsubscribe from all notifications: {{ SITE_URL }}{% url "unsubscribe" "global" user.id %}?LA_KEY={{ la_key.key }}

{% endautoescape %}
