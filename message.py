from django.contrib import messages
from django.shortcuts import render, redirect

def my_view(request):
    # Perform some action
    # ...
    
    # Display an informational message
    messages.info(request, 'This is an informational message.')
    
    # Clear any existing messages from the session
    storage = messages.get_messages(request)
    storage.used = True
    
    # Redirect to a different URL
    return redirect('my_other_view')


# showing Messages in HTML
# {% if messages %}
#     <ul class="messages">
#         {% for message in messages %}
#             <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
#         {% endfor %}
#     </ul>
# {% endif %}