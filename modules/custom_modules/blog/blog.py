import markdown
from jinja2 import Environment, FileSystemLoader
import os
import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

CSS_FILE = 'static/style.css'
TEMPLATE_DIR = 'templates'
BLOG_SAVE_DIR = 'blog'

class MarkdownEngine:
    def __init__(self, template_dir=TEMPLATE_DIR, css_file=CSS_FILE):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.css_file = css_file

    def render_blog_post(self, title, content, date, filename):
        try:
            # Load Jinja2 template
            template = self.env.get_template('blog_post.html')
            
            # Convert Markdown to HTML with extensions for advanced features
            md_extensions = [
                'markdown.extensions.fenced_code',   # Support for fenced code blocks
                'markdown.extensions.codehilite',    # Syntax highlighting
                'markdown.extensions.tables',        # Tables
                'markdown.extensions.footnotes',     # Footnotes
                'markdown.extensions.admonition'     # Admonitions (e.g., notes, warnings)
            ]
            html_content = markdown.markdown(content, extensions=md_extensions)

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
            logging.info(f'Blog post successfully generated: {filename}')
        
        except Exception as e:
            logging.error(f'Error generating blog post: {e}')

# Example usage
if __name__ == "__main__":
    engine = MarkdownEngine()
    markdown_content = """
    # My Blog Post

    This is a sample blog post.

    ## Code Example

    ```python
    def hello_world():
        print("Hello, World!")
    ```

    ## Table Example

    | Header 1 | Header 2 |
    |----------|----------|
    | Row 1    | Data 1   |
    | Row 2    | Data 2   |

    ## Footnotes

    Here is a footnote reference[^1].

    [^1]: This is the footnote text.

    ## Admonitions

    !!! note
        This is a note admonition.
    """
    engine.render_blog_post(
        title="Sample Blog Post",
        content=markdown_content,
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
        filename='output_blog_post.html'
    )
