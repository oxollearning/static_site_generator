import re
from htmlnode import *
from inline_markdown import *

def markdown_to_blocks(markdown):
    blocks = []
    for text in markdown.split("\n\n"):
        lines = list(map(lambda x: x.strip(), text.strip().split("\n")))
        result = "\n".join(lines)
        if result != "":
            blocks.append(result)
    return blocks

def block_to_block_type(text):
    if re.findall(r"^#{1,6} ", text):
        return "heading"
    if text[:3] == "```" and text[-3:] == "```":
        return "code"
    if len(re.findall(r"(?:^|\n)>", text)) == len(text.split("\n")):
        return "quote"
    if len(re.findall(r"(?:^|\n)[\*-] ", text)) == len(text.split("\n")):
        return "unordered_list"
    if re.findall(r"(?:^|\n)(\d*)\. ", text) == list(map(lambda x: str(x), range(1,len(text.split("\n")) + 1))):
        return "ordered_list"
    return "paragraph"

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    root_children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                num = len(re.findall(r"^(#{1,6}) ", block)[0])
                child_nodes = text_to_children(re.findall(r"^#{1,6} (.*)$", block)[0])
                block_node = ParentNode(f"h{num}", child_nodes)
            case "quote":
                child_nodes = text_to_children("\n".join(list(map(lambda x: x[2:], block.split("\n")))))
                block_node = ParentNode("blockquote", child_nodes)
            case "code":
                child_nodes = text_to_children(block[3:-3])
                block_node = ParentNode("pre", [ParentNode("code", child_nodes)])
            case "unordered_list":
                child_nodes = []
                for line in block.split("\n"):
                    li_child = text_to_children(line[2:])
                    child_nodes.append(ParentNode("li", li_child))
                block_node = ParentNode("ul", child_nodes)
            case "ordered_list":
                child_nodes = []
                for line in re.findall(r"(?:^|\n)\d*\. (.*)", block):
                    li_child = text_to_children(line)
                    child_nodes.append(ParentNode("li", li_child))
                block_node = ParentNode("ol", child_nodes)
            case "paragraph":
                child_nodes = text_to_children(block)
                block_node = ParentNode("p", child_nodes)
        root_children.append(block_node)
    return ParentNode("div", root_children)
        
def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == "heading":
            num = len(re.findall(r"^(#{1,6}) ", block)[0])
            if num == 1:
                return re.findall(r"^#{1,6} (.*)$", block)[0]
    raise Exception("There is no h1 on this markdown")