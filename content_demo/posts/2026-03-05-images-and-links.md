---
title: "Advanced Images and Links"
date: "2026-03-05"
tags: ["markdown", "images", "links"]
---

Thanks to the `attr_list` extension, you aren't limited to plain markdown images and links.

## Using target="_blank"
By default, markdown links open in the same tab. If you want to link to an external site and open it in a new tab, just add `{: target="_blank" }` after the link.

[Example External Link](https://example.com){: target="_blank" rel="noopener"}

## Specifying Image Dimensions
You can host your images inside the `static/` folder, or link to external URLs. You can explicitly set the width and height using the same attribute syntax.

![Placeholder Graphic](https://picsum.photos/seed/generator/300/150){: width="300" height="150" style="border: 2px solid #ccc;"}
