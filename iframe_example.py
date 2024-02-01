# {% for item in items %}
#   <a href="{{ item.url }}" class="link" data-id="{{ item.id }}">Link {{ item.id }}</a>
# {% endfor %}

# <iframe id="myIframe" src="default_url.html"></iframe>

# <script>
#   const links = document.querySelectorAll('.link');
#   const myIframe = document.getElementById('myIframe');

#   links.forEach(link => {
#     link.addEventListener('click', (event) => {
#       event.preventDefault();
#       const selectedLink = event.target;
#       const selectedValue = selectedLink.dataset.id;
#       myIframe.src = selectedLink.href + '?id=' + selectedValue;
#     });
#   });
# </script>

