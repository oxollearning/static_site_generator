import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

class TestNodeToHTML(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("Text Type", TextType.TEXT, None)
        html_result = 'Text Type'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)
    def test_bold(self):
        text_node = TextNode("Bold Type", TextType.BOLD, None)
        html_result = '<b>Bold Type</b>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)
    def test_italic(self):
        text_node = TextNode("Italic Type", TextType.ITALIC, None)
        html_result = '<i>Italic Type</i>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)
    def test_code(self):
        text_node = TextNode("Code Type", TextType.CODE, None)
        html_result = '<code>Code Type</code>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)
    def test_link(self):
        text_node = TextNode("Link Type", TextType.LINK, "https://www.google.com")
        html_result = '<a href="https://www.google.com">Link Type</a>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)
    def test_img(self):
        text_node = TextNode("Image Type", TextType.IMAGE, "https://www.google.com/logo.png")
        html_result = '<img src="https://www.google.com/logo.png" alt="Image Type"></img>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html_result)

if __name__ == "__main__":
    unittest.main()