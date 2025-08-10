"""
main module
"""

from utils import copy_static_to_public, generate_pages_recursive


def main():
    """
    main program
    """
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
