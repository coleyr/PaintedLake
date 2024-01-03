from bs4 import BeautifulSoup
import feedparser
import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def remove_html_tags(html_text:str):
    if not html_text:
        return ""
    # Parse the HTML text using BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')
    # Extract text without HTML tags
    return soup.get_text(separator=' ', strip=True)

def create_gatsby_md(title, tags, created, content, outpath:str = "./content/posts/"):
    print(f"Creating title: {title}")
    with open(f"{outpath}{slugify(title)}.md", "w", encoding="utf-8") as f:
        f.write(
f"""\
---
title: {title}
date: {created}
tags: {tags}
---

{content}
""")

        
def create_gatsby_files(xml_file_path):

    data = feedparser.parse(xml_file_path)
    for entry in data['entries']:
        title = entry['title']
        tags = [t['term'] for t in entry['tags']]
        print(tags)
        tags.append(entry['author'].replace('Schreiber', ' Schreiber').replace('Cole', 'Coley Angel'))
        created = entry['wp_post_date'].split(" ")[0]
        content = remove_html_tags(entry['content'][0]['value'])
        if not title:
            continue
        create_gatsby_md(title, tags, created=created, content=content)

# Replace 'your_wordpress_export.xml' with the path to your WordPress XML export file
xml_file_path = 'thepaintedlake.WordPress.2021-12-28.xml'

create_gatsby_files(xml_file_path)