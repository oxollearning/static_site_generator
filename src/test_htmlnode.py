import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "test link", None,
            {"href": "https://www.google.com",
             "target": "_blank",
             "class": "link"})
        props_result = ' href="https://www.google.com" target="_blank" class="link"'
        self.assertEqual(node.props_to_html(), props_result)
    def test_repr(self):
        node = HTMLNode("a", "test link", None,
            {"href": "https://www.google.com",
             "target": "_blank",
             "class": "link"})
        repr_result = "HTMLNode(a, test link, children: None, {'href': 'https://www.google.com', 'target': '_blank', 'class': 'link'})"
        self.assertEqual(str(node), repr_result)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="a", value="test link",
            props = {"href": "https://www.google.com",
             "target": "_blank",
             "class": "link"})
        to_html_result = '<a href="https://www.google.com" target="_blank" class="link">test link</a>'
        self.assertEqual(node.to_html(), to_html_result)
    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="test link",
            props = {"href": "https://www.google.com",
             "target": "_blank",
             "class": "link"})
        to_html_result = 'test link'
        self.assertEqual(node.to_html(), to_html_result)
 
class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "class": "paragraph",
                "id": "main"
            }
        )
        to_html_result = '<p class="paragraph" id="main"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), to_html_result)
    
    def test_to_html_nested(self):
        node = ParentNode(
            "table",
            [
                ParentNode(
                    "tr",
                    [
                        LeafNode(
                            "td",
                            "Table Data 1"
                        ),
                        LeafNode(
                            "td",
                            "Table Data 2"
                        )
                    ]
                )
            ],
            {
                "class": "table"
            }
        )
        to_html_result = '<table class="table"><tr><td>Table Data 1</td><td>Table Data 2</td></tr></table>'
        self.assertEqual(node.to_html(), to_html_result)

if __name__ == "__main__":
    unittest.main()