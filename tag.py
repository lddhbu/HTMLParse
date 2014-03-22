#coding=utf-8
# 半标记
HALF_TAG = ('br', 'hr', 'input', 'img', 'meta', 'spacer', 'link', 'frame', 'base')
NOTE_TAG = ('!DOCTYPE', '!--')  # 注释标记


class Render(object):
    def br_render(self, tag):
        return '\n%s\n' % ('-' * 80)

    def ul_render(self, tag):
        return '\n'

    def li_render(self, tag):
        num = 0
        p = tag.parent
        while p.name in ('ul', 'li'):
            if p.name == 'ul':
                num += 4
            p = p.parent
        return '\n%s●  ' % (' ' * num)

    def input_render(self, tag):
        return ''

    def nav_render(self, tag):
        return ''

    def h1_render(self, tag):
        return ''

    def h2_render(self, tag):
        return ''

    def h3_render(self, tag):
        return ''

    def h4_render(self, tag):
        return ''

    def h5_render(self, tag):
        return ''

    def h6_render(self, tag):
        return ''

    def h7_render(self, tag):
        return ''

    def img_render(self, tag):
        return '\n\n\nThis is picture!'

    def p_render(self, tag):
        return '\n\n'

    def div_render(self, tag):
        first = tag.first_child()
        if not first or first.name != 'div':
            return '\n'
        return ''

    def other_render(self, tag):
        return ''


_render = Render()


class BaseTag(object):
    def __init__(self, name, attrs=[], parent=None, next=None, previous=None, content=None):
        self.name = name
        self.childs = []  # 子标签,
        self.parent = parent  # 父标签
        self.previous = previous  # 前一标签
        self.next = next  # 后一标签
        self.attrs = attrs  # 属性
        self.is_half_tag = self.name in (HALF_TAG)
        self.is_content = False

    def set_parent(self, parent):
        self.parent = parent

    def first_child(self):
        if len(self.childs) > 0:
            return self.childs[0]
        return None

    def render(self):
        pass


class Tag(BaseTag):
    """标签"""
    def insert(self, position, child):
        position = min(position, len(self.childs))
        child.parent = self
        if len(self.childs) == 0:
            child.previous = None
            child.next = None
        elif position == 0:
            child.previous = None
            next_child = self.childs[0]
            child.next = next_child
            next_child.previous = child
        elif position == len(self.childs):
            child.next = None
            previous_child = self.childs[position - 1]
            child.previous = previous_child
            previous_child.next = child
        else:
            next_child = self.childs[0]
            child.next = next_child
            next_child.previous = child
            previous_child = self.childs[position - 1]
            child.previous = previous_child
            previous_child.next = child
        self.childs.insert(position, child)

    def append(self, child):
        self.insert(len(self.childs), child)

    def render(self):
        if self.name == 'title':
            return ['']
        func = getattr(_render, '%s_render' % self.name, _render.other_render)
        ret = [func(self)]
        for i in self.childs:
            ret.extend(i.render())
        return ret


class Attribute(object):
    """属性"""
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Content(BaseTag):
    """内容"""
    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)
        self.is_content = True

    def render(self):
        return [self.name.replace('&amp;', '&')]
