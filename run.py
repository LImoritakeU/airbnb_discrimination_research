from celery import group
from pathlib import Path

from airbnb.tasks import crawl_twitter, dates_list
from twitter_xpath import *

def main():
    path = Path("/home/shihhao/results").mkdir()
    date_format = "%Y/%m/%d"

    for since, until in dates_list():
        # print(since.strftime(date_format), until.strftime(date_format))
        form_data = {
            ands_xpath: "airbnb discrimination",
            since_xpath: since.strftime(date_format),
            until_xpath: until.strftime(date_format),
        }

        task = crawl_twitter.apply_async((form_data,),
                                         task_id=since.strftime(date_format))

        with open(f"{path}/{since.strftime(date_format)}", 'w') as f:
            f.write(task.get())



if __name__ == "__main__":
    main()