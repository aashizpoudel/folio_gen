---
title: "Markdown Features Overview"
date: "2026-03-01"
tags: ["markdown", "tutorial"]
---

This static site generator uses Python's `markdown` library with several powerful extensions enabled. 

Here is a quick overview of what you can do natively!

### Code Blocks
You can use standard fenced code blocks with language identifiers.

```python
def hello_world():
    print("This will be syntax highlighted if you add a CSS theme!")
```

### Tables
Tables are supported out of the box.

| Feature | Supported | Notes |
|---------|-----------|-------|
| Tables | Yes | Using the `tables` extension |
| Fenced Code | Yes | Using `fenced_code` |
| Attributes | Yes | Using `attr_list` |
