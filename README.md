# fledgling

管理nest中的任务、计划等数据的客户端程序。

# 特性

`fledgling`提供了与`nest`中大部分的 HTTP 接口对应的命令行子命令，列举如下：

| 功能|fledgling 子命令 | nest 的接口 |
|-|-|-|
|创建任务|create-task|POST /task|
|删除任务|delete-task|DELETE /task/<id_>|
|列出任务|list-task|GET /task|
|创建计划|create-plan|POST /plan|
|删除计划|delete-plan|DELETE /plan/<id_>|
|列出计划|list-plan|GET /plan|
|处理计划|event-loop| POST /plan/pop |

# 安装

```shell
pip install fledgling
```

安装成功后，用以下命令创建一个配置文件

```shell
fledgling create-config
```

`fledgling`会在目录`${HOME}/.config/fledgling/`下新建文件`config.ini`，其中需要填充的内容如下

```ini
[account]
email = 在 nest 中注册的帐号的邮箱
password = 在 nest 中注册的账号的密码

[enigma_machine]
password = 用于本地加密/解密任务简述的密码

[location]
name = 当前设备所处的地点的名称

[nest]
cookies_path = 用于存储 Cookie 文件的本地路径
hostname = nest 服务的域名
port = nest 服务的端口号
protocol = nest 服务的协议名称
```

如果你不想或不方便搭建自己的`nest`服务，可以使用我所提供的`nest`服务，其主机、端口，以及协议如下

```ini
hostname = nest.daquan.tech
port = 443
protocol = https
```

# 用法

## 帮助文档

可以用命令`fledgling --help`查看 fledgling 提供的所有子命令

```shell
bash-3.2$ fledgling --help
Usage: fledgling [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  change-plan    修改指定计划。
  create-config  创建一份空的配置文件。
  create-plan    为任务创建一个计划。
  create-task    创建一个任务。
  delete-plan    删除指定计划。
  delete-task    删除指定任务及其计划。
  event-loop     启动事件循环拉取计划并弹出提醒。
  list-plan      列出接下来的计划。
  list-task      列出任务。
```

子命令本身也可以接受`--help`参数来打印它的使用说明

```shell
bash-3.2$ fledgling change-plan --help
Usage: fledgling change-plan [OPTIONS]

  修改指定计划。

Options:
  --duration INTEGER
  --location-id INTEGER
  --plan-id INTEGER          [required]
  --repeat-interval INTEGER
  --repeat-type TEXT
  --trigger-time TEXT
  --visible-hours TEXT
  --visible-wdays TEXT
  --help                     Show this message and exit.
```

## 注册帐号

使用`register`命令注册账号

```shell
➜  fledgling fledgling register --help
Usage: fledgling register [OPTIONS]

  注册一个新用户。

Options:
  --email TEXT     登录用的邮箱  [required]
  --nickname TEXT  昵称  [required]
  --password TEXT  登录所需的密码  [required]
  --help           Show this message and exit.
```

如果你的`fledgling`连接的是我所提供的`nest`服务（配置见前文所述），那么将会有一封来自`nest_service@sina.com`的、含有激活码的邮件发送到你注册所用的邮箱中。之后使用`fledgling`的`activate-user`命令激活帐号即可。

## 示例

### 创建一个任务，并设定它的提醒时间

```shell
fledgling create-task --brief '测试用的任务'
fledgling create-plan --task-id 69 --trigger-time '2021-08-15 17:40:00'  # 传给选项--task-id的数字69是上一道命令创建的任务的ID
```

### 设定一个每小时提醒一次的任务

```shell
fledgling create-task --brief '喝水'
fledgling create-plan --task-id 3 --trigger-time '2021-08-15 18:20:00' --repeat-type 'hourly'
```

# FAQ

## 如何从源码安装？

在 fledgling 仓库的根目录中运行下列命令

```shell
python setup.py sdist
```

这会在子目录 ./dist 中生成一个文件 fledgling-0.0.1.tar.gz。接着使用 pip 安装即可

```shell
pip install ./dist/fledgling-0.0.1.tar.gz
```

## 如何使用修改中的代码？

以使用仓库目录下的代码来创建任务为例

```shell
PYTHONPATH="${PYTHONPATH}:`pwd`" python fledgling/cli/main.py create-task --help
```
