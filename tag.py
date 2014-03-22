#coding=utf-8
# 半标记
HALF_TAG = ('br', 'hr', 'input', 'img', 'meta', 'spacer', 'link', 'frame', 'base')
NOTE_TAG = ('!DOCTYPE', '!--')  # 注释标记


class BaseTag(object):
    def __init__(self, name, attrs=[], parent=None, next=None, previous=None, content=None):
        self.name = name
        self.childs = []  # 子标签,
        self.parent = parent  # 父标签
        self.previous = previous  # 前一标签
        self.next = next  # 后一标签
        self.attrs = attrs  # 属性
        self.is_half_tag = self.name in (HALF_TAG)

    def set_parent(self, parent):
        self.parent = parent

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

    def prin(self):
        print '<%s' % self.name
        for i in self.attrs:
            print ' %s=%s' % (i.name, i.value)
        if self.is_half_tag:
            print ' />'
        else:
            print '>'
            for i in self.childs:
                i.prin()  # 递归子tag
            print '</ %s>' % self.name

    def render(self):
        ret = []
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
    def render(self):
        return [self.name]


