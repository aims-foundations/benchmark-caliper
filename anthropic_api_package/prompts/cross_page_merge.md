You receive two text fragments extracted from adjacent pages of a PDF document.
The page boundary may have split a sentence between them.

Determine if these fragments are parts of the same sentence or thought. If so,
merge them into one clean sentence. If they are clearly separate, say so.

Rules:
- If they form one sentence: output ONLY the merged text on a single line
- If they are separate sentences: output the word SEPARATE on its own line
- Remove any duplicated words or partial words at the merge point
- Do not add words that aren't in either fragment
- Preserve original wording exactly, except for merge-point cleanup
