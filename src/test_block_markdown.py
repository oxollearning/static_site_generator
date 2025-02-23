import unittest

from block_markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text="""  \t  \t
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


\t \t\t\t\t

   * This is the first list item in a list block\t \t
* This is a list item
\t    \t* This is another list item"""

        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_heading(self):
        text1 = "# heading 1"
        text2 = "## heading 2"
        text3 = "### heading 3"
        text4 = "#### heading 4"
        text5 = "##### heading 5"
        text6 = "###### heading 6"
        text7 = "####### heading 7"
        self.assertEqual(block_to_block_type(text1), "heading")
        self.assertEqual(block_to_block_type(text2), "heading")
        self.assertEqual(block_to_block_type(text3), "heading")
        self.assertEqual(block_to_block_type(text4), "heading")
        self.assertEqual(block_to_block_type(text5), "heading")
        self.assertEqual(block_to_block_type(text6), "heading")
        self.assertEqual(block_to_block_type(text7), "paragraph")
    
    def test_block_code(self):
        text1 = """```code line 1
code line 2```"""
        text2 = """```code line 1
code line 2"""
        text3 = """code line 1
code line 2```"""
        self.assertEqual(block_to_block_type(text1), "code")
        self.assertEqual(block_to_block_type(text2), "paragraph")
        self.assertEqual(block_to_block_type(text3), "paragraph")
    
    def test_block_quote(self):
        text1 = """>quote line 1
>quote line 2"""
        text2 = """>quote line 1
quote line 2"""
        self.assertEqual(block_to_block_type(text1), "quote")
        self.assertEqual(block_to_block_type(text2), "paragraph")
    
    def test_block_unordered_list(self):
        text1 = """* This is the first list item in a list block
* This is a list item  	
- This is another list item"""
        text2 = """* This is the first list item in a list block
* This is a list item  	
 This is another list item"""
        self.assertEqual(block_to_block_type(text1), "unordered_list")
        self.assertEqual(block_to_block_type(text2), "paragraph")

    def test_block_ordered_list(self):
        text1 = """1. This is the first list item in a list block
2. This is a list item  	
3. This is another list item"""
        text2 = """1. This is the first list item in a list block
2. This is a list item  	
This is another list item"""
        text3 = """1. This is the first list item in a list block
2. This is a list item  	
4. This is another list item"""
        self.assertEqual(block_to_block_type(text1), "ordered_list")
        self.assertEqual(block_to_block_type(text2), "paragraph")
        self.assertEqual(block_to_block_type(text3), "paragraph")

class TestExtractTitle(unittest.TestCase):
        def test_extract_title(self):
                markdown = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy"""
                self.assertEqual(extract_title(markdown), "Tolkien Fan Club")

                markdown = """## Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy"""
                with self.assertRaises(Exception):
                        extract_title(markdown)

        