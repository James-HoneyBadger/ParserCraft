# ParserCraft CLI Reference

Complete guide to ParserCraft command-line tools for language configuration management.

## Installation

CLI tools are included when you install ParserCraft:

```bash
pip install -e .
```

Available commands:
- `parsercraft` - Main language configuration tool
- `parsercraft-ide` - Launch ParserCraft IDE

## Commands

### create

Create a new language configuration.

```bash
parsercraft create [OPTIONS]
```

**Options:**
- `--preset PRESET` - Start from template (default: minimal)
- `--output FILE` - Save to file (default: output.yaml)
- `--format FORMAT` - Output format: yaml or json
- `--interactive` - Interactive creation wizard

**Presets:**
- `minimal` - Bare minimum configuration
- `python_like` - Python-style syntax

**Presets:**
- `minimal` - Bare minimum configuration
- `python_like` - Python-style syntax
- `javascript_like` - JavaScript-style syntax
- `lisp_like` - Lisp-style syntax
- `teachscript` - Educational language
- `pascal_like` - Pascal-style syntax
- `ruby_like` - Ruby-style syntax

**Examples:**
```bash
# Create Python-like language
parsercraft create --preset python_like --output spanish.yaml

# Create interactive
parsercraft create --interactive

# Create as JSON
parsercraft create --preset minimal --output config.json --format json
```

### edit

Edit an existing configuration file.

```bash
parsercraft edit FILE [OPTIONS]
```

**Options:**
- `--key KEY` - Edit specific configuration key
- `--value VALUE` - Set specific value
- `--keyword OLD NEW` - Rename keyword
- `--function NAME DESC` - Add function
- `--remove-keyword KW` - Remove keyword
- `--remove-function FN` - Remove function

**Examples:**
```bash
# Interactive edit
parsercraft edit my_lang.yaml

# Rename keyword
parsercraft edit my_lang.yaml --keyword if cuando

# Add function
parsercraft edit my_lang.yaml --function say "print output"
```

### validate

Check if a configuration is valid.

```bash
parsercraft validate FILE [OPTIONS]
```

**Options:**
- `--strict` - Enforce strict validation
- `--verbose` - Show detailed output
- `--fix` - Attempt automatic fixes

**Examples:**
```bash
# Simple validation
parsercraft validate spanish.yaml

# Verbose output
parsercraft validate spanish.yaml --verbose

# Auto-fix issues
parsercraft validate spanish.yaml --fix
```

### info

Display configuration information.

```bash
parsercraft info [FILE]
```

**Options:**
- `--keywords` - Show only keywords
- `--functions` - Show only functions
- `--syntax` - Show syntax settings
- `--all` - Show complete information (default)

**Examples:**
```bash
# Show all info
parsercraft info spanish.yaml

# Show only keywords
parsercraft info spanish.yaml --keywords

# Show functions
parsercraft info spanish.yaml --functions
```

### export

Export configuration to different formats.

```bash
parsercraft export FILE [OPTIONS]
```

**Options:**
- `--format FORMAT` - Output format: markdown, html, json, yaml, pdf
- `--output FILE` - Save to file
- `--include SECTIONS` - Include specific sections (keywords, functions, syntax)

**Examples:**
```bash
# Export as markdown documentation
parsercraft export spanish.yaml --format markdown --output docs.md

# Export as HTML
parsercraft export spanish.yaml --format html --output reference.html

# Export as JSON
parsercraft export spanish.yaml --format json --output config.json
```

### import

Load a configuration from file.

```bash
parsercraft import FILE [OPTIONS]
```

**Options:**
- `--scope SCOPE` - Installation scope: runtime, project, user
- `--as NAME` - Import with different name
- `--validate` - Validate after import

**Examples:**
```bash
# Import to user scope
parsercraft import spanish.yaml --scope user

# Import to project
parsercraft import spanish.yaml --scope project --as my_spanish
```

### list-presets

List all available language presets.

```bash
parsercraft list-presets [OPTIONS]
```

**Options:**
- `--details` - Show details of each preset
- `--category CATEGORY` - Filter by category
- `--search TERM` - Search presets

**Examples:**
```bash
# List all presets
parsercraft list-presets

# Show detailed info
parsercraft list-presets --details

# Search for python
parsercraft list-presets --search python
```

### convert

Convert configuration between formats.

```bash
parsercraft convert FILE --to FORMAT [OPTIONS]
```

**Supported formats:** yaml, json, toml

**Options:**
- `--to FORMAT` - Target format (required)
- `--output FILE` - Save to file
- `--validate` - Validate before converting

**Examples:**
```bash
# Convert YAML to JSON
parsercraft convert spanish.yaml --to json --output spanish.json

# Convert JSON to YAML
parsercraft convert config.json --to yaml
```

### diff

Compare two configurations.

```bash
parsercraft diff FILE1 FILE2 [OPTIONS]
```

**Options:**
- `--keywords-only` - Compare only keywords
- `--functions-only` - Compare only functions
- `--unified` - Unified diff format
- `--ignore-order` - Ignore order differences

**Examples:**
```bash
# Compare two language configs
parsercraft diff spanish.yaml french.yaml

# Show only keyword differences
parsercraft diff spanish.yaml french.yaml --keywords-only

# Show functions that differ
parsercraft diff spanish.yaml french.yaml --functions-only
```

### update

Modify specific aspects of a configuration.

```bash
parsercraft update FILE [OPTIONS]
```

**Options:**
- `--set KEY VALUE` - Set configuration value
- `--merge FILE` - Merge with another config
- `--delete KEY` - Delete configuration key
- `--rename OLD NEW` - Rename keyword/function
- `--output FILE` - Save result to file

**Examples:**
```bash
# Set array indexing
parsercraft update spanish.yaml --set array_indexing 0

# Merge configurations
parsercraft update spanish.yaml --merge base.yaml

# Rename keyword
parsercraft update spanish.yaml --rename si when --output spanish_updated.yaml
```

### repl

Launch interactive configuration REPL.

```bash
parsercraft repl [FILE] [OPTIONS]
```

**Options:**
- `--debug` - Enable debug mode
- `--history` - Load previous REPL history
- `--no-defaults` - Don't load defaults

**Examples:**
```bash
# Interactive REPL (start from scratch)
parsercraft repl

# REPL with existing config
parsercraft repl spanish.yaml --debug

# REPL with history
parsercraft repl spanish.yaml --history
```

**REPL Commands:**
- `list keywords` - Show all keywords
- `list functions` - Show all functions
- `add keyword if cuando` - Add keyword
- `remove keyword if` - Remove keyword
- `set array_indexing 0` - Set option
- `validate` - Validate current config
- `save file.yaml` - Save to file
- `load file.yaml` - Load from file
- `exit` - Exit REPL

### batch

Execute batch operations from script.

```bash
parsercraft batch SCRIPT [OPTIONS]
```

**Options:**
- `--output DIR` - Output directory for generated files
- `--verbose` - Show all operations
- `--continue-on-error` - Don't stop on errors

**Batch Script Format:**
```
# Comments start with #
create --preset python_like spanish.yaml
edit spanish.yaml --keyword if si
edit spanish.yaml --keyword def define
validate spanish.yaml
export spanish.yaml --format markdown docs.md
```

**Example:**
```bash
parsercraft batch build_languages.batch --output generated/
```

### test

Translate, run, and verify test cases defined in YAML or JSON.

```bash
parsercraft test --config CONFIG.yaml --tests cases.yaml [--show-translation] [--stop-on-fail]
```

**Test file format (YAML):**
```yaml
- name: prints hello
	source: |
		print("hello")
	expect_stdout: "hello"
- name: sets variable
	source: |
		x = 2 + 3
	expect_vars:
		x: 5
```

**Options:**
- `--config` - Language configuration file
- `--tests` - Test cases file (YAML or JSON list)
- `--show-translation` - Print translated Python per case
- `--stop-on-fail` - Abort after first failure
- `--debug` - Show stack traces on execution errors

## Global Options

All commands support these options:

```bash
--help              # Show command help
--version           # Show version
--verbose           # Verbose output
--quiet             # Suppress output
--config FILE       # Use alternate config file
```

## Examples

### Complete Workflow

```bash
# Create a new language
parsercraft create --preset python_like --output mydata.yaml

# Edit keywords
parsercraft edit mydata.yaml --keyword if cuando
parsercraft edit mydata.yaml --keyword def funcion
parsercraft edit mydata.yaml --keyword return devolver

# Validate
parsercraft validate mydata.yaml --verbose

# Export documentation
parsercraft export mydata.yaml --format markdown --output mydata_docs.md

# Show info
parsercraft info mydata.yaml --all

# Launch IDE to test
parsercraft-ide
```

### Automation with Batch

Create `build.batch`:
```
# Build multiple language variants
create --preset python_like spanish.yaml
create --preset python_like french.yaml
create --preset python_like italian.yaml

edit spanish.yaml --keyword if si
edit french.yaml --keyword if si
edit italian.yaml --keyword if se

validate spanish.yaml
validate french.yaml
validate italian.yaml

export spanish.yaml --format markdown docs/spanish.md
export french.yaml --format markdown docs/french.md
export italian.yaml --format markdown docs/italian.md
```

Then run:
```bash
parsercraft batch build.batch --output languages/
```

## Troubleshooting

### Command not found

Make sure ParserCraft is installed:
```bash
pip install -e .
```

### Permission denied

On Linux/macOS, make scripts executable:
```bash
chmod +x run-codecraft.sh
```

### Configuration validation fails

Check syntax:
```bash
parsercraft validate myfile.yaml --verbose
```

Auto-fix:
```bash
parsercraft validate myfile.yaml --fix
```

## See Also

- [API Reference](API_REFERENCE.md) - Python API
- [Configuration Reference](CONFIG_REFERENCE.md) - YAML schema
- [ParserCraft IDE](../guides/CODEX_DEVELOPER_GUIDE.md) - GUI alternative
