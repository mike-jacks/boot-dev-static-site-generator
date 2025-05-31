"""
test htmlnode
"""

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """
    TestHTMLNode
    """

    def test_props_to_html(self):
        """
        test_propsToHtml
        """
        html_node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        props = html_node.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        """
        test_repr
        """
        html_node = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            repr(html_node),
            """HTMLNode(tag=None,value=None,children=None,props={'href': 'https://www.google.com', 'target': '_blank'})""",
        )
