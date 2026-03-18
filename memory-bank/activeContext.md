# Active Context

## Current State
Major feature expansion completed (2026-03-18). All 7 plan items implemented and tested.

## Recent Changes (this session)

### 1. Status Bar with Connection Indicator
- Persistent status bar at bottom of window
- Color-coded dot: green (connected) / red (disconnected)
- Shows "CONNECTED host:port" or "DISCONNECTED"

### 2. Save/Load Configuration Profiles (JSON)
- File > Save Profile (Ctrl+S) saves all form values + dynamic sections to JSON
- File > Load Profile (Ctrl+O) restores all values from JSON
- File > Import install.cache parses shell-style `key="value"` format
- Testable via `save_profile_to()`, `load_profile_from()`, `import_cache_from()`

### 3. SSH Key Authentication
- New `[KEY FILE]` field with `[...]` browse button in connection frame
- If keyfile is set, paramiko uses key-based auth
- Password still works as fallback (or both can be provided)

### 4. Dynamic Section Count (1-22)
- Sections stored in `self.section_entries` list of dicts (name, path, dated)
- `sections` StringVar traced; changing the count auto-rebuilds UI
- Cache generation loops dynamically over section_entries
- `_suppress_rebuild` flag prevents redundant rebuilds during bulk profile/cache loads

### 5. Tooltips
- `_ToolTip` class: binds Enter/Leave to show/hide a themed Toplevel
- Added to all connection fields and installation form fields
- Tooltip text describes each field's purpose

### 6. UX Polish
- **Confirmation dialog** before installation ("Install on {host}?")
- **Auto-switch to LOG tab** when installation starts
- **Clear Log / Export Log** buttons in log toolbar
- **Minimum window size** 800x600
- **Keyboard shortcuts**: Ctrl+S save, Ctrl+O load, Enter to connect
- **Select All / Deselect All** buttons above optional scripts
- **Connection timeout**: 10 second timeout on SSH connect
- **Menu bar**: File menu with profile save/load/import/exit

## Architecture Notes
- `VARIABLE_DEFAULTS` no longer contains section1-3 fields (managed dynamically)
- `DEFAULT_SECTIONS` defines the 3 startup sections
- `CACHE_SCHEMA` uses `_SECTIONS_MARKER` sentinel for dynamic section generation
- `_SimpleVar` now supports `trace_add()` for section count change detection
- Profile/import methods split into GUI wrappers and testable core methods

## Test Coverage
- 27 tests, all passing
- Tests cover: defaults, dynamic sections (increase/decrease/clamp/invalid), cache generation (static + dynamic + special chars), profile save/load roundtrip, cache import/roundtrip, script toggles, suppress rebuild flag

## Next Steps
- Consider adding SSH connection history/bookmarks
- Add section name suggestions dropdown (0DAY, ANIME, FLAC, etc.)
- Password strength indicator for admin password
