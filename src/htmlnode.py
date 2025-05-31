"""
HTMLNode Module
"""


class HTMLNode:
    """
    HTMLNode Class
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        to_html method
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        props_to_html method
        """
        if self.props is not None:
            props_list = []
            for key, value in self.props.items():
                props_list.append(f' {key}="{value}"')
            return "".join(props_list)
        return ""

    def __repr__(self):
        """
        __repr__ method
        """
        return f"HTMLNode(tag={self.tag},value={self.value},children={self.children},props={self.props})"
