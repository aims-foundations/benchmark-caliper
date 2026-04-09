#!/usr/bin/env bash
# split_pdf.sh — Split a PDF into individual pages for per-page LLM extraction.
# Prerequisites: pdftk (or qpdf as fallback)
#
# Usage: ./scripts/split_pdf.sh <input.pdf> [output_dir]
# Output: Creates output_dir/page_001.pdf, page_002.pdf, etc.
#         Prints total page count to stdout.

set -euo pipefail

PDF_PATH="${1:?Usage: $0 <input.pdf> [output_dir]}"
OUTPUT_DIR="${2:-$(dirname "$PDF_PATH")/pages}"

if [[ ! -f "$PDF_PATH" ]]; then
    echo "ERROR: PDF not found at $PDF_PATH" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Get page count
get_page_count() {
    if command -v pdftk &>/dev/null; then
        pdftk "$PDF_PATH" dump_data 2>/dev/null | grep NumberOfPages | awk '{print $2}'
    elif command -v qpdf &>/dev/null; then
        qpdf --show-npages "$PDF_PATH" 2>/dev/null
    elif command -v python3 &>/dev/null; then
        python3 -c "
import subprocess
result = subprocess.run(['mdls', '-name', 'kMDItemNumberOfPages', '$PDF_PATH'],
                       capture_output=True, text=True)
count = result.stdout.strip().split('=')[-1].strip()
if count != '(null)':
    print(count)
else:
    # Fallback: count PDF page objects
    with open('$PDF_PATH', 'rb') as f:
        import re
        content = f.read()
        pages = len(re.findall(rb'/Type\s*/Page[^s]', content))
        print(pages)
" 2>/dev/null
    else
        echo "ERROR: No PDF tool found. Install pdftk or qpdf." >&2
        exit 1
    fi
}

TOTAL_PAGES=$(get_page_count)

if [[ -z "$TOTAL_PAGES" || "$TOTAL_PAGES" -eq 0 ]]; then
    echo "ERROR: Could not determine page count for $PDF_PATH" >&2
    exit 1
fi

echo "Total pages: $TOTAL_PAGES"

# Split into individual pages
if command -v pdftk &>/dev/null; then
    pdftk "$PDF_PATH" burst output "$OUTPUT_DIR/page_%03d.pdf" 2>/dev/null
    rm -f "$OUTPUT_DIR/doc_data.txt"  # pdftk creates this artifact
elif command -v qpdf &>/dev/null; then
    for i in $(seq 1 "$TOTAL_PAGES"); do
        PAGE_NUM=$(printf "%03d" "$i")
        qpdf "$PDF_PATH" --pages . "$i" -- "$OUTPUT_DIR/page_${PAGE_NUM}.pdf" 2>/dev/null
    done
else
    echo "WARN: No PDF splitter available. Pipeline will use Read tool with pages parameter." >&2
    echo "$TOTAL_PAGES"
    exit 0
fi

# Verify
SPLIT_COUNT=$(ls "$OUTPUT_DIR"/page_*.pdf 2>/dev/null | wc -l | tr -d ' ')
if [[ "$SPLIT_COUNT" -ne "$TOTAL_PAGES" ]]; then
    echo "WARN: Expected $TOTAL_PAGES pages but got $SPLIT_COUNT files" >&2
fi

echo "Split $TOTAL_PAGES pages into $OUTPUT_DIR/"
echo "$TOTAL_PAGES"
