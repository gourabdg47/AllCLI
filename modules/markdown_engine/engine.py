import markdown
from jinja2 import Environment, FileSystemLoader
import os
import datetime

class MarkdownEngine:
    def __init__(self, template_dir='templates', css_file='static/style.css'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.css_file = css_file

    def render_blog_post(self, title, content, date, filename):
        template = self.env.get_template('blog_post.html')

        # Convert Markdown to HTML
        html_content = markdown.markdown(content)

        # Render HTML with Jinja2 template
        html_output = template.render(
            title=title,
            content=html_content,
            date=date,
            css_file=self.css_file,
            current_year=datetime.datetime.now().year
        )

        # Save HTML to file
        with open(filename, 'w') as file:
            file.write(html_output)
