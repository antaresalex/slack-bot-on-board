from html.parser import HTMLParser


class HTMLToSlack(HTMLParser):
    tag_stack = []
    slack_md = ''
    mrdwn = {'b': ['*', '*'],
             'i': ['_', '_'],
             'strike': ['~', '~'],
             'a': ['<', '>'],
             'li': ['• ', '\n']}

    def handle_starttag(self, tag, attrs):
        if tag in self.mrdwn:
            self.slack_md = self.slack_md + self.mrdwn[tag][0]
        for attr in attrs:
            if attr[0] == 'href':
                self.slack_md = self.slack_md + attr[1] + '|'
        self.tag_stack.append(tag)

    def handle_data(self, tag):
        self.slack_md = self.slack_md + tag

    def handle_endtag(self, tag):
        if tag in self.mrdwn:
            self.slack_md = self.slack_md + self.mrdwn[tag][1]
        if self.tag_stack[0] == tag:
            self.tag_stack.pop()
            self.slack_md = self.slack_md + '\n'
        else:
            self.tag_stack.pop()


def convert_to_slack_md(html):
    html_to_slack = HTMLToSlack()
    html_to_slack.feed(html)
    slack_to_md = html_to_slack.slack_md
    return slack_to_md
