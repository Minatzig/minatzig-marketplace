# Converting existing PDF or Word material

The MCP accepts only Markdown (`.md`) and ZIP (Markdown plus images). PDF and Word files must be converted before upload.

## First: does the person want a conversion?

If they only want an existing manual uploaded as it is, tell them the Minatzig dashboard accepts PDF and Word files directly under **Enseñale a la IA**. No conversion is needed for that. Offer the conversion when they want it improved, split by audience, or uploaded from here.

## Order of work

1. **Sensitive data first.** Old manuals are where real customer names, emails and screenshots with real data usually are. Extract the text, scan it against [audiences.md](audiences.md#sensitive-data), and report findings before doing anything else.
2. **Extract the text** with whatever is available on the machine, checking first and installing only with the person's permission:
   - `.docx`: `pandoc file.docx -t gfm` keeps headings, lists and tables. Without pandoc, use Python with `python-docx`.
   - `.pdf`: `pdftotext -layout file.pdf -` or Python with `pdfplumber`. If almost no text comes out, the PDF is scanned. Say so, since it has no text to convert.
   - `.doc` (old Word): ask the person to save it as `.docx` first.
3. **Images.** This version converts text only. List every image or figure you could not carry over, with its page or position and what it seemed to show from the surrounding text. Then ask the person to export the ones worth keeping as PNG or JPEG into an `images/` folder. Insert them where they belong once they arrive.
4. **Restructure** to the writing rules: one topic per document (a long manual often becomes several documents), real `#`/`##` headings instead of bold or enlarged text, self-contained sections, numbered steps.
5. **Audience.** Old manuals often mix customer steps with internal notes. Apply the split in [audiences.md](audiences.md).
6. Continue with step 5 of the main workflow (show the draft) and onwards.

Keep the person's original file untouched. Write the converted files next to it, or in a new folder.
