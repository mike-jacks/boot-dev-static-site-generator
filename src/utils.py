from textnode import TextType, TextNode, text_node_to_html_node
from parentnode import ParentNode
import re
from htmlnode import HTMLNode
from enum import Enum
import os

class BlockType(Enum):
    """
    BlockType Enum
    """

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"
):
    """Generate pages recursively from a content directory
    """
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"content directory not found: {dir_path_content}")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    for file in os.listdir(dir_path_content):
        if file.endswith(".md"):
            generate_page(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file.replace(".md", ".html")),
                basepath,
            )
        elif os.path.isdir(os.path.join(dir_path_content, file)):
            generate_pages_recursive(
                os.path.join(dir_path_content, file),
                template_path,
                os.path.join(dest_dir_path, file),
                basepath,
            )
        else:
            raise ValueError(f"invalid file: {file}")

def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
):
    """Generate a page from a content file and a template file
    """
    print(f"Generating page from '{from_path}' to '{dest_path}' using template '{template_path}'")
    with open(from_path, "r") as content_file:
        md_content = content_file.read()
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    title = extract_title(md_content)
    html_content = markdown_to_html_node(md_content).to_html()
    template_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    # Normalize basepath (ensure leading and trailing slash)
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    # Prefix absolute asset and link paths with basepath
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as dest_file:
        dest_file.write(template_content)

def extract_title(markdown: str) -> str:
    """Extract the title from a markdown file
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")

def copy_static_to_dir(dest_dir_path: str):
    """Copy static files to a destination folder (clears it first)."""
    if not os.path.exists("./static"):
        raise FileNotFoundError("static folder not found")
    reset_dir(dest_dir_path)
    copy_files("./static", dest_dir_path)

def copy_files(src_path: str, dst_path: str, buffer_size: int = 1024 * 1024):
    """Recursively copy files/dirs from src_path to dst_path using only os and builtins."""
    if os.path.isdir(src_path):
        os.makedirs(dst_path, exist_ok=True)
        for name in os.listdir(src_path):
            child_src = os.path.join(src_path, name)
            child_dst = os.path.join(dst_path, name)
            copy_files(child_src, child_dst, buffer_size)
        return

    # Copy a single file
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
        while True:
            chunk = src.read(buffer_size)
            if not chunk:
                break
            dst.write(chunk)
    # replicate basic permissions when possible
    try:
        src_mode = os.stat(src_path).st_mode & 0o777
        os.chmod(dst_path, src_mode)
    except OSError:
        pass

def empty_dir(path: str):
    """Empty a directory
    """
    if not os.path.exists(path):
        return
    for root, dirs, files in os.walk(path, topdown=False, followlinks=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            target = os.path.join(root, name)
            if os.path.islink(target):
                os.unlink(target)
            elif os.path.isfile(target):
                os.remove(target)
            else:
                os.rmdir(target)

def reset_dir(path: str):
    if os.path.exists(path):
        empty_dir(path)
        os.rmdir(path)
    os.makedirs(path, exist_ok=True)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div",children,None)

def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    else:
        raise ValueError(f"Invalid block type: {block_type}")

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children: list[HTMLNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children, None)

def heading_to_html_node(block: str) -> HTMLNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError("invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children, None)

def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child =  text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code], None)

def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_block_type(block: str) -> BlockType:
    """
    Convert block to block type
    """
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in block.split("\n"):
            if not re.match(r"^>", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block.split("\n"):
            if not re.match(r"^- ", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Convert markdown to blocks
    """
    split_markdown: list[str] = markdown.split("\n\n")
    blocks: list[str] = []
    for section in split_markdown:
        if len(section) == 0:
            continue
        section = section.strip()
        blocks.append(section)
    return blocks

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = []
    nodes.append(TextNode(text, TextType.TEXT))
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(old_node)
            continue
        
        for alt, src in images:
            sections = text.split(f"![{alt}]({src})", 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(old_node)
            continue

        for label, href in links:
            sections = text.split(f"[{label}]({href})", 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, href))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_pattern, text)
    return matches
