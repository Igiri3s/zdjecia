import requests
from jinja2 import Template

def fetch_comic_data(comic_number):
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def load_comic_numbers(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def generate_html(comics_data):
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>XKCD Comics</title>
    </head>
    <body>
        <div class="container">
            <div class="row">
                {% for comic in comics %}
                <div class="col-12 col-md-6 col-lg-4">
                    <div class="card mb-4">
                        <img src="{{ comic.img }}" class="card-img-top" alt="{{ comic.title }}">
                        <div class="card-body">
                            <h5 class="card-title">{{ comic.title }}</h5>
                            <p class="card-text">{{ comic.alt }}</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    template = Template(template_str)
    html_content = template.render(comics=comics_data)
    with open('comics.html', 'w') as file:
        file.write(html_content)

def main():
    comic_numbers = load_comic_numbers('numbers.txt')
    comics_data = []
    for number in comic_numbers:
        data = fetch_comic_data(number)
        if data:
            comics_data.append(data)
    generate_html(comics_data)
    print("HTML file 'comics.html' generated successfully.")

if __name__ == "__main__":
    main()
