from html.parser import HTMLParser
from pyquery import PyQuery as pq
from re import sub

__all__ = ['convert']

# HTML tag for convert to SlackMD
MRKDWN = {'b': ('*', '*'),
          'i': ('_', '_'),
          'strike': ('~', '~'),
          'a': ('<', '>'),
          'li': ('• ', '\\n')}


class HTMLToSlackMD(HTMLParser):
    def __init__(self):
        super().__init__()
        self._tag_stack = []
        self._slack_md = ''

    def handle_starttag(self, tag, attrs):
        if tag in MRKDWN:
            self._slack_md = self._slack_md + MRKDWN[tag][0]
        for attr in attrs:
            if attr[0] == 'href':
                self._slack_md = self._slack_md + attr[1] + '|'
        self._tag_stack.append(tag)

    def handle_data(self, tag):
        self._slack_md = self._slack_md + tag

    def handle_endtag(self, tag):
        if tag in MRKDWN:
            self._slack_md = self._slack_md + MRKDWN[tag][1]
        if self._tag_stack[0] == tag:
            self._tag_stack.pop()
            self._slack_md = self._slack_md + '\\n'
        else:
            self._tag_stack.pop()

    def _clear_mrk(self, html):
        doc = pq(html)
        for tag_el in MRKDWN.keys():
            for el in doc.items(tag_el):
                if not pq(el).text():
                    el.remove()
                    html = doc.html()

        return sub(' +', ' ', html)

    def convert(self, html=''):
        self.html = self._clear_mrk(html)
        self.feed(self.html)
        print(self._slack_md)
        return self._slack_md


_inst = HTMLToSlackMD()
convert = _inst.convert
