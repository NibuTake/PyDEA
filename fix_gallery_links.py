"""Fix Sphinx-Gallery thumbnail links in generated HTML files."""
import re
from pathlib import Path


def fix_gallery_links(docs_dir: Path):
    """Fix gallery thumbnail links by converting span references to actual links."""

    # Pattern to match: <span class="xref std std-ref">sphx_glr_tutorials_XX_XXXX_YY_YYYY.py</span>
    pattern = re.compile(
        r'<span class="xref std std-ref">(sphx_glr_tutorials_(\d+)_(\w+)_(\d+)_([^<]+)\.py)</span>'
    )

    def replace_with_link(match):
        full_ref = match.group(1)
        section_num = match.group(2)
        section_name = match.group(3)
        file_num = match.group(4)
        file_name = match.group(5)

        # Construct the relative HTML path
        html_file = f"{file_num}_{file_name}.html"

        # Return proper link
        return f'<a class="reference internal" href="{html_file}"><span class="std std-ref">{full_ref}</span></a>'

    # Find all HTML files in tutorials directories
    html_files = list(docs_dir.glob("tutorials/**/index.html"))

    for html_file in html_files:
        print(f"Processing: {html_file}")
        content = html_file.read_text(encoding="utf-8")

        # Count replacements
        original_count = len(pattern.findall(content))

        # Replace patterns
        new_content = pattern.sub(replace_with_link, content)

        if content != new_content:
            html_file.write_text(new_content, encoding="utf-8")
            print(f"  Fixed {original_count} links")
        else:
            print(f"  No links to fix")


if __name__ == "__main__":
    docs_dir = Path(__file__).parent / "docs"
    fix_gallery_links(docs_dir)
    print("\nDone!")
