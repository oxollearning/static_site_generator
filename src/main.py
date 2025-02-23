from textnode import TextNode, TextType
from htmlnode import LeafNode
from copystatic import copy_dir
from generate_page import generate_page_recursive
import os
import shutil

static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_path = "./template.html"

def main():
    #node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    #print(node)
    print("Deleting public directory")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    print("Copying static files to public directory")
    copy_dir(static_dir, public_dir)
    generate_page_recursive(
        content_dir,
        template_path,
        public_dir,
    )

if __name__ == "__main__":
    main()