# 📁 How to Add Your Data Files

## 🎯 Quick Start - Add Your Files

### Step 1: Choose a Folder

Copy your files to any of these folders:

```text
📁 RAG/
├── data/
│   ├── books/          ← Stories, novels, literature
│   ├── documents/      ← General documents, reports
│   ├── research/       ← Research papers, studies
│   └── manuals/        ← User guides, documentation
```

### Step 2: Supported File Types

✅ **Markdown files** (`.md`) - Best for text content  
✅ **Text files** (`.txt`) - Plain text documents  
✅ **PDF files** (`.pdf`) - Reports, papers, books  
✅ **Word documents** (`.docx`) - Microsoft Word files

### Step 3: Add Your Files

#### Option A: Using File Explorer

1. Open `c:\Users\2005g\Downloads\RAG\data\`
2. Choose the appropriate subfolder
3. Copy/paste your files there

#### Option B: Using Command Line

```bash
# Copy a file to the books folder
copy "C:\path\to\your\document.pdf" "data\books\"

# Copy multiple files
copy "C:\path\to\your\files\*.*" "data\documents\"
```

### Step 4: Regenerate Database

After adding files, run:

```bash
python create_database_multi_folder.py
```

## 📋 Examples of What You Can Add

### Books & Literature (`data/books/`)

- Novels (PDF, TXT, MD)
- Short stories
- Poetry collections
- Classic literature

### Documents (`data/documents/`)

- Company reports
- Meeting notes
- Presentations (converted to text)
- Articles

### Research (`data/research/`)

- Academic papers
- Research reports
- Scientific studies
- Technical documentation

### Manuals (`data/manuals/`)

- User guides
- API documentation
- How-to guides
- Technical manuals

## 🔧 Advanced: Custom Folders

### Add New Folder Types

1. Create new folder: `mkdir data/newfolder`
2. Edit `create_database_multi_folder.py`
3. Add `"data/newfolder"` to the `DATA_PATHS` list

### File Processing Tips

- **Large files**: Will be automatically chunked into smaller pieces
- **Multiple formats**: Mix different file types in the same folder
- **Organization**: Use subfolders for better organization
- **Naming**: Use descriptive filenames for better source tracking

## 🚀 Quick Test

### Add a sample file

Create a simple text file in `data/documents/`:

```text
data/documents/test.md
```

### Regenerate database

```bash
python create_database_multi_folder.py
```

### Query your new data

```bash
python query_data_gemini.py "What information is in the test document?"
```

## ⚠️ Important Notes

- **File Size**: Large files are automatically split into chunks
- **Encoding**: Use UTF-8 encoding for text files
- **Updates**: Regenerate database after adding/removing files
- **Backups**: Database is recreated each time (old data is replaced)

## 🎯 Real-World Examples

### Company Knowledge Base

```text
data/
├── documents/
│   ├── company_policies.pdf
│   ├── employee_handbook.docx
│   └── quarterly_reports/
├── manuals/
│   ├── software_guide.md
│   ├── api_documentation.pdf
│   └── troubleshooting.txt
```

### Research Collection

```text
data/
├── research/
│   ├── ai_papers/
│   ├── market_analysis.pdf
│   └── competitor_research.md
├── documents/
│   ├── project_notes.txt
│   └── meeting_minutes/
```

Start by adding just one or two files to test the system, then gradually build your knowledge base! 🚀
