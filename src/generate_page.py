from block_markdown import markdown_to_html_node, extract_title
import os
import pathlib

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    src_file = open(from_path, 'r')
    markdown = src_file.read()
    src_file.close()

    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()

    html = markdown_to_html_node(markdown).to_html()
    result = template.replace("{{ Content }}", html)

    title = extract_title(markdown)
    result = result.replace("{{ Title }}", title)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    result_file = open(dest_path, "w")
    result_file.write(result)
    result_file.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        content_item_path =  os.path.join(dir_path_content, item)
        if os.path.isfile(content_item_path):
            dest_item_name = pathlib.Path(item).stem + ".html"
            dest_item_path = os.path.join(dest_dir_path, dest_item_name)
            generate_page(
                content_item_path,
                template_path,
                dest_item_path
            )
        else:
            dest_item_path = os.path.join(dest_dir_path, item)
            generate_page_recursive(
                content_item_path,
                template_path,
                dest_item_path
            )