
## Generating Markdown from Konflux website

This crawls the Konflux documentation website using
https://github.com/paulpierre/markdown-crawler to convert the content
to Markdown, which we use to train InstructLab.

```
pip install beautifulsoup4 requests markdownify markdown-crawler
python crawl.py
```

