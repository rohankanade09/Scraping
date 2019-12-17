import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

seo_tags = []

# SEO TAG EXTRACTOR FUCNTION
def SEO_Tag_Extractor(url):

    seo_tags.clear()
    blog_url = url

    blog_req = requests.get(blog_url)
    blog_html = BeautifulSoup(blog_req.text,"html.parser")

# SEO TAG EXTRACTOR FROM META TAG
    try:
        keywords = blog_html.findAll(attrs={"name": re.compile(r"keywords", re.I)})
        seo_tags.append(keywords[0]['content'])
    except Exception:
        print("Name Exception ::", Exception)
        pass

    try:
        keywords = blog_html.findAll(attrs={"property": re.compile(r"keywords", re.I)})
        seo_tags.append(keywords[0]['content'])
    except Exception:
        print("Property Exception ::", Exception)
        pass


    return seo_tags


if __name__ == '__main__':

    tag_list = []
    topic_class_df = pd.read_csv('dataset.csv')
    tags_df = pd.DataFrame(columns=["tags"])

    for url in topic_class_df['link']:
        try:
            tag_list = SEO_Tag_Extractor(url)
        except:
            pass
        print(tag_list)

        if len(tag_list)!=0:
            tags_df = tags_df.append({'tags':tag_list}, ignore_index=True)
        else:
            tags_df = tags_df.append({'tags': np.NaN}, ignore_index=True)


    tags_df.to_csv('tags.csv', index=False, header=True)
