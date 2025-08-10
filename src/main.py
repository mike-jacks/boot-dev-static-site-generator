"""
main module
"""

from utils import copy_static_to_dir, generate_pages_recursive
import sys


def main():
    """
    main program
    """
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # For local testing, build into docs per assignment
    output_dir = "docs"
    copy_static_to_dir(output_dir)
    generate_pages_recursive("content", "template.html", output_dir, basepath)

if __name__ == "__main__":
    main()
