import json
import html
import urllib.parse


from multiprocessing import Pool
import mwparserfromhell
import tqdm


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

def get_formatted_doc(doc):
  tree = mwparserfromhell.parse(doc['text'])
  out = []
  for node in tree.nodes:
    if not isinstance(node, mwparserfromhell.nodes.wikilink.Wikilink):
      stripped = strip_code(node)
      if stripped:
        out.append(stripped)
      continue

    title = node.title
    text = node.text if node.text else node.title
    if not title or not text:
      stripped = strip_code(node)
      if stripped:
        out.append(stripped)
      continue
    url_encoded_title = title.strip().replace(' ', '_').lower()
    url_encoded_title = urllib.parse.quote(url_encoded_title)
    html_link = f'<a href="https://en.wikipedia.org/wiki/{url_encoded_title}">{html.escape(str(text))}</a>'
    out.append(html_link)

  title = doc['title']
  if not title:
    return None
  url_encoded_title = title.strip().replace(' ', '_').lower()
  url_encoded_title = urllib.parse.quote(url_encoded_title)
  url = f'https://en.wikipedia.org/wiki/{url_encoded_title}'

  return { 'title': doc['title'], 'text': ''.join(out), 'url': url }

if __name__ == "__main__":
  with open('wikipedia.txt', 'r') as f:
    # docs shape: [{'title': 'title', 'text': 'text'}, ...]
    docs = [json.loads(i) for i in f.readlines()]
    print (f"Loaded {len(docs)} docs")

  seen_urls = set() # to remove duplicates
  with open('wikipedia_formatted.txt', 'w') as f:
    with Pool(processes=16) as pool:
      for doc in tqdm.tqdm(pool.imap_unordered(get_formatted_doc, docs), total=len(docs)):
        if not doc:
          continue
        if doc['url'] in seen_urls:
          continue
        seen_urls.add(doc['url'])
        f.write(json.dumps(doc) + '\n')
