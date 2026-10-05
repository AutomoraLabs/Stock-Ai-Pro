# Stock AI Pro

**Organize images and metadata. Export the CSV you need.**

![Windows](https://img.shields.io/badge/Windows-Desktop-0078D6?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=flat-square&logo=qt&logoColor=white)
![Version](https://img.shields.io/badge/Version-2.0-8B5CF6?style=flat-square)

Stock AI Pro is a free Windows desktop app for stock contributors, AI-image creators and anyone managing images with titles, keywords and other metadata. Turn formatted text into asset records, attach the matching images, and export your selected CSV fields.

Start with the built-in **Adobe Stock preset**, or create a custom parsing template with only the sections you need.

[Download for Windows](https://github.com/AutomoraLabs/Stock-Ai-Pro/releases/latest) · [Official website](https://www.automoralabs.store/2026/09/Stock-Ai-Pro.html) · [Report a bug](https://www.automoralabs.store/p/contact-us.html) · [Buy Me a Coffee](https://buymeacoffee.com/rishichaurasiya)

![Stock AI Pro showing Pending Assets and Attached Assets](https://res.cloudinary.com/xboahlnh/image/upload/v1791174106/dashboard-light.webp)

## How it works

1. **Choose your format.** Open Parsing Templates, select the Adobe Stock preset or create your own, then set it as default.
2. **Paste your asset details.** Matching text is parsed into records in Pending Assets. An optional Click-to-Paste toggle lets you paste from the clipboard by clicking the input area.
3. **Copy the field you need.** Click an asset’s Robot button to copy the selected template field and queue Downloads Auto-Pick. Click again to cancel that request.
4. **Generate and download, or attach manually.** Use your preferred image tool separately. Once an image is attached, its record moves to Attached Assets.
5. **Export the attached assets.** Use the Adobe preset’s CSV/image package, or export the fields selected in your custom template.
6. **Keep completed work in batches.** Mark All Upload moves attached records into Uploaded History as a separate batch.

**Stock AI Pro does not generate images or upload them to contributor websites.** Robot copies text and starts Auto-Pick; Mark All Upload records completed work locally. You generate images and submit them to your destination separately.

## Custom parsing templates

You no longer have to use one fixed Adobe-only text format.

- Create, save and delete custom templates; the Adobe Stock default preset is protected from deletion.
- Add or remove sections using placeholders such as `{title}`, `{tags}`, `{description}` or `{license}`.
- Choose which section the Robot button copies. A Prompt section is optional.
- Test sample input and inspect the parsed preview before adding assets.
- Choose the fields included in CSV export; additional sections are not automatically exported.
- Set a default template that persists after restart.
- Get a warning before closing the template editor with unsaved changes.

![Parsing Templates with custom sections and CSV field selection](https://res.cloudinary.com/xboahlnh/image/upload/v1791174106/parsing-templates.webp)

### Custom template example

```text
Title: {title}
Tags: {tags}
Description: {description}
License: {license}
```

Matching input:

```text
Title: Soft Botanical Shapes
Tags: botanical, green, minimal
Description: A minimal composition of botanical shapes on a light background
License: Personal project
```

Select **Tags** as the Robot copy field if that is what you want copied. Select only the CSV fields you need—for example, Title and Tags.

### Adobe Stock preset example

```text
Category: Graphic Resources
Aspect Ratio: 3:2
AI Image Generation Prompt: A minimal botanical composition with soft natural light
Adobe Stock Title: Minimal Botanical Composition with Soft Natural Light
Adobe Stock Keywords: botanical, minimal, natural light, green, composition
SEO Optimized File Name: minimal-botanical-composition
```

This is a parsing example. Review the image, metadata and destination requirements before submission.

## Features

| Feature | What it does |
| --- | --- |
| Pending and Attached lists | Keeps records without images separate from records ready for export. |
| Downloads Auto-Pick | Matches a queued record with a newly downloaded image; manual attachment is also available. |
| Sequential Auto Play | Starts Robot actions in pending-list order and advances after each image attaches. You still generate and download each image yourself. |
| Image previews | Shows attached thumbnails and lets you open the image from its row. |
| Sort controls | Sort by number, title or attachment priority; lock a sort choice to retain it after restart. |
| My Prompts | Save, edit, pin, delete and export reusable prompts. |
| Uploaded History | Keeps completed records in separate batches and includes Export Selected Batch. |
| Folder exports | Exports images and TXT metadata into organized subfolders. |
| Whole Settings backup | Exports/imports My Prompts, parsing templates and user settings. Asset lists and media are excluded. |
| Appearance | Light/dark modes, soft accent choices, hover feedback and layouts that adapt to window size. |
| Languages | English, Hindi, Spanish, Portuguese, Russian, Japanese, German and French. |
| Permanent history deletion | Removes uploaded assets permanently when you choose the delete action and confirm. |

<details>
<summary>View the dark interface</summary>

![Stock AI Pro dark interface](https://res.cloudinary.com/xboahlnh/image/upload/v1791174110/dashboard-dark.webp)

</details>

<details>
<summary>View Uploaded History</summary>

![Uploaded History with separate batches](https://res.cloudinary.com/xboahlnh/image/upload/v1791174109/batch-history.webp)

</details>

## CSV and file exports

**Adobe Stock preset:** exports `AdobeStock_Metadata.csv` and an `Images_To_Upload` folder. The CSV contains `Filename`, `Title`, `Keywords`, `Category` and `Releases`. Recognized category names are mapped to Adobe Stock category IDs.

**Custom templates:** export `Custom_Metadata.csv` containing the selected fields. Custom CSV export does not automatically create an Adobe-style image package; use folder export separately when needed.

Exports use attached records that have not yet been marked as uploaded. Export before moving your records into Uploaded History.

Custom templates are flexible formats, not built-in integrations with every contributor platform. Match your destination’s exact column names, required values, filename rules and CSV formatting before uploading. Images are uploaded separately from CSV metadata.

## Local workspace

The app stores its workspace in your Windows Documents folder:

```text
Documents\StockAI_Pro_Workspace\
```

Supported image formats: **JPG, JPEG, PNG and WEBP**.

Whole Settings backup is for configuration and prompt/template libraries. It is not a backup of your assets or images; export those separately.

## Run from source

Use a Python environment compatible with PyQt5. The packaged Windows release does not require a separate Python installation.

Open **Command Prompt**:

```bat
git clone https://github.com/AutomoraLabs/Stock-Ai-Pro.git
cd Stock-Ai-Pro
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install PyQt5 qtawesome
python app.py
```

Keep `app_icon.ico` beside `app.py` for the application icon.

## Build a Windows OneDir release

From the activated environment and project folder:

```bat
python -m pip install --upgrade pyinstaller pyinstaller-hooks-contrib
python -m PyInstaller --noconfirm --clean --onedir --windowed --noupx --name "App" --icon "app_icon.ico" --add-data "app_icon.ico:." --collect-data qtawesome "app.py"
```

Test the executable:

```bat
start "" "dist\App\App.exe"
```

Distribute the complete `dist\App` folder, including `_internal`. Copying only `App.exe` is not sufficient.

For an installer, use Inno Setup to copy the **contents of `dist\App`** into the installation directory, and include `app_icon.ico` for shortcuts and the uninstall entry. OneDir avoids extracting bundled dependencies on each launch; startup time still depends on the app and computer.

Build references: [PyInstaller options](https://pyinstaller.org/en/stable/usage.html) · [Inno Setup files](https://jrsoftware.org/ishelp/topic_filessection.htm)

## Support and contributions

Found a problem? [Open a GitHub issue](https://github.com/AutomoraLabs/Stock-Ai-Pro/issues) or [contact Automora Labs](https://www.automoralabs.store/p/contact-us.html). Include your app version, Windows version, steps to reproduce and a screenshot where helpful.

If the app helps your workflow, you can [support development on Buy Me a Coffee](https://buymeacoffee.com/rishichaurasiya).

## License

Stock AI Pro is free to use, modify, fork, contribute to and use commercially. The software itself may not be sold, resold or redistributed as a paid product without prior written permission from the copyright holder.

See [LICENSE](LICENSE) for the full terms. Bundled third-party libraries and fonts retain their own licenses.

Stock AI Pro is not affiliated with Adobe Inc., Adobe Stock or other contributor platforms. Platform names and trademarks belong to their respective owners.

**Created by Rishi Chaurasiya · [Automora Labs](https://www.automoralabs.store)**
