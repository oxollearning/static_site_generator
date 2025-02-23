import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text, props=None)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text, props=None)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter, maxsplit=2)
            if len(split_nodes) == 2:
                raise Exception("invalid Markdown syntax")
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            if len(split_nodes) == 3:
                new_nodes.append(TextNode(split_nodes[1], text_type))
                if split_nodes[2] != "":
                    new_nodes.extend(
                        split_nodes_delimiter(
                            [TextNode(split_nodes[2], TextType.TEXT)],
                            delimiter,
                            text_type
                        )
                    )
    return new_nodes

                
def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    #return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return re.findall(r"(?:^|[^!])\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            images = extract_markdown_images(text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                for image in images:
                    image_alt = image[0]
                    image_url = image[1]
                    split_nodes = text.split(f"![{image_alt}]({image_url})", maxsplit=1)
                    if split_nodes[0] != "":
                        new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                    text = split_nodes[1]
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            links = extract_markdown_links(text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                for link in links:
                    link_text = link[0]
                    link_url = link[1]
                    split_nodes = text.split(f"[{link_text}]({link_url})", maxsplit=1)
                    if split_nodes[0] != "":
                        new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                    text = split_nodes[1]
                if text != "":
                    new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
