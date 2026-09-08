# 🚀 StockAI Pro

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge&logo=qt)
![License](https://img.shields.io/badge/License-Free-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

Free, lightning-fast, and open-source Python software designed to automate the workflow of managing, organizing, and exporting AI-generated assets for Adobe Stock contributors.

## 💡 Why StockAI Pro?

Generating AI assets for microstock agencies often involves a tedious loop of copying prompts, downloading images, renaming files, and creating CSV metadata. **StockAI Pro** eliminates the friction by combining clipboard monitoring, one-click auto-picking, and automated metadata generation into a single, seamless desktop application.

### 🔄 The Core Workflow

1. **Paste Metadata:** Paste your raw text format. The app requires this exact structure to auto-parse correctly:

   ```text
   Category: Backgrounds
   Aspect Ratio: 9:16
   AI Image Generation Prompt: [Your Prompt]
   Adobe Stock Title: [Your Title]
   Adobe Stock Keywords: [Your Keywords]
   SEO Optimized File Name: [Your-File-Name]

   **Use this Prompt to achieve the exact format as above (Just put this into your current Model)**
   
From now EACH concept, you MUST output the data STRICTLY in the exact format below. Do not add any extra markdown formatting, bullet points, or numbers before the labels. The labels must be exact.

Category: [Choose ONE valid Adobe Stock category: Animals / Buildings and Architecture / Business / Drinks / The Environment / States of Mind / Food / Graphic Resources / Hobbies and Leisure / Industry / Landscapes / Lifestyle / People / Plants and Flowers / Culture and Religion / Science / Social Issues / Sports / Technology / Transport / Travel]
Aspect Ratio: [e.g., 16:9 or 9:16 or 1:1]
AI Image Generation Prompt: 
Adobe Stock Title: [A descriptive, SEO-friendly title between 5-15 words]
Adobe Stock Keywords: [Exactly 40-45 highly relevant, comma-separated keywords, ordered by importance]
SEO Optimized File Name: [a-descriptive-kebab-case-file-name-without-extension]

   
2. **Auto-Add:** The app instantly parses and adds the asset to your Pending list.
3. **1-Click Generation 🤖:** Click the Robot icon to copy the prompt to your clipboard and launch an auto-listener.
4. **Auto-Pick:** Once you download the AI image, the app instantly detects, renames, and assigns it to the asset.
5. **Bulk Export:** Click Export to generate an Adobe-ready CSV (with auto-mapped Category IDs) and a packed image folder.

---

## ✨ Key Features

*   **🤖 1-Click Auto-Pick Workflow:** Copies your AI prompt and actively listens to your `Downloads` folder. The moment the image is generated and downloaded, it automatically grabs it, preventing manual browsing.
*   **🧠 Smart Category Mapping:** Automatically reads text categories (e.g., "Culture and Religion", "Animals") and converts them into Adobe Stock's required numeric Category IDs (1-21) during CSV export.
*   **⚡ Ultra-Fast Thumbnail Engine:** Automatically generates and caches 15KB tiny thumbnails for heavy 8K/4K images to ensure the UI remains instantaneous with zero lag.
*   **📂 Automated Asset Organization:** Generates SEO-optimized filenames automatically and stores assets in dedicated folders with associated `.txt` metadata files.
*   **📝 My Custom Prompts:** A built-in advanced Notepad to save, edit, pin (📌), and manage your favorite prompt templates. Includes a 1-click bulk export to `.txt` files.
*   **🌍 Multi-Language UI:** Fully localized into 8 languages (English, Hindi, Spanish, Portuguese, Russian, Japanese, German, French) with persistent saving.
*   **🛡️ Duplicate Prevention:** Remembers previously picked downloaded files across sessions to prevent accidental duplicate uploads.

---

## 🛠️ Requirements

- **OS:** Windows 10/11
- **Language:** Python 3.x
- **Libraries:** `PyQt5`, `qtawesome`

---

## 🚀 Run from Source

```bash
# Clone the repository
git clone [https://github.com/AutomoraLabs/Stock-Ai-Pro.git](https://github.com/yourusername/Stock-Ai-Pro.git)
cd Stock-Ai-Pro

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install PyQt5 qtawesome

# Run the app
python app.py


## Build a Windows executable



For a simple local build:



```bash

pip install pyinstaller

python -m PyInstaller --noconsole --windowed --name "StockAI Pro" --icon=app_icon.ico app.py

```



If you do not have `app_icon.ico`, remove the `--icon app_icon.ico` part.



The generated executable will be placed in:



```text

dist/

```



You can then package the generated `.exe` with Inno Setup.



## Important



Stock Ai Pro is **not affiliated with Adobe Inc. or Adobe Stock**. Adobe Stock is a trademark of Adobe Inc.



## Support



Stock Ai Pro is free to use.



If you find it useful and would like to support continued development:



☕ https://www.buymeacoffee.com/rishichaurasiya



## License



Stock Ai Pro is free to use, modify, fork, contribute to, and use commercially.



The software itself may not be sold, resold, or redistributed as a paid product without prior written permission from the copyright holder.



See [LICENSE](LICENSE) for the full terms.



## Author



**Rishi Chaurasiya** 

