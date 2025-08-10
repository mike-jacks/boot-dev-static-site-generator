"""
parentnode module
"""

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    ParendNode Class
    """

    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        output = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
