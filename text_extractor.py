"""Unified text extractor for all sources."""

from pathlib import Path
from src.extractors.link_to_text import extract_article_text
from src.extractors.pdf_to_text import extract_text_from_pdf
from src.extractors.youtube_to_text import extract_video_id, extract_transcript


def main():
    all_text = []
    total_processed = 0
    
    # Extract from links.txt
    links_file = Path('input/links.txt')
    if links_file.exists():
        with open(links_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"Found {len(urls)} URL(s) in links.txt")
        for url in urls:
            print(f"Processing URL: {url}")
            try:
                data = extract_article_text(url)
                all_text.append(f"=== {data['title']} ===\nURL: {url}\n\n{data['text']}")
                print("Extracted successfully")
                total_processed += 1
            except Exception as e:
                print(f"Error: {e}")
    
    # Extract from yt.txt
    yt_file = Path('input/yt.txt')
    if yt_file.exists():
        with open(yt_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"Found {len(urls)} YouTube URL(s) in yt.txt")
        for url in urls:
            print(f"Processing YouTube: {url}")
            try:
                video_id = extract_video_id(url)
                if video_id:
                    text = extract_transcript(video_id)
                    all_text.append(f"=== YouTube: {video_id} ===\nURL: {url}\n\n{text}")
                    print("Extracted successfully")
                    total_processed += 1
            except Exception as e:
                print(f"Error: {e}")
    
    # Extract from PDFs
    input_dir = Path('input')
    if input_dir.exists():
        pdf_files = list(input_dir.glob('*.pdf'))
        if pdf_files:
            print(f"Found {len(pdf_files)} PDF file(s)")
        for pdf_file in pdf_files:
            print(f"Processing PDF: {pdf_file.name}")
            try:
                text = extract_text_from_pdf(str(pdf_file))
                all_text.append(f"=== {pdf_file.name} ===\n\n{text}")
                print("Extracted successfully")
                total_processed += 1
            except Exception as e:
                print(f"Error: {e}")
    
    # Save all to single file
    if total_processed > 0:
        Path('output').mkdir(exist_ok=True)
        with open('output/extracted_text.txt', 'w', encoding='utf-8') as f:
            f.write("\n\n" + "="*80 + "\n\n".join(all_text))
        print(f"\nCompleted! Processed {total_processed} item(s)")
        print(f"All text saved to output/extracted_text.txt")
    else:
        print("\nNo files or links found to process")
        print("Add URLs to input/links.txt, input/yt.txt, or PDFs to input/")


if __name__ == "__main__":
    main()