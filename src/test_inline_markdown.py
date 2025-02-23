import unittest

from textnode import *
from inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splitnodes(self):
        node1 = TextNode("`Halo` ini adalah `contoh` code", TextType.TEXT)
        node2 = TextNode("Halo ini adalah contoh code", TextType.TEXT)
        node3 = TextNode("Halo ini adalah contoh code", TextType.BOLD)

        self.assertEqual(
            split_nodes_delimiter([node1], "`", TextType.CODE),
            [
                TextNode("Halo", TextType.CODE),
                TextNode(" ini adalah ", TextType.TEXT),
                TextNode("contoh", TextType.CODE),
                TextNode(" code", TextType.TEXT)
            ]
        )
        self.assertEqual(
            split_nodes_delimiter([node2], "`", TextType.CODE),
            [
                TextNode("Halo ini adalah contoh code", TextType.TEXT)
            ]
        )

        self.assertEqual(
            split_nodes_delimiter([node3], "`", TextType.CODE),
            [
                TextNode("Halo ini adalah contoh code", TextType.BOLD)
            ]
        )

        self.assertEqual(
            split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE),
            [
                TextNode("Halo", TextType.CODE),
                TextNode(" ini adalah ", TextType.TEXT),
                TextNode("contoh", TextType.CODE),
                TextNode(" code", TextType.TEXT),
                TextNode("Halo ini adalah contoh code", TextType.TEXT),
                TextNode("Halo ini adalah contoh code", TextType.BOLD)
            ]
        )


class TestExtractImagesLinks(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_images(text),
            []
        )

    def test_extract_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(text),
            []
        )
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodeslink(self):
        node1 = TextNode("This is text without a link", TextType.TEXT)
        node2 = TextNode("[to boot dev](https://www.boot.dev) is the link", TextType.TEXT)
        node3 = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node4 = TextNode("It is bold text", TextType.BOLD)

        self.assertEqual(
            split_nodes_link([node1]),
            [TextNode("This is text without a link", TextType.TEXT)]
        )

        self.assertEqual(
            split_nodes_link([node2]),
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is the link", TextType.TEXT)
            ]
        )

        self.assertEqual(
            split_nodes_link([node3]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ]
        )

        self.assertEqual(
            split_nodes_link([node4]),
            [node4]
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodesimage(self):
        node1 = TextNode("This is text without a image", TextType.TEXT)
        node2 = TextNode("![to boot dev](https://www.boot.dev/image.jpg) is the image", TextType.TEXT)
        node3 = TextNode("This is image ![to boot dev](https://www.boot.dev/image.jpg) and ![to youtube](https://www.youtube.com/image.jpg)", TextType.TEXT)
        node4 = TextNode("It is bold text", TextType.BOLD)

        self.assertEqual(
            split_nodes_image([node1]),
            [TextNode("This is text without a image", TextType.TEXT)]
        )

        self.assertEqual(
            split_nodes_image([node2]),
            [
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/image.jpg"),
                TextNode(" is the image", TextType.TEXT)
            ]
        )

        self.assertEqual(
            split_nodes_image([node3]),
            [
                TextNode("This is image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/image.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/image.jpg")
            ]
        )

        self.assertEqual(
            split_nodes_image([node4]),
            [node4]
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )



if __name__ == "__main__":
    unittest.main()