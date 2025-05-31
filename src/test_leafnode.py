"""
test leafnode
"""

import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    """
    TestLeafNode
    """

    def test_to_html_no_props(self):
        leaf_node = LeafNode(tag="p", value="This is a paragraph of text.")
        want = "<p>This is a paragraph of text.</p>"
        got = leaf_node.to_html()
        self.assertEqual(want, got, "Expected a valid tag")

    def test_to_html_w_props(self):
        leaf_node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        want = '<a href="https://www.google.com">Click me!</a>'
        got = leaf_node.to_html()
        self.assertEqual(want, got, "Expected a valid tag")
