#!/usr/bin/env python3
"""
build.py — 合并 src/ 下的 4 个 JS 文件到 main.html，输出单文件 HTML

Usage:
    python3 build.py
    python3 build.py --output dist/global_macro_interactive.html
"""

import argparse
import os
import sys

DEFAULT_OUTPUT = "global_macro_interactive.html"
SRC_DIR = "src"
FILES = ["data.js", "model.js", "render.js", "app.js"]
HTML_FILE = "main.html"


def build(output_path: str) -> None:
    src_dir = os.path.join(os.path.dirname(__file__), SRC_DIR)
    if not os.path.isdir(src_dir):
        sys.exit(f"错误：找不到源代码目录 {src_dir}/")

    html_path = os.path.join(src_dir, HTML_FILE)
    if not os.path.isfile(html_path):
        sys.exit(f"错误：找不到 {html_path}")

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    js_blocks = []
    for fname in FILES:
        fpath = os.path.join(src_dir, fname)
        if not os.path.isfile(fpath):
            sys.exit(f"错误：找不到 {fpath}")
        with open(fpath, "r", encoding="utf-8") as f:
            js_blocks.append(f.read())

    # 替换 main.html 里的 <script src="..."> 引用为内联脚本
    placeholder = (
        '<script src="data.js"></script>\n'
        '<script src="model.js"></script>\n'
        '<script src="render.js"></script>\n'
        '<script src="app.js"></script>'
    )
    if placeholder not in html:
        sys.exit("错误：main.html 中找不到预期的 <script src=...> 占位符")

    inline = "<script>\n" + "\n\n".join(js_blocks) + "\n</script>"
    out = html.replace(placeholder, inline)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(out)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✓ 构建成功：{output_path} ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="合并源代码到单文件 HTML")
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"输出文件路径（默认：{DEFAULT_OUTPUT}）",
    )
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
