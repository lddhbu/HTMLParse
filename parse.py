#coding=utf-8
from tag import Tag, Attribute, Content
from tag import HALF_TAG, NOTE_TAG
from util import my_split


class ParseHTML(object):
    PUSH_SYMBOl = ('"', "'", '<', '>')

    def __init__(self, path):
        self.path = path
        self.root = Tag('root')
        self.html = ''
        self.tag_stack = [self.root]  # 标签栈, 保存的是未完成解析的tag
        self.symbol_stack = [[-1, '>']]  # 符号栈
        self.last_tag = self.root
        self._get_html()
        self.extract()

    def	_get_html(self):
        with open(self.path) as f:
            self.html = f.read()

    def _is_half_tag(self, start, end):
        while self.html[start] in '</> \n' and start < end:
            start += 1
        index = start
        while self.html[index] not in '</> \n' and index < end:
            index += 1
        return self.html[start: index] in HALF_TAG

    def _is_note_tag(self, start, end):
        while self.html[start] in '</> \n' and start < end:
            start += 1
        index = start
        while self.html[index] not in '</> \n' and index < end:
            index += 1
        return self.html[start: index] in NOTE_TAG

    def _on_create_tag(self, start, end):
        """生成一个tag时, 即遇到<>时"""
        this_tag = self.html[start: end].strip('</> \n')
        index = this_tag.find(' ')
        if index == -1:  # 没有属性
            tag_name = this_tag
            tag_attrs = []
        else:
            tag_name = this_tag[:index]
            tag_attrs = []
            indexs = my_split(this_tag[index + 1:], ' ', '"')
            for i in indexs:
                name, sep, value = this_tag[i[0]: i[1] + 1].partition('=')
                tag_attrs.append(Attribute(name, value))
        new_tag = Tag(tag_name, tag_attrs)
        return new_tag

    def _on_end_tag(self):
        """tag结束时，即遇到</>时"""
        pass

    def _on_content(self, start, end):
        """遇到content时"""
        this_content = self.html[start: end].strip('</>\n')
        new_content = Content(this_content)
        return  new_content

    def extract(self):
        """取标签，
        """
        quotation_flag = False
        for index, i in enumerate(self.html):
            if i != '"' and quotation_flag:
                continue
            elif i == '"':
                quotation_flag = not quotation_flag
            if i == '<' and self.symbol_stack[-1][1] != '<':
                if self.symbol_stack[-1][1] == '$':  # 内容的结束
                    new_content = self._on_content(self.symbol_stack[-1][0], index)
                    self.tag_stack[-1].append(new_content)
                    self.symbol_stack.pop()
                self.symbol_stack.append([index, i])
            elif i == '/' and self.symbol_stack[-1][1] == '<':
                self.symbol_stack.append([index, i])
            elif i == '>':
                if self._is_half_tag(self.symbol_stack[-1][0], index):  # 半标记
                    new_tag = self._on_create_tag(self.symbol_stack[-1][0], index)
                    if self.symbol_stack[-1][1] == '/':
                        self.symbol_stack.pop()
                    self.symbol_stack.pop()
                    new_tag.set_parent(self.tag_stack[-1])
                    self.tag_stack[-1].append(new_tag)
                    continue
                if self._is_note_tag(self.symbol_stack[-1][0], index):  # 注释标记
                    while self.symbol_stack.pop()[1] != '<':
                        pass
                if self.symbol_stack[-1][1] == '<':
                    new_tag = self._on_create_tag(self.symbol_stack[-1][0], index)
                    self.symbol_stack.pop()
                    new_tag.set_parent(self.tag_stack[-1])
                    self.tag_stack[-1].append(new_tag)
                    self.tag_stack.append(new_tag)
                elif self.symbol_stack[-1][1] == '/':
                    self._on_end_tag()
                    if self.tag_stack[-1].name != 'root':
                        self.tag_stack.pop()
                    self.symbol_stack.pop()
                    self.symbol_stack.pop()
                else:
                    continue
            else:  # 内容
                if self.symbol_stack[-1][1] == '>':  # $符号代表内容content
                    self.symbol_stack.append([index, '$'])

    def render(self):
        ret = ''.join(self.root.render())
        print ret


def main():
    parse = ParseHTML('asd.html')
    parse.render()


if __name__ == "__main__":
    main()
