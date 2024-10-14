# protobuf_to_pydantic
Generate Pydantic Model or source code with parameter verification function based on Protobuf file (Proto3).


[中文文档](https://github.com/so1n/protobuf_to_pydantic/blob/master/README_ZH.md)

# Feature

Feature：
- [x] Generate source code through `Protobuf` plugin。
- [x] Generate `Pydantic Model` or source code by parsing `Protobuf Message` in `Python` runtime.
- [x] Compatible with `V1` and `V2` versions of `Pydantic`。
- [x] Supports multiple verification rules and is compatible with `proto-gen-validate` (subsequent versions will support the rules of `proto-gen-validate` 1.0)。
- [x] Support custom functionality through templates。
- [ ] Supports `protovalidate` verification rules（`proto-gen-validate` version >= 1.0）

The following is a functional overview diagram of `protobuf-to-pydantic`.
In the picture `P2P` represents `protobuf-to-pydantic`, `Protoc` represents the command for `Protobuf` to generate code, and `plugin` represents ` Plugin for Protoc`:
![protobuf-to-pydantic](https://github.com/so1n/protobuf_to_pydantic/blob/master/images/protobuf-to-pydantic_index.png?raw=true)

# Installation
By default, `protobuf-to-pydantic` can be installed directly via the following command:
```bash
pip install protobuf_to_pydantic
```
If want to use the full functionality of `protobuf-to-pydantic`, can install `protobuf-to-pydantic` with the following command:.
```bash
pip install protobuf_to_pydantic[all]
```
# Usage
## 1.code generation
`protobuf-to-pydantic` currently has two methods to generate `Pydantic Model` objects based on Protobuf files.：
- 1: Plugin Mode: Use the `Protoc` plug-in to generate the corresponding `Python` code file through the Protobuf file。
- 2: Runtime Mode: Generate the corresponding `Pydantic Model` object through the `Message` object in `Python` runtime。

### 1.1.Plugin Mode
#### 1.1.0.Install dependencies
The `protobuf-to-pydantic` plug-in depends on `mypy-protobuf`, need to install `mypy-protobuf` through the following command first:
```bash
python -m pip install protobuf-to-pydantic[mypy-protobuf]
```
or
```bash
poetry add protobuf-to-pydantic -E mypy-protobuf
```
#### 1.1.1.Use plugins
Plug-in is the `Pydantic Model` source code generation method recommended by `protobuf-to-pydantic`.
It supports the most complete functions and is also very simple to use.

Assume that it is usually generated through the following command Code corresponding to Protobuf file:
```bash
python -m grpc_tools.protoc -I. example.proto
# or
protoc -I. --python_out=. example.proto
```
After installing `protobuf-to-pydantic`,can use the `protobuf-to-pydantic` plugin with the `--protobuf-to-pydantic_out` option with the following command:
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=. example.proto
# or
protoc -I. --protobuf-to-pydantic_out=. example.proto
```

In this command, `--protobuf-to-pydantic_out=.` means using the `prorobuf-to-pydantic` plug-in,
And it is declared that the output location of the `protobuf-to-pydantic` plug-in is `.`

> `.` indicates the output path used by `grpc_tools.proto`.

After running the command, the `protobuf-to-pydantic` plugin writes the generated source code to a file with the filename suffix `p2p.py`, e.g., `example.proto` generates a file with the name `example_p2p.py`.


#### 1.1.2.Plug-in configuration
The `protobuf-to-pydantic` plugin supports loading configuration by reading a `Python` file。

> In order to ensure that the variables of the configuration file can be introduced normally, the configuration file should be stored in the current path where the command is run.

An example configuration that can be read by 'protobuf_to_pydantic' would look like:

```Python
import logging
from typing import List, Type

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.template import Template

# Configure the log output format and log level of the plugin, which is very useful when debugging
logging.basicConfig(
  format="[%(asctime)s %(levelname)s] %(message)s",
  datefmt="%y-%m-%d %H:%M:%S",
  level=logging.DEBUG
)


class CustomerField(FieldInfo):
  pass


def customer_any() -> Any:
  return Any  # type: ignore


# For the configuration of the local template, see the use of the local template for details
local_dict = {
  "CustomerField": CustomerField,
  "confloat": confloat,
  "conint": conint,
  "customer_any": customer_any,
}
# Specifies the start of key comments
comment_prefix = "p2p"
# Specify the class of the template, can extend the template by inheriting this class, see the chapter on custom templates for details
template: Type[Template] = Template
# Specify the protobuf files of which packages to ignore, and the messages of the ignored packages will not be parsed
ignore_pkg_list: List[str] = ["validate", "p2p_validate"]
# Specifies the generated file name suffix (without .py)
file_name_suffix = "_p2p"
```
Next, in order to be able to read this file, need to change the `--protobuf-to-pydantic_out=. ` to ` --protobuf-to-pydantic_out=config_path=plugin_config.py:. `.
where the left side of `:` indicates that the configuration file path to be read is `plugin_config.py`, and the right side of `:` declares that the output location of the `protobuf-to-pydantic` plugin is `. `
The final complete command is as follows：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
# or
protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
```
Through this command, can load the corresponding configuration and run the `protobuf-to-pydantic` plug-in。

In addition to the configuration options in the example configuration file,
the `protobuf-to-pydantic` plug-in also supports other configuration options.
The specific configuration instructions are as follows：

| Configuration name            | Functional module                      | Type                                            | Hidden meaning                                                                                                                                                   |
|-------------------------------|----------------------------------------|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| local_dict                    | Template                               | dict                                            | Holds variables for the `local` template                                                                                                                         |
| template                 | Template                               | protobuf_to_pydantic.template.Template | Implementation of the template class                                                                                                                             |
| comment_prefix                | Template                               | str                                             | Comment prefix.Only strings with a fixed prefix will be used by the template                                                                                     |
| parse_comment                 | comment(plugin only)                   | bool                                            | If true, the annotation rule is compatible                                                                                                                       |
| customer_import_set           | Code generation                        | `Set[str]`                                      | A collection of custom import statements, such as `from typing import Set`or `import typing`, that will write data in order to the source code file              |
| customer_deque                | Code generation                        | `deque[str]`                                    | Custom source file content, used to add custom content                                                                                                           |
| module_path                   | str                                    | str                                             | Used to define the root path of the project or module, which helps `protobuf-to-pydantic`to better automatically generate module import statements               |
| pyproject_file_path           | Code generation                        | str                                             | Define the pyproject file path, which defaults to the current project path                                                                                       |
| code_indent                   | Code generation                        | int                                             | Defines the number of indentation Spaces in the code; the default is 4                                                                                           |
| ignore_pkg_list               | Code generation(plugin only)           | `list[str]`                                     | Definition ignores parsing of the specified package file                                                                                                         |
| base_model_class              | Model Code generation, Code generation | `Type[BaseModel]`                               | Define the parent class of the generated Model                                                                                                                   |
| file_name_suffix              | Code generation                        | str                                             | Define the generated file suffix, default `_p2p.py`                                                                                                              |
| file_descriptor_proto_to_code | Code generation(plugin only)           | `Type[FileDescriptorProtoToCode]`               | Define the `FileDescriptorProtoToCode` to use                                                                                                                    |
| protobuf_type_config          | Code generation(plugin only) | `Dict[str, ProtobufTypeConfigModel]`            | Compatible with non-standard ones Message, See[ConfigModel note](https://github.com/so1n/protobuf_to_pydantic/blob/master/protobuf_to_pydantic/plugin/config.py) |
| pkg_config                    |Code generation(plugin only)| `Dict[str, "ConfigModel"]`                        | Adapt the corresponding configuration for each PKG                                                                                                               |

> Note:
>   - 1:For more information, see the configuration instructions[/protobuf_to_pydantic/plugin/config.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/protobuf_to_pydantic/plugin/config.py)
>   - 2:See for directions of use[/example/plugin_config.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/plugin_config.py)
#### 1.1.3.buf-cli
If you are using `buf-cli` to manage Protobuf files,
then you can also use `protobuf-to-pydantic` in `buf-cli`, See [How to use `protobuf-to-pydantic` in `buf-cli`](https://github.com/so1n/protobuf_to_pydantic/blob/master/buf-plugin/README.md)

### 1.2.Runtime Mode
`protobuf_to_pydantic` can generate the corresponding `PydanticModel` object based on the `Message` object at runtime。

For example, the `UserMessage` in the following Protobuf file named `demo.proto`:
```protobuf
// path: ./demo.proto
syntax = "proto3";
package user;

enum SexType {
  man = 0;
  women = 1;
}

message UserMessage {
  string uid=1;
  int32 age=2;
  float height=3;
  SexType sex=4;
  bool is_adult=5;
  string user_name=6;
}
```
`protoc` can be used to generate the Python code file corresponding to the `Protobuf` file (the file name is `demo_pb2.py`), and the code related to the `UserMessage` is stored in the code file.

At `Python` runtime, The func `msg_to_pydantic_model` can be called to read the `UserMessage` object from the `demo_pb2` module and generate the corresponding `Pydantic Model` object as follows:
```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from . import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(demo_pb2.UserMessage)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)

# output
# {
#   `uid`: FieldInfo(default=``, extra={}),
#   `age`: FieldInfo(default=0, extra={}),
#   `height`: FieldInfo(default=0.0, extra={}),
#   `sex`: FieldInfo(default=0, extra={}),
#   `is_adult`: FieldInfo(default=False, extra={}),
#   `user_name`: FieldInfo(default=``, extra={})
#  }
```
Through the output results, it can be found that the generated `pydantic.BaseModel` object also contains `uid`, `age`, `height`, `sex`, `is adult` and `user name` fields,
and the `default` property matches the zero value of the Protobuf type。

The `msg_to_pydantic_model` func is customizable just like plugins, with the following extension parameters:

| Fields                                    | Meaning                                                   |
|-------------------------------------------|-----------------------------------------------------------|
| default_field                             | Generate a `Field` for each field in the `Pydantic Model` |
| comment_prefix                            | The prefix of a comment that can be parsed                |
| parse_msg_desc_method                     | Parsing rules to use                                      |
| local_dict                                | Variables used by the `local` template                    |
| pydantic_base                             | Generates the parent class of the `Pydantic Model` object |
| pydantic_module                           | Generate the `Module` of the `Pydantic Model` object      |
| template                             | Template class to use                                     |
| message_type_dict_by_type_name            | Protobuf type mapping to `Python` type                    |
| message_default_factory_dict_by_type_name | Protobuf type mapping to the Python type factory          |

Among them, `parse_msg_desc_method` defines the rule information where `protobuf_to_pydantic` obtains the Message object.

### 1.2.1.parse_msg_desc_method
By default, the value of `parse_msg_desc_method` is empty. In this case, `protobuf_to_pydantic` obtains the parameter validation rules through the Option of the Message object.

If the parameter validation rules are declared through comments, then `protobuf_to_pydantic` can only obtain the parameter validation rules through the other.

- 1:The value of `parse_msg_desc_method` is the `Python` module corresponding to `Message`

  In this case, `protobuf-to-pydantic` can obtain additional information about each field in the Message object through the comments in the `.pyi` file corresponding to the `Python` module during the running process.
  For example, in the above sample code, the `Python` module corresponding to `demo_pb2.UserMessage` is `demo_pb2`.

  > Note: This feature requires the use of the [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf) plug-in when generating the corresponding `Python` code from the Protobuf file, and the specified pyi file output path must be the same as the generated `Python` code path to take effect.
  > Before execution, please install `protobuf-to-pydantic` using the `python -m pip install protobuf-to-pydantic[mypy-protobuf]` command

- 2:The value of `parse_msg_desc_method` is the path to the Protobuf file

  In addition to obtaining comments through `.pyi` files, `protobuf-to-pydantic` also supports obtaining information about each field through comments in the Protobuf file to which the Message object belongs.
  Using this feat is very simple. Just set the value of `parse_msg_desc_method` to the root directory path specified when the Message object is generated.

  > When using this method, make sure to install `protobuf-to-pydantic` via `python -m pip install protobuf-to-pydantic[lark]` and that the Protobuf files are present in your project.

  For example, the project structure of the `protobuf-to-pydantic` sample code is as follows:
  ```bash
  ./protobuf_to_pydantic/
  ├── example/
  │ ├── python_example_proto_code/
  │ └── example_proto/
  ├── protobuf_to_pydantic/
  └── /
  ```
  The Protobuf file is stored in the `example/example_proto` folder, and then run the following command in the `example` directory to generate the `Python` code file corresponding to Protobuf:
  ```bash
  cd example

  python -m grpc_tools.protoc
    --python_out=./python_example_proto_code \
    --grpc_python_out=./python_example_proto_code \
    -I. \
  # or
  protoc
    --python_out=./python_example_proto_code \
    --grpc_python_out=./python_example_proto_code \
    -I. \
  ```
  Then the path that needs to be filled in for `parse_msg_desc_method` is `./protobuf_to_pydantic/example`.
  For example, the following sample code:
  ```python
  # pydantic Version v1
  from typing import Type
  from protobuf_to_pydantic import msg_to_pydantic_model
  from pydantic import BaseModel

  # import protobuf gen python obj
  from example.proto_3_20_pydanticv1.example.example_proto.demo import demo_pb2

  UserModel: Type[BaseModel] = msg_to_pydantic_model(
      demo_pb2.UserMessage, parse_msg_desc_method="./protobuf_to_pydantic/example"
  )
  print(
      {
          k: v.field_info
          for k, v in UserModel.__fields__.items()
      }
  )
  # output
  # {
  #   'uid': FieldInfo(default=PydanticUndefined, title='UID', description='user union id', extra={'example': '10086'}),
  #   'age': FieldInfo(default=0, title='use age', ge=0, extra={'example': 18}),
  #   'height': FieldInfo(default=0.0, ge=0, le=2, extra={}),
  #   'sex': FieldInfo(default=0, extra={}),
  #   'is_adult': FieldInfo(default=False, extra={}),
  #   'user_name': FieldInfo(default='', description='user name', min_length=1, max_length=10, extra={'example': 'so1n'})
  # }
  ```
  As you can see, the only difference in this code is the value of `parse_msg_desc_method`, but the output is the same.

### 1.3.Generate files

In addition to generating the corresponding `Pydantic Model` object at runtime,
`protobuf-to-pydantic` also supports converting `Pydantic Model` objects to Python code text at runtime (only compatible with `Pydantic Model` objects generated by `protobuf-to-pydantic`).
The `pydantic_model_to_py_code` func is used to generate the source code, and the `pydantic_model_to_py_file` func is used to generate the code file. The example code of the `pydantic_model_to_py_file` func is as follows:

```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
When the code runs, it converts`demo_pb2.NestedMessage`to a Pydantic Model object and passes it to the  `pydantic_model_to_py_file`. `pydantic_model_to_py_file` generates the source code and writes it to a `demo_gen_code.py` file.


## 2.Parameter validation
In the previous section, the `Pydantic Model` object generated by the Protobuf file is very simple because the Protobuf file does not have enough parameters to verify the relevant information.
In order for each field in the generated `Pydantic Model` object to have parameter validation capabilities, the corresponding parameter checking rules for the field need to be refined in the Protobuf file.

Currently, `protobuf-to-pydantic` supports three validation rules：
- 1.Text annotations
- 2.PGV(protoc-geb-validate)
- 3.P2P

With these rules, the `Pydantic Model` object generated by `protobuf-to-pydantic` will have parameter validation feature.
Among them, text annotations and P2P rules are consistent, they both support most of the parameters in `Pydantic Field`, some of the variations and new parameters are seen
[2.4.`P2P` and text annotation rule other parameter support](#24p2p-and-text-comment-rule-other-parameter-support)

> NOTE:
>  - 1.Text annotation rules are not the focus of subsequent functional iterative development, and it is recommended to use P2P verification rules.
>  - 2.In plugin mode, annotation rules are written slightly differently, See[demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate_by_comment/demo.proto)
>  - 3.The plugin mode automatically selects the most suitable parameter verification rule.


### 2.1.Text annotations
In the Protobuf file, can write annotations for each field that meet the requirements of `protobuf-to-pydantic`,
so that `protobuf-to-pydantic` can obtain the validation information of the parameters when parsing the Protobuf file, such as the following example
```protobuf
syntax = "proto3";
package user;

enum SexType {
  man = 0;
  women = 1;
}

// user info
message UserMessage {
  // p2p: {"required": true, "example": "10086"}
  // p2p: {"title": "UID"}
  string uid=1; // p2p: {"description": "user union id"}
  // p2p: {"example": 18, "title": "use age", "ge": 0}
  int32 age=2;
  // p2p: {"ge": 0, "le": 2.5}
  float height=3;
  SexType sex=4;
  bool is_adult=5;
  // p2p: {"description": "user name"}
  // p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
  string user_name=6;
}
```

In this example, each annotation that can be used by `protobuf_to_pydantic` starts with `p2p:` (supports customization) and is followed by a complete Json string. If are familiar with the usage of `pydantic`, can find This Json string contains the verification information corresponding to `pydantic.Field`. For example, the `uid` field in `UserMessage` contains a total of 4 pieces of information as follows：

| Column      | Meaning                                                                               |
|-------------|---------------------------------------------------------------------------------------|
| required    | Indicates that the generated field does not have a default value                      |
| example     | An example value representing the generated field is 10086                            |
| title       | Indicates that the schema name of the field is UID                                    |
 | description | The schema documentation for the representation field is described as `user_union_id` |

> Note:
>   - 1.Currently only single-line comments are supported and comments must be a complete Json data (no line breaks).

When these annotations are written, `protobuf_to_pydantic` will bring the corresponding information for each field when converting the Message into the corresponding `Pydantic.BaseModel` object, as follows:

```python
# pydantic version V1
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(demo_pb2.UserMessage, parse_msg_desc_method=demo_pb2)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)
# output
# {
#   `uid`: FieldInfo(default=PydanticUndefined, title=`UID`, description=`user union id`, extra={`example`: `10086`}),
#   `age`: FieldInfo(default=0, title=`use age`, ge=0, extra={`example`: 18}),
#   `height`: FieldInfo(default=0.0, ge=0, le=2, extra={}),
#   `sex`: FieldInfo(default=0, extra={}),
#   `is_adult`: FieldInfo(default=False, extra={}),
#   `user_name`: FieldInfo(default=``, description=`user name`, min_length=1, max_length=10, extra={`example`: `so1n`})
# }
```
It can be seen that the output fields carry the corresponding information, which is consistent with the comments of the Protobuf file.

### 2.2.PGV(protoc-gen-validate)
At present, the commonly used parameter verification project in the Protobuf ecosystem is [protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)，
It has become a common standard in Protobuf because it supports multiple languages and requires only one writing of `PGV` rules to make the generated `Message` object support the corresponding validation rules.

> Currently `protobuf-to-pydantic` only supports rules that [protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate) is less than version 1.0.0

`protobuf-to-pydantic` supports parsing of `PGV` validation rules and generates `Pydantic Model` objects with validation logic functions.
Using `PGV` checksum rules in `protobuf-to-pydantic` is very simple, just write the corresponding `PGV` rules in the Protobuf file first,
and then specify the value of `parse_msg_desc_method` to be `PGV` when calling `msg_to_pydantic_model` as the code below:
```Python
# pydantic version V1
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.proto_3_20_pydanticv1.example.example_proto.validate import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(
    demo_pb2.FloatTest, parse_msg_desc_method="PGV"
)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)
# output
# {
#   `const_test`: FieldInfo(default=1.0, const=True, extra={}),
#   `range_e_test`: FieldInfo(default=0.0, ge=1, le=10, extra={}),
#   `range_test`: FieldInfo(default=0.0, gt=1, lt=10, extra={}),
#   `in_test`: FieldInfo(default=0.0, extra={`in`: [1.0, 2.0, 3.0]}),
#   `not_in_test`: FieldInfo(default=0.0, extra={`not_in`: [1.0, 2.0, 3.0]}),
#   `ignore_test`: FieldInfo(default=0.0, extra={})
# }
```

> Note:
>  - 1.For the usage of `PGV`, see: [protoc-gen-validate doc](https://github.com/bufbuild/protoc-gen-validate/blob/v0.10.2-SNAPSHOT.17/README.md)
>  - 2.There are three ways to introduce validate
>    - 2.1.Install `PGV` through  `pip install protoc_gen_validate`
>    - 2.2.Download [validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto)to the protobuf directory in the project。
>    - 2.3.Install `PGV `through [buf-cli](https://github.com/so1n/protobuf_to_pydantic/blob/master/buf-plugin/README_ZH.md)


### 2.3.P2P
The `PGV` verification rules are written in the Option attribute of each field of `Message` and have a better code specification,
so Protobuf that use `PGV` checksum rules will be more readable than Protobuf that use annotation .

At the same time, when writing `PGV` rules, can also experience the convenience of the IDE's auto-completion and the security of checksumming when generating the corresponding language objects from Protobuf files, but it only supports checksumming-related logic, which is not as rich as the file annotation mode.


The `P2P` verification rule that comes with `protobuf-to-pydantic` expands on the `PGV` verification rule by incorporating some of the functionality of the text annotation verification rule, which satisfies most of the customization of the properties of each `Field` in the `Pydantic Model`, such as the following Protobuf file.
```protobuf
syntax = "proto3";
package p2p_validate_test;

import "example_proto/common/p2p_validate.proto";


message FloatTest {
  float const_test = 1 [(p2p_validate.rules).float.const = 1];
  float range_e_test = 2 [(p2p_validate.rules).float = {ge: 1, le: 10}];
  float range_test = 3[(p2p_validate.rules).float = {gt: 1, lt: 10}];
  float in_test = 4[(p2p_validate.rules).float = {in: [1,2,3]}];
  float not_in_test = 5[(p2p_validate.rules).float = {not_in: [1,2,3]}];
  float default_test = 6[(p2p_validate.rules).float.default = 1.0];
  float not_enable_test = 7[(p2p_validate.rules).float.enable = false];
  float default_factory_test = 8[(p2p_validate.rules).float.default_factory = "p2p@builtin|float"];
  float miss_default_test = 9[(p2p_validate.rules).float.miss_default = true];
  float alias_test = 10 [(p2p_validate.rules).float.alias = "alias"];
  float desc_test = 11 [(p2p_validate.rules).float.description = "test desc"];
  float multiple_of_test = 12 [(p2p_validate.rules).float.multiple_of = 3.0];
  float example_test = 13 [(p2p_validate.rules).float.example = 1.0];
  float example_factory = 14 [(p2p_validate.rules).float.example_factory = "p2p@builtin|float"];
  float field_test = 15[(p2p_validate.rules).float.field = "p2p@local|CustomerField"];
  float type_test = 16[(p2p_validate.rules).float.type = "p2p@local|confloat"];
  float title_test = 17 [(p2p_validate.rules).float.title = "title_test"];
}
```
`protobuf-to-pydantic` can read the generated Message object at runtime and generate a `Pydantic Model` object with the corresponding information:

```python
# pydantic version V1
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel, confloat
from pydantic.fields import FieldInfo

# import protobuf gen python obj
from example.proto_3_20_pydanticv1.example.example_proto.p2p_validate import demo_pb2


class CustomerField(FieldInfo):
    pass


DemoModel: Type[BaseModel] = msg_to_pydantic_model(
    demo_pb2.FloatTest,
    local_dict={"CustomerField": CustomerField, "confloat": confloat},
)
print(
    {
        k: v.field_info
        for k, v in DemoModel.__fields__.items()
    }
)
# output:
# {
#   'const_test': FieldInfo(default=1.0, const=True, extra={}),
#   'range_e_test': FieldInfo(default=0.0, ge=1, le=10, extra={}),
#   'range_test': FieldInfo(default=0.0, gt=1, lt=10, extra={}),
#   'in_test': FieldInfo(default=0.0, extra={'in': [1.0, 2.0, 3.0]}),
#   'not_in_test': FieldInfo(default=0.0, extra={'not_in': [1.0, 2.0, 3.0]}),
#   'default_test': FieldInfo(default=1.0, extra={}),
#   'default_factory_test': FieldInfo(default=PydanticUndefined, default_factory=<class 'float'>, extra={}),
#   'miss_default_test': FieldInfo(extra={}),
#   'alias_test': FieldInfo(default=0.0, alias='alias', alias_priority=2, extra={}),
#   'desc_test': FieldInfo(default=0.0, description='test desc', extra={}),
#   'multiple_of_test': FieldInfo(default=0.0, multiple_of=3, extra={}),
#   'example_test': FieldInfo(default=0.0, extra={'example': 1.0}),
#   'example_factory': FieldInfo(default=0.0, extra={'example': <class 'float'>}),
#   'field_test': CustomerField(default=0.0, extra={}),
#   'type_test': FieldInfo(default=0.0, extra={}),
#   'title_test': FieldInfo(default=0.0, title='title_test', extra={})
#   }
```

> Note:
>  - 1.See the [2.5.template](#25Template) for the usage of `local_dict`
>  - 2.If the reference to the Proto file fails, need to download [p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/protos/protobuf_to_pydantic/protos/p2p_validate.proto) in the project and use it in the Protobuf file。



### 2.4.`P2P` and text annotation rule other parameter support
The `protobuf-to-pydantic` text annotation rules and the `P2P` rules support most of the parameters in `FieldInfo`, as described in the [Pydantic Field doc](https://docs.pydantic.dev/latest/usage/fields/)。

> The new parameters added to `Pydantic V2` will be supported in next version , for now `P2P` rule naming is still written on the basis of `Pydantic V1`, but automatic mapping to `Pydantic V2` naming is supported.

Other partial changes in meaning and new parameters are described as follows:

| Parameter        | Default value | Illustrate                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| required         | False         | By default, the default value of each field in the generated `Pydantic Model` object is the same as the zero value of its corresponding type. When `required` is `True`, no more default values are generated for the fields.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| enable           | True          | By default, `protobuf-to-pydantic` generates all fields for `Message`, if don't want the generated `Message` to have this field, can set `enable` to `False`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| const            | None          | Used to specify a constant value for a field, though different `Pydantic` versions behave differently<br/>  For `Pydantic V1`, the value of `default` in `Field` is set to the value specified by `const`, and `const` in `Field` is set to True.Note: `Pydantic Model`'s const only supports bool variables, when `const` is `True`, the accepted value can only be the value set by `default`, and the default value carried by the message generated by protobuf is the zero value of the corresponding type does not match with `Pydantic Model`, so ` protobuf-to-pydantic` makes some changes to the input of this value.<br/> For `Pydantic V2`, the value of `default` in `Field` remains the same, but the type annotation changes to `typing_extensions.Literal[xxx]` |
| type             | None          | By default, the default type of a field is the same as Protobuf's, but use the [2.5.template](#25Template) function to modify the type of a field.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| extra            | None          | The `extra` parameter accepted by `Pydantic` is of type `Python Dict`, which is not supported by Protobuf, and requires the use of either [2.5.Templates](#25Templates) or the corresponding Json structure `protobuf-to-pydantic` in the Protobuf file to parse it properly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| field            | None          | By default, the `Field` of the parameter is `Pydantic FieldInfo`, although it can be customized using the [2.5.Templates](#25Templates) function                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| default_template | None          | Similar to `default`, default values can be customized in fields that are not of string type using the [2.5.Templates](#25Templates) feature.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

In addition to the above parameters, also support for fast import of `Pydantic type` for string types. For example, if want to add a check for card numbers via the `pydantic.types.PaymentCardNumber` type, can specify the type of the `pydantic_type` parameter field to be `PaymentCardNumber`, which is similar to the use of template imports in the `type` rule, as follows:
- Text annotation rules：
  ```protobuf
  syntax = "proto3";
  package common_validate_test;

  // common example
  message UserPayMessage {
    string bank_number=1; // p2p: {"pydantic_type": "PaymentCardNumber"}
    string other_bank_number=2; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```
- P2P rules：
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;

  import "example_proto/common/p2p_validate.proto";
  // p2p example
  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
    string other_bank_number=2[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
  }
  ```

> See [Extra Types Overview](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) for supported `Pydantic Types'.
### 2.5.Template
When working with definition fields, will find that some fields are filled with values that are methods or functions of one of the libraries in `Python` (e.g., the values of the `type` parameter and the `default_factory` parameter), which can't be accomplished with the Json syntax.
At this point, templates can be used to solve the corresponding problem, and currently `protobuf-to-pydantic` supports a variety of template functi

> Note: The `p2p` string at the beginning of a template can be defined via the comment_prefix variable

#### 2.5.1.`p2p@import`Template
The `p2p@import` template is used to represent variables in other modules that need to be introduced before they can be used, as follows.
- Examples of text annotation rules：
  ```protobuf
  syntax = "proto3";
  package comment_validate_test;

  // comment example
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```

- Examples of P2P rules (1)：
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;
  import "example_proto/common/p2p_validate.proto";

  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
  }
  ```

- Examples of P2P rules (2)：
  ```protobuf
  syntax = "proto3";
  package p2p_other_validate_test;
  import "example_proto/common/p2p_validate.proto";
  // p2p other example
  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
  }
  ```

The example Protobuf file uses a syntax in the format `p2p@{methods of the template}|{modules to be imported:A}|{variables in modules:B}`, indicating that a `B` object needs to be imported by `from A import B` and used by the corresponding rule.
With the definition of the template, `protobuf-to-pydantic` converts the corresponding Message into a `Pydantic Model`, as follows:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.5.2.`p2p@import_instance` Template
The `p2p@import_instance` template introduces the class of a library and then instantiates it in combination with the specified parameters before it is used by the corresponding rule, which is used as follows:
```protobuf
syntax = "proto3";
package p2p_validate_test;
import "google/protobuf/any.proto";
import "example_proto/common/p2p_validate.proto";
// p2p example
message AnyTest {
  google.protobuf.Any default_test = 23 [
    (p2p_validate.rules).any.default = 'p2p@import_instance|google.protobuf.any_pb2|Any|{"type_url": "type.googleapis.com/google.protobuf.Duration"}'
  ];
}
```
The syntax used here is `p2p@{methods of the template}|{modules to be introduced}|{classes to be introduced}|{initialization parameters}`, and the definition of `protobuf-to-pydantic` through the template will turn the corresponding Message into the following `Pydantic Model` object:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
    )
```

#### 2.5.3.`p2p@local` Template
This template is used to introduce user-defined variables, using a syntax in the format `{method of the template}|{local variable to be used}`, as follows:

- Example of text annotation:
  ```protobuf
  syntax = "proto3";
  package comment_validate_test;
  import "google/protobuf/timestamp.proto";
  import "example_proto/common/p2p_validate.proto";
  // comment example
  message UserPayMessage {
    google.protobuf.Timestamp exp=1; // p2p: {"default_factory": "p2p@local|exp_time"}
  }
  ```
- Examples of P2P rules：
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;
  import "google/protobuf/timestamp.proto";
  import "example_proto/common/p2p_validate.proto";
  // p2p example
  message UserPayMessage {
    google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.default_factory= "p2p@local|exp_time"];
  }
  ```
However, the `msg_to_pydantic_model` func needs to be called with the parameter `local_dict` to register the corresponding value, the pseudo-code is as follows:
```Python
# a.py
import time

from example.proto_3_20_pydanticv1.example.example_proto.p2p_validate import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model


def exp_time() -> float:
  return time.time()

msg_to_pydantic_model(
    demo_pb2.NestedMessage,
    local_dict={"exp_time": exp_time},  # <----  use local_dict
)
```
In this way, `protobuf-to-pydantic` generates a conforming `Pydantic Model` object:
```python
# b.py
from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from a import exp_time  # <-- exp_time in a.py

class UserPayMessage(BaseModel):
    exp: datetime = FieldInfo(default_factory=exp_time, extra={})
```


#### 2.5.4.`p2p@builtin` Template
This template (which can be thought of as a simplified version of the `p2p@local` template) can be used directly when the variables to be used come from `Python` built-in functions,the syntax is used as follows:
- Examples of text annotation rules:
  ```protobuf
  syntax = "proto3";
  package comment_validate_test;
  import "google/protobuf/timestamp.proto";
  import "example_proto/common/p2p_validate.proto";
  // comment example
  message UserPayMessage {
    google.protobuf.Timestamp exp=1; // p2p: {"type": "p2p@builtin|float"}
  }
  ```
- Examples of P2P rules：
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;
  import "google/protobuf/timestamp.proto";
  import "example_proto/common/p2p_validate.proto";
  // p2p example
  message UserPayMessage {
    google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.type= "p2p@builtin|float"];
  }
  ```
Then can directly generate a conforming `Pydantic Model` object by calling the `msg_to_pydantic_model` function, as follows:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.5.5.Customized templates
Currently `protobuf-to-pydantic` only supports a few simple templates, if have more template needs, can extend the templates by inheriting the `Template` class.

For example, there is an odd feature that requires the default value of a field to be the timestamp of the time when the `Pydantic Model` object was generated, but the timestamps used are available in lengths of 10 and 13, so the following Protobuf file needs to be written to support defining the length of the timestamps:
```protobuf
syntax = "proto3";
package p2p_validate_test;
import "google/protobuf/timestamp.proto";
import "example_proto/common/p2p_validate.proto";

message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default_template = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default_template = "p2p@timestamp|13"];
}
```
As you can see, the Protobuf file customizes the syntax of `p2p@timestamp|{x}`, where `x` has only two values, 10 and 13. The next step is to write code based on this template behavior, which looks like this.

```python
import time
from protobuf_to_pydantic.gen_model import Template


class CustomTemplate(Template):
  def template_timestamp(self, length_str: str) -> int:
    timestamp: float = time.time()
    if length_str == "10":
      return int(timestamp)
    elif length_str == "13":
      return int(timestamp * 100)
    else:
      raise KeyError(f"timestamp template not support value:{length_str}")


from .demo_pb2 import TimestampTest  # fake code
from protobuf_to_pydantic import msg_to_pydantic_model

msg_to_pydantic_model(
  TimestampTest,
  template=CustomTemplate  # <-- Use a custom template class
)
```
This code first creates a class `CustomTemplate` that inherits from `Template`.
During the execution process, it is found that when the parameter verification rule starts with `p2p@`, the parameter will be sent to the `template_{template name}` method corresponding to the `Template` class, so `CustomTemplate` defines the `template_timestamp` method to implement the `p2p@timestamp` template function.
In addition, the `length_str` variable received in this method is either 10 in `p2p@timestamp|10` or 13 in `p2p@timestamp|13`.

Then load the `CustomTemplate` through the `msg_to_pydantic_model` function, then the following code will be generated (assuming that the code is generated at a timestamp of 1600000000):
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```

> Note: In plugin mode, you can declare a template class to be loaded through a configuration file.

## 3.Code format
The code generated directly through `protobuf-to-pydantic` is not perfect, but it is possible to indirectly generate code that conforms to the `Python` specification through different formatting tools.
Currently, `protobuf-to-pydantic` supports formatting tools such as `autoflake`, `black` and `isort`. If the corresponding formatting tool is installed in the current `Python` environment, then `protobuf-to-pydantic` will call the tool to format the generated code before outputting it to a file.

In addition, the decision to enable or disable a formatting tool can be made through the `pyproject.toml` configuration file, the `pyproject.toml` example of which reads as follows:
```toml
# Controls which formatting tools protobuf-to-pydantic uses,
# if false then no formatting tools are used (default is true)
[tool.protobuf-to-pydantic.format]
black = true
isort = true
autoflake = true

# black docc:https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-format
[tool.black]
line-length = 120
target-version = ['py37']

# isort doc:https://pycqa.github.io/isort/docs/configuration/config_files.html#pyprojecttoml-preferred-format
[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 120

# autoflake doc:https://github.com/PyCQA/autoflake#configuration
[tool.autoflake]
in-place = true
remove-all-unused-imports = true
remove-unused-variables = true
```

## 4.example
`protobuf-to-pydantic` provides some simple example code for reference only.

### 4.1.Generate code directly
Protobuf file: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)

Generate `Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code.py)

Generate `Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code.py)
### 4.2.Text annotation
Protobuf File: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)

`Pydantic Model` generated based on `pyi` file(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py)

`Pydantic Model` generated based on `pyi` file(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py)

`Pydantic Model` generated based on protobuf file(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py)
`Pydantic Model` generated based on protobuf file(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py)
validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)

Generate `Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_pgv.py)

Generate `Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_pgv.py)
### 4.4.P2P rule
Protobuf file: [p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)

Generate `Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_p2p.py)

Generate `Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_p2p.py)
### 4.5.Protoc Plugin-in
Protobuf field:
 - [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)
 - [validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)
 - [p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)
 - [p2p_validate_by_comment/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate_by_comment/demo.proto)

`Pydantic Model` generated via `demo/demo.proto`(Pydantic V1):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/demo/demo_p2p.py)

`Pydantic Model` generated via `demo/demo.proto`(Pydantic V2):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/demo/demo_p2p.py)

`Pydantic Model` generated via `validate/demo.proto`(Pydantic V1):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/validate/demo_p2p.py)

`Pydantic Model` generated via `validate/demo.proto`(Pydantic V2):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/validate/demo_p2p.py)

`Pydantic Model` generated via `p2p_validate/demo.proto`(Pydantic V1):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/p2p_validate/demo_p2p.py)

`Pydantic Model` generated via `p2p_validate/demo.proto`(Pydantic V2):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/p2p_validate/demo_p2p.py)

`Pydantic Model` generated via `p2p_validate_by_comment/demo.proto`(Pydantic V1):[example/example_proto/p2p_validate_by_comment](https://github.com/so1n/protobuf_to_pydantic/tree/master/example/proto_pydanticv1/example/example_proto/p2p_validate_by_comment)

`Pydantic Model` generated via `p2p_validate_by_comment/demo.proto`(Pydantic V2):[example/example_proto/p2p_validate_by_comment](https://github.com/so1n/protobuf_to_pydantic/tree/master/example/proto_pydanticv2/example/example_proto/p2p_validate_by_comment)
