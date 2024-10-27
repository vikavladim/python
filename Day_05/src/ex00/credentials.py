from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

html = """
<html>
<body>
   <form method="get" action="">  
        <select name="species">
            <option value="Cyberman">Cyberman</option>
            <option value="Dalek">Dalek</option>
            <option value="Judoon">Judoon</option>
            <option value="Human">Human</option>
            <option value="Ood">Ood</option>
            <option value="Silence">Silence</option>
            <option value="Slitheen">Slitheen</option>
            <option value="Sontaran">Sontaran</option>
            <option value="Time Lord">Time Lord</option>
            <option value="Weeping Angel">Weeping Angel</option>
            <option value="Zygon">Zygon</option>
        </select>
        <input type="submit" value="Submit">
    </form>
    <p>
        Species: %(value)s<br>
    </p>
</body>
</html>
"""

characters = {
    'Cyberman': 'John Lumic',
    'Dalek': 'Davros',
    'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
    'Human': 'Leonardo da Vinci',
    'Ood': 'Klineman Halpen',
    'Silence': 'Tasha Lem',
    'Slitheen': 'Coca-Cola salesman',
    'Sontaran': 'General staal',
    'Time Lord': 'Rassilon',
    'Weeping Angel': 'The Division Representative',
    'Zygon': 'Broton'
}


def application(environ, start_response):
    query_string = environ.get('QUERY_STRING')
    d = parse_qs(query_string)
    species = d.get('species', [''])[0]

    if species in characters:
        value = characters[species]
        status = '200 OK'
    else:
        value = 'Unknown'
        status = '404 Not Found'

    credentials = {'credentials': value}

    response_body = html % {
        'value': credentials or 'Empty',
        'species': species or 'Empty'
    }

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode()]


httpd = make_server('localhost', 8888, application)

httpd.serve_forever()
