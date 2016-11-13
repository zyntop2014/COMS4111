{% extends "mainlayout.html" %}
{% block content %}
<form action = "{{ url_for('addrecwaitlist') }}" method = "POST">
  <h3>Waitlist Information</h3>

  restaurant_id<br>
  <select name="restaurant_id">
    {% for r in restaurants %}
      <option value="{{ r[0] }}">{{ r[1] }}</option>
    {% endfor %}
  </select>
  <br>
  customer_id<br>
  <select name="customer_id">
    {% for c in customers %}
      <option value="{{ r[0] }}">{{ r[4] }}</option>
    {% endfor %}
  </select>


  party_datetime<br>
  <input type = "TIMESTAMP" name = "party_datetime" /><br>

  listed_at<br>
  <input type = "TIMESTAMP" name = "listed_at" /><br>

  unlisted_at<br>
  <input type = "TIMESTAMP" name = "unlisted_at" /><br>


  <input type = "submit" value = "submit" /><br>

</form>
{% endblock %}
