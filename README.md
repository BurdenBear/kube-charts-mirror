# kube-charts-mirror
kubernetes helm 自制国内镜像，每三天更新一次（直到梯子到期没钱续费）

## 最新更新: 
微软也提供了helm 仓库的镜像, 找到这儿的朋友推荐使用微软的镜像：
- stable: http://mirror.azure.cn/kubernetes/charts/
- incubator:	http://mirror.azure.cn/kubernetes/charts-incubator/

感谢 [pureboys](https://github.com/BurdenBear/kube-charts-mirror/issues/3#issuecomment-459614569) 和 [lizebang](https://github.com/BurdenBear/kube-charts-mirror/issues/6#issue-412805159) 两位朋友的分享

-------------------------------------------------------------------------------
## problem to solve
helm官方charts仓库 https://kubernetes-charts.storage.googleapis.com/ 需要翻墙访问，
阿里云提供了一个镜像仓库：https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts 然而从11月开始好像就没有更新过，
而helm的项目迭代得非常快，阿里镜像里连rabbitmq-ha都还没有。
自己尝试用SSR+proxifier代理翻墙,出现证书相关错误，浏览器提示网站开启了HSTS，不知如何解决。
charts仓库组织方式其实很简单，只有一个索引文件和对应压缩包，可以直接从官方源爬过来放到自己服务器下。
这里使用了官方推荐的使用gitPage搭建charts仓库的方式。

## 使用方式：
```
$ helm repo add stable https://burdenbear.github.io/kube-charts-mirror/
```

或者参照以下步骤搭建您自己的仓库：

1.fork 该项目

2.clone代码到一台能访问国外地址的服务器
```
$ git clone https://github.com/${YourUsername}/kube-charts-mirror.git
```

3.启动更新容器(将GIT_REPO，GIT_USER_NAME，GIT_USER_EMAIL替换成您自己的)
```
docker build -t kube-charts-updater .
docker run \
-e GIT_REPO=https://BurdenBear:XXX@github.com/BurdenBear/kube-charts-mirror.git \ 
-e GIT_USER_NAME=BurdenBear \ 
-e GIT_USER_EMAIL=burdenbear@fxdayu.com  \ 
-v /data/charts:/mnt/charts -d kube-charts-updater
```

以上docker镜像完成从原仓库爬取charts上传到对应github项目中的工作，
也可以单独使用(比如爬取其他仓库)，环境变量参数为：
```
CHARTS_URL: 爬取的源仓库
GIT_REPO: 提交的项目地址
GIT_USER_NAME: git config 中的user.name
GIT_USER_EMAIL: git config 中的user.email
UPDATE_INTERVAL: 更新间隔，秒为单位，默认86400(3天)
```

4.在fork后的项目settings里设置开启gitPage，定位到master分支的docs

联系邮箱：
burdenbear@fxdayu.com
