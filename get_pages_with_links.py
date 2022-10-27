import json
import html
import urllib.parse


import mwparserfromhell


# adapted
# https://sourcegraph.com/python/mwparserfromhell@d5423558aa50167ed25bef7775831d8625aefc17/-/blob/src/mwparserfromhell/wikicode.py?L641
def strip_code(node):
  collapse = True
  kwargs = {
    "normalize": True,
    "collapse": collapse,
    "keep_template_params": False,
  }

  out = []
  stripped = node.__strip__(**kwargs)
  if stripped:
    out.append(str(stripped))

  if collapse:
    stripped = "".join(out).strip("\n")
    while "\n\n\n" in stripped:
      stripped = stripped.replace("\n\n\n", "\n\n")
    return stripped
  return "".join(out)

with open('wikipedia.txt', 'r') as f:
  # docs shape: [{'title': 'title', 'text': 'text'}, ...]
  docs = [json.loads(i) for i in f.readlines()]
with open('wikipedia_formatted.txt', 'w') as f:
  for doc in docs:
    tree = mwparserfromhell.parse(doc['text'])
    out = []
    for node in tree.nodes:
      if not isinstance(node, mwparserfromhell.nodes.wikilink.Wikilink):
        stripped = strip_code(node)
        if stripped:
          out.append(stripped)
        continue

      text = node.text
      title = node.title if node.title else node.text
      url_encoded_title = title.strip().replace(' ', '_').lower()
      url_encoded_title = urllib.parse.quote(url_encoded_title)
      if not title or not text:
        stripped = strip_code(node)
        if stripped:
          out.append(stripped)
        continue
      html_link = f'<a href="https://en.wikipedia.org/wiki/{url_encoded_title}">{html.escape(str(text))}</a>'
      out.append(html_link)

    title = doc['title']
    if not title:
      continue
    url_encoded_title = title.strip().replace(' ', '_').lower()
    url_encoded_title = urllib.parse.quote(url_encoded_title)
    url = f'https://en.wikipedia.org/wiki/{url_encoded_title}'

    json_dump = json.dumps({ 'title': doc['title'], 'text': ''.join(out), 'url': url })
    f.write(json_dump)
    f.write('\n')




