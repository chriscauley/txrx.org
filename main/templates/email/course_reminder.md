{% load i18n %}{% autoescape off %}

This is a reminder that you have {% if notifications|length == 1%}a class{% else %}{{ notifications|length }} classes{% endif %} tomorrow at {{ settings.SITE_NAME }}.

{% for classtime in classtimes %}
**{{ classtime.session.course }}:** {{ classtime.start|date:"l F j @ P" }}

{{ session.course.get_location_string }}{% if classtime.session.course.requirements %}

**Please remember the following requirements: {{ classtimesession.course.requirements }}**{% endif %}

--------
{% endfor %}

We started sending these notifications because quite a few people forget that they have signed up for a class. If you would like to not receive these notifications, please use one of the links below.

Unsubscribe from class reminders: {{ SITE_URL }}{% url "unsubscribe" "classes" user.id %}?LA_KEY={{ la_key.key }}

Unsubscribe from all notifications: {{ SITE_URL }}{% url "unsubscribe" "global" user.id %}?LA_KEY={{ la_key.key }}

{% endautoescape %}
