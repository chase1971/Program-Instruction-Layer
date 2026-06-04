# Logging Standards

Standards for user-facing log messages across applications.

---

## Emoji Catalog

Use these emojis consistently for message categories:

### Status Indicators
| Emoji | Category | When to Use |
|-------|----------|-------------|
| `✅` | Success | Operation completed successfully |
| `❌` | Error | Operation failed, needs attention |
| `⚠️` | Warning | Non-critical issue, review recommended |
| `ℹ️` | Info | Neutral information |

### Action Types
| Emoji | Category | When to Use |
|-------|----------|-------------|
| `🔍` | Searching | Looking for files, scanning |
| `📦` | Package/Bundle | ZIP files, bundling operations |
| `🔬` | Analysis | Extracting data, parsing, OCR |
| `🗑️` | Delete/Clear | Removing files, clearing data |
| `🧹` | Cleanup | Removing corrupted/old data |
| `🔄` | Process/Refresh | Reloading, restarting, killing processes |

### File/Folder Operations
| Emoji | Category | When to Use |
|-------|----------|-------------|
| `📂` | Folder | Opening folders, loading directories |
| `📁` | File location | File found, multiple files |
| `📄` | Document | PDF, individual files |
| `📋` | List/Data | Import files, grade lists, tables |

### Communication
| Emoji | Category | When to Use |
|-------|----------|-------------|
| `📡` | Network/API | Sending requests (DEBUG ONLY - hide in normal mode) |
| `📊` | Statistics | Summary counts, totals |

---

## Message Patterns

### Success Messages
```
✅ {Operation} completed!
✅ {Action} {count} {items}
```
Examples:
- `✅ Quiz processing completed!`
- `✅ Grade extraction completed successfully!`
- `✅ Auto-assigned 10 points to 25 submissions`

### Error Messages
```
❌ {What went wrong}
❌ {What went wrong} - {Suggestion to fix}
```
Examples:
- `❌ Please select a class first`
- `❌ No ZIP files found in Downloads folder`
- `❌ File is being used by another process - please close Excel and try again`

### Progress Messages
```
{emoji} {Action}...
{emoji} {Action}: {detail}
```
Examples:
- `🔍 Searching for assignment ZIP in Downloads...`
- `📦 Processing: Quiz 4 (7.1-7.4).zip`
- `🔬 Starting grade extraction...`

### Warning Messages
```
⚠️ {Issue} - {Context or suggestion}
⚠️ {Issue}: {Details}
```
Examples:
- `⚠️ ISSUES FOUND (Please Review):`
- `⚠️ Fuzzy name matches (please verify):`
- `⚠️ End-of-Line Indicator not found - adding it to column F`

---

## Log Levels / Visibility

### Normal Mode (User-Facing)
Show only:
- Success/completion messages (`✅`)
- Errors that need action (`❌`)
- Warnings that need review (`⚠️`)
- Key progress milestones (started, completed)
- Summary statistics (`📊`)

### Expanded/Debug Mode
Additionally show:
- API/network calls (`📡`)
- Technical details (paths, folder names)
- Step-by-step processing logs
- JSON output
- Verbose status updates

---

## Filtering Rules (for LogTerminal)

### HIDE in Normal Mode:
- Messages starting with `📡 Sending`
- Lines containing `[Python]` or `[Python Error]`
- JSON formatted output (`{...}`)
- Separator lines (`----`, `====`)
- Technical prefixes: `Drive:`, `Class:`, `Processing folder:`, `Full path:`
- Header banners: `QUIZ PROCESSING STARTED`, etc.

### SHOW in Normal Mode:
- Emoji-prefixed messages (except `📡`)
- Status keywords: `extracted`, `created`, `updated`, `loaded`, `processed`
- Error/warning content
- Grade extraction results (numbered student grades)

---

## Anti-Patterns

### DON'T:
```
❌ Error: Processing failed: Error: File not found  // Redundant "Error:"
❌ {"success": false, "error": "..."}  // Raw JSON to user
❌ C:\Users\chase\Documents\...  // Full paths in normal mode
```

### DO:
```
✅ Processing completed!
❌ File not found in Downloads folder
📦 Processing: Quiz 4.zip
```

---

## Message Registry

When adding new log messages:
1. Choose appropriate emoji from catalog above
2. Follow the message pattern for that type
3. Consider visibility level (normal vs expanded)
4. Update `preview_user_messages.py` if applicable

---

## Quick Reference

```
SUCCESS:  ✅ {Action} completed!
ERROR:    ❌ {Problem} - {fix suggestion}
WARNING:  ⚠️ {Issue} (please review)
SEARCH:   🔍 Searching for {target}...
PROCESS:  📦 Processing: {filename}
ANALYZE:  🔬 Starting {analysis type}...
DELETE:   🗑️ Clearing {what}...
FOLDER:   📂 Opening {folder name}...
STATS:    📊 Processed {n} {items}
```
