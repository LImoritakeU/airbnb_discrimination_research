from pathlib import Path

from airbnb.tasks import crawl_twitter, dates_list
from conf import result_path
from twitter_xpath import *

path = result_path


def custom_strftime(dt):
    return f'{dt.year}/{dt.month}/{dt.day}'


def main():
    Path(path).mkdir(exist_ok=True)

    ls = []
    for since, until in dates_list():
        form_data = {
            ands_xpath: "airbnb discrimination",
            since_xpath: custom_strftime(since),
            until_xpath: custom_strftime(until)
        }
        result = crawl_twitter.apply_async((form_data,), task_id=since.strftime('%Y%m%d'))
        ls.append(result)

    while (not all([r.successful() for r in ls])) and (len(ls) > 0):
        for r in ls:
            if r.successful():
                n_path = f'{path}/{r.id}'
                with open(n_path, 'w') as f:
                    f.write(r.result) if isinstance(r.result, str) else None
                ls.remove(r)




if __name__ == "__main__":
    main()
