"""
LeafNode Module
"""

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    LeafNode Class
    """

    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"
