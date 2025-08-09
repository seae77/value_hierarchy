import os
import re
import PyPDF2


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyPDF2."""
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def parse_pdf_text(text):
    """
    Parse the PDF text into a list of blocks.
    
    Assumes that the PDF has:
      - A title as the first non-empty line.
      - Then several blocks each starting with a line "Hypothesis: Hx"
      - Followed by "Vignette:" and the vignette text, then one or more "Question:" lines.
    """
    lines = text.splitlines()

    # Extract the title: first non-empty line
    title = None
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if title is None and stripped:
            title = stripped
            continue  # Do not add the title to new_lines (it won't be shown to participants)
        new_lines.append(line)
    # Rebuild text without the title line.
    text = "\n".join(new_lines)

    # Regular expressions for markers
    hypothesis_re = re.compile(r"^Hypothesis:\s*(H\d+)")
    vignette_re = re.compile(r"^Vignette:")
    # The Question marker can optionally include additional info in parentheses.
    question_re = re.compile(r"^Question(?:\s*\(.*?\))?:")

    blocks = []
    current_block = None
    current_section = None  # either 'vignette' or 'question'

    for line in text.splitlines():
        line = line.rstrip()
        # Check for Hypothesis marker.
        hyp_match = hypothesis_re.match(line)
        if hyp_match:
            # If an existing block exists, save it.
            if current_block is not None:
                blocks.append(current_block)
            # Start a new block; attach the file title to it.
            current_block = {"title": title,
                             "hypothesis": hyp_match.group(1),
                             "vignette": "",
                             "questions": []}
            current_section = None
            continue

        # Check for Vignette marker.
        if vignette_re.match(line):
            current_section = "vignette"
            continue

        # Check for Question marker.
        if question_re.match(line):
            current_section = "question"
            # Start a new question entry.
            current_block["questions"].append("")
            # Remove the marker (but keep any extra text after the marker) and add it.
            line: str = question_re.sub("", line).strip()
            if line:
                current_block["questions"][-1] += line + " "
            continue

        # Append line to the current section.
        if current_section == "vignette":
            current_block["vignette"] += line + " "
        elif current_section == "question":
            if current_block["questions"]:
                current_block["questions"][-1] += line + " "

    # Append the last block if present.
    if current_block is not None:
        blocks.append(current_block)

    return blocks


def generate_qualtrics_txt(blocks):
    """
    Generate a Qualtrics-compatible TXT string from the list of blocks.
    Each block is formatted with a header containing both the title and hypothesis.
    """
    output_lines = []
    for block in blocks:
        # Block header with title and hypothesis
        output_lines.append(f"[[Block: {block['title']} - {block['hypothesis']}]]")
        # Vignette narrative
        output_lines.append(block['vignette'].strip())
        output_lines.append("")  # blank line
        # Each question preceded by a 'Question:' marker.
        for question in block['questions']:
            output_lines.append("Question:")
            output_lines.append(question.strip())
            output_lines.append("")  # blank line between questions
    return "\n".join(output_lines)


def main():
    # Set the folder path containing your PDF files.
    folder_path = r"C:\Users\SebastianAeschbach(G\Dropbox\Cursus\Cursus_Psychology\Master"  # <-- Change this to your folder path
    output_filename = "QualtricsSurvey.txt"
    all_blocks = []

    # Process each PDF file in the folder.
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {pdf_path}...")
            pdf_text = extract_text_from_pdf(pdf_path)
            blocks = parse_pdf_text(pdf_text)
            all_blocks.extend(blocks)

    # Generate the Qualtrics TXT content.
    output_text = generate_qualtrics_txt(all_blocks)

    # Write the output file (ensure UTF-8 encoding).
    with open(output_filename, "w", encoding = "utf-8") as f:
        f.write(output_text)

    print(f"Output written to {output_filename}")


if __name__ == "__main__":
    main()
