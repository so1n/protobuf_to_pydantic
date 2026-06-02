# buf-plugin
`buf-plugin` makes it quick and easy to use the `protobuf-to-pydantic` protoc-plugin in buf.

`protobuf-to-pydantic` currently provides two buf-plugins. The main difference between them is the different versions of `pydantic` they depend on.

- If using the '1.x.x' version of `pydantic`, then need to use `buf-plugin-protobuf-to-pydantic-v1`
- If using the '2.x.x' version of `pydantic`, then need to use `buf-plugin-protobuf-to-pydantic-v2`

## 1.Usage
> Note: Before you begin, please make sure you have read[Try the Buf CLI](https://buf.build/docs/tutorials/getting-started-with-buf-cli)

### 1.1.Initialize project
The usage of `buf-plugin` is the same as `protoc`. Suppose there is a project now and its project structure is as follows:
```bash
├── my-proto-demo
│   └── demo.proto
├── plugin_config.py
└── pyproject.toml
```
Among them, the content of `plugin config.py` is as follows:
```Python
import logging

logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.INFO)


def default_func() -> int:
    return 1

local_dict = {
    "default_func": default_func,
}
```
`plugin config.py` provides a function called `default func`, which will be called in the generated `Pydantic` model.
The content of another file `my-proto-demo/demo.proto` is as follows:
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
It shows the use of `validate` and `p2p_validate`. Since the current system lacks `p2p_validate.proto` and `validate.proto` files, the editor will prompt that the files are missing and mark the error.

### 1.2.Add buf dependency
Enter the `my-proto-demo` directory and execute the following command:
```bash
buf mod init
```
This command will create a `buf.yaml` file in the current directory with the following contents:
```yaml
version: v1
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
```
Next, add the Protobuf file dependency of `protobuf-to-pydantic` in the `buf.yaml` file.
The final content is as follows:
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
Then execute the following command in the current directory:
```bash
buf mod update
```
This command will add the dependencies from the `buf.yaml` file to the `buf.lock` file and download the corresponding Protobuf file.

> Note: After the IDE and other code editors download the corresponding buf plugin, the IDE can find the Protobuf file and the error message will disappear.
### 1.3.Generate Pydantic code
Now return to the root directory of the project and create the `buf.gen.yaml` file. The corresponding contents of the file are as follows:
```yaml
version: v1
plugins:
  - plugin: protobuf-to-pydantic
    opt:
      - config_path=plugin_config.py
      - config_worker_dir_path=/
    out: proto_out
```
This configuration file will tell `buf cli` that the `protobuf-to-pydantic` plug-in is currently used
and specify that the configuration file referenced by the plug-in is `plugin_config.py`;
the directory of the configuration file is the current directory and output file is `proto_out `.

Now everything is ready. After installing the corresponding `Python` version and `protobuf-to-pydantic`,
can use the plugin to generate the `Pydantic` model code.
According to different environment configurations, the way to generate `Pydantic` code is different. different.

- 1.When using `poetry` to manage projects, can generate `Pydantic` code through the following command:
    ```bash
    poetry run buf generate my-proto-demo
    ```
- 2.If using the `Python` virtual environment, can generate `Pydantic` code through the following command:
    ```bash
    source .venv/bin/activate
    buf generate my-proto-demo
    ```
- 3.Specify the path of the plugin in the `buf.yaml` file, and then execute the `buf generate my-proto-demo` command to execute the plugin to generate `Pydantic` code.
For example, if the current `Python` virtual environment is `.venv`, then can add the path of the plugin to the `buf.yaml` file, as shown below:
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

Regardless of which method is used to generate `Pydantic` code, the final project structure will become as follows:
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
### 1.4.Generating Pydantic Code with Remote Plugins
> Note: Since the BUF plugin created by the developer cannot be used publicly, the remote plug-in cannot be used normally(See: [issue](https://github.com/bufbuild/plugins/issues/589#issuecomment-1799085322))。If necessary, please refer to the custom plugins in the next section to create your own plugins。

In addition to executing local plugin to generate `Pydantic` code, can also use remote plugin.

First, need to change the `buf.gen.yaml` file to the following content:
```yaml
version: v1
plugins:
  - plugin: buf.build/python-pai/protobuf-to-pydantic:v0.2.1
    out: proto_out_by_remote_plugin
    opt:
      - plugin_config_py_code_base64=aW1wb3J0IGxvZ2dpbmcKCmxvZ2dpbmcuYmFzaWNDb25maWcoZm9ybWF0PSJbJShhc2N0aW1lKXMgJShsZXZlbG5hbWUpc10gJShtZXNzYWdlKXMiLCBkYXRlZm10PSIleS0lbS0lZCAlSDolTTolUyIsIGxldmVsPWxvZ2dpbmcuSU5GTykKCgpkZWYgZGVmYXVsdF9mdW5jKCkgLT4gaW50OgogICAgcmV0dXJuIDEKCmxvY2FsX2RpY3QgPSB7CiAgICAiZGVmYXVsdF9mdW5jIjogZGVmYXVsdF9mdW5jLAp9Cg
      - plugin_config_module_name=plugin_config
```
Among them, `plugin` fills in the remote plugin name of `protobuf-to-pydantic`, and two new parameters appear in `opt`, their functions are as follows:

  - plugin_config_py_code_base64: Base64 encoding of the contents of the `plugin config.py` file.
    Since the `buf-cli` remote plugin cannot read local files, it is necessary to convert the content of `plugin config.py` into base64 encoding and pass it to the plugin through this parameter.
    > Note:
    >  - 1:If the `localdict` and `BaseModel` parameters are used, the local file(`plugin_config.py` ) cannot be deleted.
    >  - 2:The `=` at the end of the generated base64 encoding text must be removed, otherwise the plugin will fail to load.

  - plugin_config_module_name: Specifies the module name of the dynamically generated plugin configuration file.

    > Note: If the file name is `plugin_config.py`, then the module name is `plugin_confg`. If the file name is `example/plugin_config.py`, then the module name is `example.plugin_config`.

## Custom Plugins
> Note: Make sure you have read it before you read [buf custom plugins dev doc](https://buf.build/docs/bsr/remote-plugins/custom-plugins)

The standard `buf-plugin` of `protobuf-to-pydantic` can satisfy most functions. If you have custom needs, you should create your own custom plugin.


- 1.Create a directory to store plugin related files. At the same time, create `requirements.txt`, `pyproject.toml`, `plugin_+config.py` and other files according to your own needs. For specific contents, please refer to the standard `buf-plugin` directory of `pydantic-to-pydantic`.
- 2.Go into the directory, create a file called `Dockerfile` and fill in the following content:
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

- 3.According to your needs, create the `plugin_config.py` file and the `pyproject.toml` file in the current directory and fill in the corresponding contents.
- 4.After preparing the Dockerfile, build the image through `docker build` and label it:
    ```bash
    docker build --platform linux/amd64 -t buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} .
    ```
    In order to verify whether the image is built successfully, you can run the container through the `docker run` command, as follows:
    ```bash
    docker run buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} --info
    ```
    If the build is successful, you will see the following output:
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
    In addition, you can also view the contents of the plugin's pyproject.toml file through the `--toml-info` option, as follows:
    ```bash
    docker run buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version} --info
    ```
    After executing the command, you can see the following output:
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

- 5.Prepare the `buf.plugin.yaml` file and fill in the following content:
    ```yaml
    version: v1
    name: buf.build/{you org name}/protobuf-to-pydantic-pydantic
    plugin_version: {protobuf-to-pydantic version}
    ```
- 6.Push the plugin to BSR through the following command：
    ```bash
    buf beta registry plugin push \
        --visibility private \
        --image buf.example.com/{you org name}/protobuf-to-pydantic:{protobuf-to-pydantic version}
    ```
    After successful push, you can see the following information:
    ```bash
    Owner           Name                  Version                          Revision
    {you org name}  protobuf-to-pydantic  {protobuf-to-pydantic version}   1
    ```
- 7.At this point, the development work of the plugin has been completed. You can use the customized plugin in your own project. The usage method is as follows:
    ```yaml
    version: v1
    plugins:
      - plugin: buf.build/{you org name}/{protobuf-to-pydantic version}
        out: xxx
        opt:
          - config_path=/plugin_config.py
          - config_worker_dir_path=/
    ```
    Among them, `config_path` is the configuration file path of the plugin, and `config_worker_dir_path` is the working directory path for loading the configuration file.
    Through configuration, `protobuf-to-pydantic` will load the `plugin_config.py` file in the image at runtime, and then execute the plug-in.
