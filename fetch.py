#!/usr/bin/env python
# encoding: utf-8

import yaml
import requests
from contextlib import closing
import os
from urllib.parse import urlparse

# 转自https://www.zhihu.com/question/41132103/answer/93438156 
def wget(url, file_name):
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        progress = ProgressBar(file_name, total=content_size,
                               unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(file_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def main():
    root = "/mnt/charts/docs"
    chart_url = os.environ.get(
        "CHARTS_URL", "https://kubernetes-charts.storage.googleapis.com/")
    repo_url = os.environ.get("GIT_REPO")
    if repo_url is None:
        raise RuntimeError("You must specify a git repo!")
    p = urlparse(repo_url)
    git_user = p.path.split("/")[-2]
    repo_name = p.path.split("/")[-1].split(".")[0]
    default_mirror = "https://%s.github.io/%s/" % (git_user.lower(), repo_name)
    mirror_url = os.environ.get("MIRROR_URL", default_mirror)
    index_file = "index.yaml"
    wget(chart_url + index_file, index_file)
    with open(index_file) as f:
        index = yaml.load(f)
    entries = index["entries"]
    new = index.copy()
    for name, charts in entries.items():
        for chart, new_chart in zip(charts, new["entries"][name]):
            url = chart["urls"][0]
            tar_name = url.split("/")[-1]
            target = os.path.join(root, tar_name)
            new_chart["urls"][0] = "/".join(
                [mirror_url[:-1] if mirror_url.endswith("/") else mirror_url, tar_name])
            # datetime format issure
            new_chart["created"] = new_chart["created"].strftime('%Y-%m-%dT%H:%M:%S.%f000Z')
            if os.path.exists(target):
                continue
            wget(url, target)
    new["generated"] = new["generated"].strftime('%Y-%m-%dT%H:%M:%S.%f000Z')
    with open(os.path.join(root, "index.yaml"), "w") as f:
        yaml.dump(new, stream=f)


if __name__ == "__main__":
    main()

