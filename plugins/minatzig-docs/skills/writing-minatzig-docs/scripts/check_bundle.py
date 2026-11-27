#!/usr/bin/env python3
"""Check a Minatzig knowledge-base file (.md or .zip) before upload.

Usage:
    python3 check_bundle.py <file.md|file.zip> [--max-bytes N] [--max-megapixels N]
                            [--keep-types png,jpg,jpeg] [--convert-types gif,webp]

Pass the limits returned by the MCP's get_authoring_guide. The defaults below
match the guide at the time of writing, but the guide is the source of truth.

Prints one line per finding:
    ERROR: ...   the upload would fail or lose content. Fix before uploading.
    WARN:  ...   allowed, but likely to hurt answers. Tell the person.
Exits 1 if there is any ERROR, otherwise 0. Uses only the standard library.
"""

import argparse
import os
import re
import struct
import sys
import zipfile
from pathlib import PurePosixPath

# Image types the server keeps as they are. Override with --keep-types.
DEFAULT_KEEP_TYPES = {"png", "jpg", "jpeg"}
# Image types the server converts. Allowed, with a warning. Override with --convert-types.
DEFAULT_CONVERT_TYPES = {"gif", "webp"}
# Largest image the server accepts, in megapixels. Override with --max-megapixels.
DEFAULT_MAX_MEGAPIXELS = 40.0

# File and folder names: lowercase letters, digits and hyphens, then an extension.
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.[a-z0-9]+$")

IMAGE_REF_RE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_IMG_RE = re.compile(r"<img\b", re.IGNORECASE)
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

# Phrases that usually mean a section depends on another one.
CROSS_REF_RE = re.compile(
    r"\b(como se (explic[oó]|mencion[oó]|indic[oó]|vio)|ver (arriba|abajo|la secci[oó]n anterior)"
    r"|(m[aá]s )?arriba se|en la secci[oó]n anterior|en el documento (de clientes|para clientes|interno)"
    r"|as (explained|mentioned|described|shown) (above|earlier|before)|see (above|below|the previous section))\b",
    re.IGNORECASE,
)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def print_and_exit(self):
        for msg in self.errors:
            print(f"ERROR: {msg}")
        for msg in self.warnings:
            print(f"WARN:  {msg}")
        if not self.errors and not self.warnings:
            print("OK: no problems found")
        elif not self.errors:
            print("OK: no errors (see warnings)")
        sys.exit(1 if self.errors else 0)


def check_name(name, report, what):
    if not NAME_RE.match(name):
        report.error(
            f"{what} name '{name}' must be lowercase letters, digits and hyphens only "
            f"(no spaces, accents, ñ, underscores or capitals), e.g. 'alta-cliente-paso-2.png'"
        )


def image_size(data):
    """Return (width, height) for PNG, JPEG or GIF bytes, or None if unknown."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            # SOF markers carry the frame size; skip DHT (C4), JPG (C8) and DAC (CC).
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5 : i + 9])
                return w, h
            seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + seg_len
    return None


def strip_code(text):
    """Remove fenced and inline code so examples inside them are not checked."""
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def check_markdown(text, report, images_in_bundle, is_zip):
    """Check the Markdown text. Returns the set of image paths it references."""
    prose = strip_code(text)
    referenced = set()

    h1 = [l for l in prose.splitlines() if re.match(r"^#\s+\S", l)]
    h2 = [l for l in prose.splitlines() if re.match(r"^##\s+\S", l)]
    if not h1:
        report.warn("no '# Title' line: the file name will be used as the document title")
    elif len(h1) > 1:
        report.warn(f"{len(h1)} '# ' titles found: use a single '# ' title and '##' for sections")
    if not h2:
        report.warn("no '##' sections: the document is chunked by headings, so add one per topic or procedure")

    if HTML_IMG_RE.search(prose):
        report.error("HTML <img> tags are not processed: use ![description](images/name.png)")

    for alt, target in IMAGE_REF_RE.findall(prose):
        if re.match(r"^[a-z]+://", target, re.IGNORECASE) or target.startswith("//"):
            report.error(f"remote image '{target}' is ignored: put the file in images/ and reference it there")
            continue
        path = PurePosixPath(target.lstrip("./"))
        if not alt.strip():
            report.warn(f"image '{target}' has no description between the [ ]")
        if not is_zip:
            report.error(
                f"image '{target}' is referenced from a loose .md, so it will not be processed: "
                f"deliver a .zip with the .md and an images/ folder"
            )
            continue
        if path.parts[:1] != ("images",) or len(path.parts) != 2:
            report.error(f"image '{target}' must be referenced as images/<name> (directly inside images/)")
            continue
        referenced.add(str(path))
        if str(path) not in images_in_bundle:
            report.error(f"image '{target}' is referenced but missing from the zip (the whole upload is rejected)")

    for line_no, line in enumerate(prose.splitlines(), 1):
        m = CROSS_REF_RE.search(line)
        if m:
            report.warn(
                f"line {line_no}: '{m.group(0)}' points to another section or document; "
                f"sections are retrieved alone, so restate or name what is needed"
            )
    return referenced


def check_zip(path, report, args):
    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        report.error("not a valid zip file")
        return
    with zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        md_files = [n for n in names if n.lower().endswith(".md")]
        images = {}

        if len(md_files) != 1:
            report.error(f"the zip must contain exactly one .md file, found {len(md_files)}: {md_files or 'none'}")
        for md in md_files:
            if "/" in md:
                report.error(f"'{md}' must be at the root of the zip, not inside a folder")

        for name in names:
            p = PurePosixPath(name)
            if name in md_files:
                check_name(p.name, report, "Markdown file")
                continue
            if p.parts[0] != "images" or len(p.parts) != 2:
                report.error(f"'{name}' is not allowed: the zip may only hold the .md and images/<file>")
                continue
            check_name(p.name, report, "Image")
            ext = p.suffix.lower().lstrip(".")
            if ext in args.keep_types:
                pass
            elif ext in args.convert_types:
                report.warn(f"'{name}' ({ext}) will be converted by the server; PNG or JPEG is safer")
            else:
                allowed = ", ".join(sorted(args.keep_types | args.convert_types))
                report.error(f"'{name}': image type '{ext}' is not accepted (allowed: {allowed})")
            data = zf.read(name)
            images[name] = data
            size = image_size(data)
            if size:
                mp = size[0] * size[1] / 1_000_000
                if mp > args.max_megapixels:
                    report.error(f"'{name}' is {size[0]}x{size[1]} ({mp:.1f} MP), over the {args.max_megapixels:g} MP limit")

        if len(md_files) == 1:
            md_name = md_files[0]
            stem_zip = PurePosixPath(os.path.basename(path)).stem
            if PurePosixPath(md_name).stem != stem_zip:
                report.warn(f"zip '{os.path.basename(path)}' and '{md_name}' should share a name")
            text = zf.read(md_name).decode("utf-8", errors="replace")
            referenced = check_markdown(text, report, set(images), is_zip=True)
            for name in sorted(set(images) - referenced):
                report.warn(f"'{name}' is not referenced in the text, so it will be ignored")
            if not images:
                report.warn("the zip has no images: a single .md file is enough")


def main():
    ap = argparse.ArgumentParser(description="Check a Minatzig knowledge-base file before upload.")
    ap.add_argument("file", help="the .md or .zip to check")
    ap.add_argument("--max-bytes", type=int, help="maximum file size from get_authoring_guide")
    ap.add_argument("--max-megapixels", type=float, default=DEFAULT_MAX_MEGAPIXELS)
    ap.add_argument("--keep-types", default=",".join(sorted(DEFAULT_KEEP_TYPES)))
    ap.add_argument("--convert-types", default=",".join(sorted(DEFAULT_CONVERT_TYPES)))
    args = ap.parse_args()
    args.keep_types = {t.strip().lower() for t in args.keep_types.split(",") if t.strip()}
    args.convert_types = {t.strip().lower() for t in args.convert_types.split(",") if t.strip()}

    report = Report()
    path = args.file
    if not os.path.isfile(path):
        report.error(f"file not found: {path}")
        report.print_and_exit()

    base = os.path.basename(path)
    check_name(base, report, "File")
    size = os.path.getsize(path)
    if args.max_bytes is None:
        report.warn("size not checked: pass --max-bytes from get_authoring_guide")
    elif size > args.max_bytes:
        report.error(
            f"file is {size:,} bytes, over the {args.max_bytes:,} byte limit; "
            f"usually the images are too large: crop them and save at screen resolution"
        )

    ext = base.lower().rsplit(".", 1)[-1] if "." in base else ""
    if ext == "zip":
        check_zip(path, report, args)
    elif ext == "md":
        with open(path, encoding="utf-8", errors="replace") as f:
            check_markdown(f.read(), report, set(), is_zip=False)
    else:
        report.error(f"'{base}': only .md or .zip can be uploaded through the MCP (convert PDF/Word first)")

    report.print_and_exit()


if __name__ == "__main__":
    main()
