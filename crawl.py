from markdown_crawler import md_crawl
url = 'https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/'
print(f'🕸️ Starting crawl of {url}')
md_crawl(
    url,
    max_depth=3,
    num_threads=5,
    base_dir='markdown',
    valid_paths=['/docs.appstudio.io/Documentation/main'],
    target_content=['main.article article'],
    is_domain_match=True,
    is_base_path_match=False,
    is_debug=True
)
