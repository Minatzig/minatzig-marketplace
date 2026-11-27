# Minatzig plugin for Claude Code

This plugin helps you write documentation for your Minatzig knowledge base and upload it from Claude Code.
It connects Claude Code to Minatzig and adds a skill that writes, restructures and splits documents for customers or for your team.
Before anything is uploaded, Claude shows you a summary and waits for your yes.

## What you need first

- A Minatzig user with permission to upload documentation.
- Claude Code installed.

## Install

1. Add this marketplace. Replace `<marketplace>` with the path to this folder, or with the repository you were given:

   ```bash
   claude plugin marketplace add <marketplace>
   ```

2. Install the plugin:

   ```bash
   claude plugin install minatzig-docs@minatzig
   ```

3. Start a new Claude Code session, or run `/reload-plugins` in an open one.

If you already added a Minatzig MCP server by hand with the same URL, remove it first with `claude mcp remove <name>`: a manually added server takes precedence over the plugin's.

## First use

1. In Claude Code, run `/mcp`, choose `plugin:minatzig-docs:minatzig` and sign in with your Minatzig user.
2. Ask for a document in your own words, for example: "Write a customer FAQ about invoicing for our product and upload it to Minatzig." You can also give Claude notes, an existing Markdown file or a PDF or Word manual to convert.
3. To start the skill directly, run `/minatzig-docs:writing-minatzig-docs`.

Claude asks about the product, version and audience when they are not clear, shows you the draft, and uploads only after you confirm.

## Update

```bash
claude plugin marketplace update minatzig
claude plugin update minatzig-docs@minatzig
```

Then restart Claude Code.

## Remove

```bash
claude plugin uninstall minatzig-docs@minatzig
claude plugin marketplace remove minatzig
```
