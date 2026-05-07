from playwright.sync_api import sync_playwright
import os

def export_presentation_to_pdf(html_filename, pdf_filename):
    # Sanity Check
    if not os.path.exists(html_filename):
        print(f"\n[ERROR] I cannot find '{html_filename}'!")
        print(f"Please make sure it is in this exact folder: {os.getcwd()}\n")
        return

    print(f"File '{html_filename}' located. Initiating Chromium engine...")
    
    # This is the secret CSS formula to "unroll" the presentation into a printable document
    print_css = """
    @media print {
        /* Force the document to expand beyond 1 page */
        html, body { height: auto !important; overflow: visible !important; background: #0a0d14 !important; }
        .deck { height: auto !important; position: static !important; }
        
        /* Make EVERY slide visible, static, and force a page break after it */
        .slide { 
            position: relative !important; 
            opacity: 1 !important; 
            transform: none !important; 
            height: 100vh !important; 
            page-break-after: always !important; 
            break-after: page !important;
            background: transparent !important;
            z-index: 10 !important;
        }
        
        /* Reveal all animated text immediately */
        .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
        
        /* Hide interactive UI elements that don't belong in a static PDF */
        .nav-controls, .cursor-dot, .cursor-trail, input[type="range"], .interactive-btn { 
            display: none !important; 
        }
        
        /* Lock the background effects so they appear on every page */
        .background-container { position: fixed !important; inset: 0 !important; }
        
        /* Force the browser to print the dark theme and colors accurately */
        * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    }
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        file_url = f"file://{os.path.abspath(html_filename)}"
        
        print(f"Loading {html_filename} and waiting for animations to settle...")
        page.goto(file_url, wait_until="networkidle")
        
        # Inject the CSS to prepare it for multi-page printing
        print("Injecting print-formatting overrides...")
        page.add_style_tag(content=print_css)
        
        print("Exporting all 23 slides to PDF...")
        page.pdf(
            path=pdf_filename,
            landscape=True,
            print_background=True,
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"} # Remove white borders
        )
        
        browser.close()
        print(f"Success! The full multi-page case file has been securely saved as: {pdf_filename}")

if __name__ == "__main__":
    # Ensure this exactly matches your HTML file
    input_html = "Elasticity-G8.html" 
    output_pdf = "Elasticity_Presentation_G8.pdf"
    
    export_presentation_to_pdf(input_html, output_pdf)