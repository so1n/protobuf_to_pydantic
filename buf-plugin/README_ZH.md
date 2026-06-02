# buf-plugin
通过`buf-plugin`，可以快速轻松地在buf中使用`protobuf-to-pydantic`的protoc-plugin。

`protobuf-to-pydantic`目前提供两种buf-plugin，它们的区别在于依赖的`pydantic`版本不同。

- 如果使用的是`pydantic`的'1.x.x'版本，那么需要使用`buf-plugin-protobuf-to-pydantic-v1`，
- 如果使用的是`pydantic`的'2.x.x'版本，那么需要使用`buf-plugin-protobuf-to-pydantic-v2`。

## 1.Usage
> Note: 在开始之前，请确保你已经阅读了 [Try the Buf CLI](https://buf.build/docs/tutorials/getting-started-with-buf-cli)

### 1.1.初始化项目
`buf-plugin`的使用方法与`protoc`相同，假设现在有一个项目，它的项目结构如下:
```bash
├── my-proto-demo
│   └── demo.proto
├── plugin_config.py
└── pyproject.toml
```
其中，`plugin_config.py`的内容如下:
```Python
import logging

logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.INFO)


def default_func() -> int:
    return 1

local_dict = {
    "default_func": default_func,
}
```
`plugin_config.py`提供了一个名为`default_func`的函数，它会在生成的`Pydantic`模型中被调用。

而另外一个文件`my-proto-demo/demo.proto`的内容如下:
```protobuf
syntax = "proto3";

package demo;

import "p2p_validate.proto";
import "validate.proto";

message P2PValidateDemo{
  int32 a = 1[
    (p2p_validate.rules).int32.default_factory="p2p@local|default_func"
  ];
}

message ValidateDemo{
  string a = 1[
    (validate.rules).string.max_len=3
  ];
}
```
它展示了`validate`和`p2p_validate`的使用，由于当前系统缺少了`p2p_validate.proto`和`validate.proto`文件，所以编辑器会提示缺少文件并标记错误。

### 1.2.添加buf依赖
进入到`my-proto-demo`目录中执行以下命令:
```bash
buf mod init
```
该命令会在当前目录下创建一个`buf.yaml`文件，它的内容如下:
```yaml
version: v1
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
```
接着在`buf.yaml`文件添加`protobuf-to-pydantic`的Protobuf文件依赖，最终的内容如下:
```yaml
version: v1
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
deps:                                         # <<<<<< new
  - buf.build/so1n/protobuf-to-pydantic       # <<<<<< new
```
然后在当前目录下执行以下命令:
```bash
buf mod update
```
该命令会将`buf.yaml`文件中的依赖添加到`buf.lock`文件中，并下载相应的Protobuf文件。

> Note: IDE等代码编辑器下载对应的buf插件后，IDE可以正常寻找到Protobuf文件且错误提示会消失。
### 1.3.生成Pydantic代码
现在退回到项目的根目录，并创建`buf.gen.yaml`文件，文件对应的内容如下:
```yaml
version: v1
plugins:
  - plugin: protobuf-to-pydantic
    opt:
      - config_path=plugin_config.py
      - config_worker_dir_path=/
    out: proto_out
```
该配置文件会告诉`buf cli`当前使用的是`protobuf-to-pydantic`插件并指定插件引用的配置文件为`plugin_config.py`以及配置文件的目录为当前目录，同时告诉`buf cli`输出文件的目录为`proto_out`。

目前一切准备就绪，接下来安装了对应的`Python`版本以及`protobuf-to-pydantic`后就可以使用插件生成`Pydantic`模型了，根据不同的环境配置，生成`Pydantic`代码的方式有所不同。

- 1.在使用`poetry`管理关键项目时，可以通过如下命令生成`Pydantic`代码：
    ```bash
    poetry run buf generate my-proto-demo
    ```
- 2.如果是使用`Python`虚拟环境，那么可以通过如下命令生成`Pydantic`代码:
    ```bash
    source .venv/bin/activate
    buf generate my-proto-demo
    ```
- 3.在`buf.yaml`文件中指定插件的路径，再执行`buf generate my-proto-demo`命令执行插件生成`Pydantic`代码。
比如当前的`Python`虚拟环境为`.venv`，那么可以将插件的路径添加到`buf.yaml`文件中，如下所示:
    ```yaml
    version: v1
    plugins:
      - plugin: protobuf-to-pydantic
        path: .venv/bin/protoc-gen-protobuf-to-pydantic   # <<< new
        opt:
          - config_path=plugin_config.py
          - config_worker_dir_path=/
        out: proto_out
    ```

无论使用那种方式生成`Pydantic`代码，最终项目结构将变为如下:
```bash
├── my-proto-demo
│   ├── buf.lock
│   ├── buf.yaml
│   └── demo.proto
├── buf.gen.yaml
├── __init__.py
├── plugin_config.py
├── proto_out
│   └── demo_p2p.py
└── pyproject.toml
```
### 1.4.使用远程插件生成Pydantic代码
> Note: 由于开发者自己创建的buf插件是无法公开使用的，所以远程插件无法正常使用(具体见：[issue](https://github.com/bufbuild/plugins/issues/589#issuecomment-1799085322))。如有需要，请参考下一节的自定义插件自己创建插件。

除了执行本地插件生成Pydantic代码外，还可以使用远程插件，首先需要更改`buf.gen.yaml`文件为如下内容:
```yaml
version: v1
plugins:
  - plugin: buf.build/python-pai/protobuf-to-pydantic:v0.2.1
    out: proto_out_by_remote_plugin
    opt:
      - plugin_config_py_code_base64=aW1wb3J0IGxvZ2dpbmcKCmxvZ2dpbmcuYmFzaWNDb25maWcoZm9ybWF0PSJbJShhc2N0aW1lKXMgJShsZXZlbG5hbWUpc10gJShtZXNzYWdlKXMiLCBkYXRlZm10PSIleS0lbS0lZCAlSDolTTolUyIsIGxldmVsPWxvZ2dpbmcuSU5GTykKCgpkZWYgZGVmYXVsdF9mdW5jKCkgLT4gaW50OgogICAgcmV0dXJuIDEKCmxvY2FsX2RpY3QgPSB7CiAgICAiZGVmYXVsdF9mdW5jIjogZGVmYXVsdF9mdW5jLAp9Cg
      - plugin_config_module_name=plugin_config
```
其中`plugin`填写的是`protobuf-to-pydantic`的远程插件名，而`opt`中出现了两个新的参数，它们的作用如下:

  - plugin_config_py_code_base64: `plugin_config.py`文件内容的base64编码。
    由于`buf-cli`远程插件无法读取到本地文件，所以需要把`plugin_config.py`内容转化为base64编码后，通过该参数传递给插件。
    > Note:
    >  - 1:如果使用到了`local_dict`和`BaseModel`参数，本地的`plugin_config.py`文件不可以删除。
    >  - 2:生成的base64编码末尾的`=`必须移除，否则会导致插件加载失败。

  - plugin_config_module_name: 指定动态生成的插件配置文件的模块名。

    > Note: 如果文件名为`plugin_config.py`，那么模块名为`plugin_confg`。如果文件名为`example/plugin_config.py`，那么模块名为`example.plugin_config`。




## 2.自定义插件
> Note: 请确保你已经阅读了 [buf custom plugins dev doc](https://buf.build/docs/bsr/remote-plugins/custom-plugins)

`protobuf-to-pydantic`的标准`buf-plugin`可以满足大多数功能。如果您有自定义需求，您应该创建属于自己的自定义插件。

- 1.创建一个目录用于存放插件的相关文件。同时按照自己的需求创建`requirements.txt`，`pyproject.toml`，`plugin_config.py`等文件，具体内容可以参考`pydantic-to-pydantic`的标准`buf-plugin`目录。
- 2.进入目录，创建一个名为`Dockerfile`的文件，并填入以下内容：
    ```dockerfile
    # syntax=docker/dockerfile:1.4
    FROM python:3.11.2-alpine3.17 AS build
    WORKDIR /app
    RUN python -mvenv /app
    ADD /requirements.txt requirements.txt
    RUN source ./bin/activate \
     && pip install --no-cache-dir -r requirements.txt \
     && pip uninstall --yes pip setuptools \
     && rm -f requirements.txt bin/activate.fish bin/activate.csh bin/Activate.ps1

    FROM python:3.11.2-alpine3.17
    COPY --from=build --link /app /app
    WORKDIR /
    ADD /pyproject.toml  /app/bin/pyproject.toml
    ADD /plugin_config.py /app/bin/plugin_config.py
    USER nobody
    ENTRYPOINT [ "/app/bin/protoc-gen-protobuf-to-pydantic" ]
    ```
- 3.根据你的需求，在当前目录下创建`plugin_config.py`文件以及`pyproject.toml`文件并填入对应的内容。
- 4.准备好Dockerfile文件后，通过`docker build`构建镜像并打上标签:
    ```bash
    docker build --platform linux/amd64 -t buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} .
    ```
    为了验证镜像是否构建成功，可以通过`docker run`命令运行容器，如下:
    ```bash
    docker run buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} --info
    ```
    如果构建成功，那么可以看到如下输出:

    ```bash
    current working directory: /
    sys path:
        -/app/bin
        -/usr/local/lib/python311.zip
        -/usr/local/lib/python3.11
        -/usr/local/lib/python3.11/lib-dynload
        -/app/lib/python3.11/site-packages
    executable: /app/bin/python
    python version: sys.version_info(major=3, minor=11, micro=2, releaselevel='final', serial=0)

    ############# dependencies ##############
        grpc:            1.59.2
        pydantic:        2.4.2

    ########## Expand dependencies ##########
        mypy-protobuf:   3.3.0
        toml:            0.10.2

    ########## Format dependencies ##########
        autoflake:       1.4
        black:           23.1.0
        isort:           5.9.3
    ```
    此外，还可以通过`--toml-info`选项查看插件的`pyproject.toml`文件内容，如下:
    ```bash
    docker run buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} --toml-info
    ```
    在执行命令后，可以看到如下输出:
    ```toml
    ######### pyproject.toml Content #########
    [tool.protobuf-to-pydantic.format]
    black = true
    isort = true
    autoflake = true

    [tool.black]
    line-length = 120
    target-version = ['py38', 'py39', 'py310']


    [tool.isort]
    profile = "black"
    multi_line_output = 3
    include_trailing_comma = true
    force_grid_wrap = 0
    use_parentheses = true
    ensure_newline_before_comments = true
    line_length = 120

    [tool.autoflake]
    in-place = true
    remove-all-unused-imports = true
    remove-unused-variables = true
    ```

- 5.准备`buf.plugin.yaml`文件，并填入以下内容：
    ```yaml
    version: v1
    name: buf.build/{you org name}/protobuf-to-pydantic-pydantic
    plugin_version: {protobuf-to-pydantic version}
    ```
- 6.通过如下命令把插件推送到BSR：
    ```bash
    buf beta registry plugin push \
        --visibility private \
        --image buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version}
    ```
    成功推送后，可以看到如下信息:
    ```bash
    Owner           Name                  Version                          Revision
    {you org name}  protobuf-to-pydantic  {protobuf-to-pydantic version}   1
    ```
- 7.至此，插件的开发工作已经完成了，你可以在自己的项目中使用自定义的插件，使用方法如下:
    ```yaml
    version: v1
    plugins:
      - plugin: buf.build/{you org name}/{protobuf-to-pydantic version}
        out: xxx
        opt:
          - config_path=/plugin_config.py
          - config_worker_dir_path=/
    ```
    其中，`config_path`是插件的配置文件路径，`config_worker_dir_path`是加载配置文件的工作目录路径，通过这两个参数配置`protobuf-to-pydantic`在运行时会加载镜像中的`plugin_config.py`文件，再执行插件。
