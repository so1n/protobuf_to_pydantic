# protobuf_to_pydantic
基于Protobuf文件(Proto3)生成带有参数校验功能的`Pydantic Model`或者是源码。

# Feature

功能：
- [x] 通过`Protobuf`插件生成源码。
- [x] 在`Python`运行时通过解析`Protobuf Message`生成`Pydantic Model`或者是源码。
- [x] 兼容`Pydantic`的`V1`和`V2`版本。
- [x] 生成的源码自动格式化。
- [x] 支持多种校验规则，兼容`proto-gen-validate`(后续版本将支持`proto-gen-validate`1.0的规则)。
- [x] 通过模板支持自定义功能。
- [ ] 支持`protovalidate`校验规则（也就是`proto-gen-validate`1.0）



下面是`protobuf-to-pydantic`的功能概览图，图中`p2p`代表的是`protobuf-to-pydantic`，`Protoc`代表`Protobuf`生成代码的命令，而`plugin`代表`Protoc`的插件:
![protobuf-to-pydantic](https://github.com/so1n/protobuf_to_pydantic/blob/master/images/protobuf-to-pydantic_index.png?raw=true)

# 安装
默认情况下，通过下面的命令可以直接安装`protobuf-to-pydantic`:
```bash
pip install protobuf_to_pydantic
```
如果想要使用`protobuf-to-pydantic`的完整功能，可以使用如下命令安装`protobuf-to-pydantic`:
```bash
pip install protobuf_to_pydantic[all]
```


# 使用
## 1.代码生成
`protobuf-to-pydantic`目前拥有两种方法基于Protobuf文件生成`Pydantic Model`对象：
- 1: 插件模式：以`Protoc`插件的方式通过Protobuf文件生成对应的`Python`代码文件。
- 2: 运行时模式：在`Python`运行时根据`Message`对象生成对应的`Pydantic Model`对象。

### 1.1.插件模式
#### 1.1.0.安装依赖
`protobuf-to-pydantic`插件依赖`mypy-protobuf`，需要先通过如下命令安装`mypy-protobuf`:
```bash
python -m pip install protobuf-to-pydantic[mypy-protobuf]
```
or
```bash
poetry add protobuf-to-pydantic -E mypy-protobuf
```
#### 1.1.1.使用插件
`protobuf-to-pydantic`插件是`protobuf-to-pydantic`推荐的`Pydantic Model`源码生成的方式，它支持的功能是最全的，同时使用起来也非常简单，假设平时是通过如下命令生成Protobuf文件对应的代码:
```bash
python -m grpc_tools.protoc -I. example.proto
# or
protoc -I. --python_out=. example.proto
```
那么,在安装`protobuf-to-pydantic`后可以通过`--protobuf-to-pydantic_out`选项使用`protobuf-to-pydantic`的插件，命令如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=. example.proto
# or
protoc -I. --protobuf-to-pydantic_out=. example.proto
```
在这个命令中`--protobuf-to-pydantic_out=.`表示使用`prorobuf_to_pydantic`插件，
且声明了`protobuf-to-pydantic`插件的输出位置为`.`(`.`表示采用`grpc_tools.proto`使用的输出路径)。


在运行命令后`protobuf-to-pydantic`插件会把生成源码文本写入到一个文件名后缀为`p2p.py`的文件中，如`protobuf-to-pydantic`为`example.proto`生成的代码文件名为`example_p2p.py`.

#### 1.1.2.插件的配置
`protobuf-to-pydantic`插件支持通过读取一个`Python`文件来加载配置。

> 为了保证能够正常的引入配置文件的变量，配置文件应尽量存放在运行命令的当前路径下。

一个可以被`protobuf-to-pydantic`读取的配置内容大概如下:

```Python
import logging
from typing import List, Type

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.template import Template

# 配置插件的日志输出格式，和日志等级，在DEBUG的时候非常有用
logging.basicConfig(
  format="[%(asctime)s %(levelname)s] %(message)s",
  datefmt="%y-%m-%d %H:%M:%S",
  level=logging.DEBUG
)


class CustomerField(FieldInfo):
  pass


def customer_any() -> Any:
  return Any  # type: ignore


# local模板的配置，详见local模板的使用
local_dict = {
  "CustomerField": CustomerField,
  "confloat": confloat,
  "conint": conint,
  "customer_any": customer_any,
}
# 指定关键注释的开头
comment_prefix = "p2p"
# 指定模板的类，可以通过继承该类拓展模板，详见自定义模板章节
template: Type[Template] = Template
# 指定要忽略的哪些package的protobuf文件，被忽略的package的message不会被解析
ignore_pkg_list: List[str] = ["validate", "p2p_validate"]
# 指定生成的文件名后缀(不包含.py)
file_name_suffix = "_p2p"
```
接下来为了能读取到这个文件，需要将命令中的`--protobuf-to-pydantic_out=.`更改为`--protobuf-to-pydantic_out=config_path=plugin_config.py:.`，
其中`:`左边的`config_path=plugin_config.py`表示要读取的配置文件路径为`plugin_config.py`，而`:`的右边与之前的`.`一样，声明了`protobuf-to-pydantic`插件的输出位置，
最终完整的命令如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
# or
protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
```
通过这个命令就可以加载对应的配置再运行`protobuf-to-pydantic`插件。


除了示例的配置文件中配置选项外，`protobuf-to-pydantic`插件还支持其他的配置选项，具体的配置说明如下：

| 配置名                           | 所属功能             | 类型                                              | 含义                                                                                                                                                    |
|-------------------------------|------------------|-------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| local_dict                    | 模板               | dict                                            | 存放供`local`模板使用的变量                                                                                                                                     |
| template                 | 模板               | protobuf_to_pydantic.template.Template | 模板类的实现                                                                                                                                                |
| comment_prefix                | 模板               | str                                             | 注释前缀，只有固定前缀的字符串才会被模板使用                                                                                                                                |
| parse_comment                 | 注释(只限Protoc插件)   | bool                                            | 如果为True，则会兼容注释形式的参数校验规则                                                                                                                               |
| comment_handler| 注释(只限Protoc插件)   | Callable[[str, str, FieldInfo], FieldInfo] | 自定义注释处理器，用于处理注释中的参数校验规则，使用该配置时，配置参数`comment_prefix`与`parse_comment`将不会生效，具体使用方法见[custom_comment_handler_pkg_plugin_config.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/custom_comment_handler_pkg_plugin_config.py) |
| customer_import_set           | 代码生成             | `Set[str]`                                      | 自定义import语句的集合，会写入到源码文件中，如`from typing import Set`或者是`import typing`                                                                                  |
| customer_deque                | 代码生成             | `deque[str]`                                    | 自定义源码文件内容，用于增加自定义内容                                                                                                                                   |
| module_path                   | 代码生成             | str                                             | 用于定义项目/模块的根路径，辅助`protobuf-to-pydantic`能更好的自动生成模块的引入语句                                                                                                 |
| pyproject_file_path           | 代码生成             | str                                             | 定义pyproject文件路径，默认为当前项目的路径                                                                                                                            |
| code_indent                   | 代码生成             | int                                             | 定义代码的缩进空格数量，默认为4                                                                                                                                      |
| ignore_pkg_list               | 代码生成(只限插件)       | `list[str]`                                     | 定义忽略指定package文件的解析                                                                                                                                    |
| base_model_class              | Model生成，代码生成     | `Type[BaseModel]`                               | 定义生成的Model的父类                                                                                                                                         |
| file_name_suffix              | 代码生成             | str                                             | 定义生成的文件后缀，默认为`_p2p.py`                                                                                                                                |
| file_descriptor_proto_to_code | 代码生成(只限Protoc插件) | `Type[FileDescriptorProtoToCode]`               | 定义使用的FileDescriptorProtoToCode                                                                                                                        |
| protobuf_type_config          | 代码生成(只限Protoc插件) | `Dict[str, ProtobufTypeConfigModel]`            | 兼容不规范的Message，具体见[ConfigModel说明](https://github.com/so1n/protobuf_to_pydantic/blob/master/protobuf_to_pydantic/plugin/config.py)                      |
| pkg_config                    |代码生成(只限Protoc插件)| `Dict[str, "ConfigModel"]`                        | 为每一个pkg适配对应的配置                                                                                                                                        |


> Note:
>   - 1:配置的具体说明见[/protobuf_to_pydantic/plugin/config.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/protobuf_to_pydantic/plugin/config.py)
>   - 2:使用方法见[/example/plugin_config.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/plugin_config.py)
#### 1.1.3.buf-cli
如果你是使用`buf-cli`来管理Protobuf文件，那么也可以在`buf-cli`中使用`protobuf-to-pydantic`，具体请访问[如何在`buf-cli`中使用使用`protobuf-to-pydantic`](https://github.com/so1n/protobuf_to_pydantic/blob/master/buf-plugin/README_ZH.md)了解详情。


### 1.2.运行时模式
`protobuf-to-pydantic`可以在运行时根据`Message`对象的信息生成对应的 `Pydantic Model`对象。

例如下面一个名为`demo.proto`的Protobuf文件中的`UserMessage`：
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
通过`protoc`可以生成`Protobuf`文件对应的`Python`代码文件(文件名为`demo_pb2.py`)，代码文件中存在`UserMessage`的相关代码。

在`Python`运行时可以调用`protobuf-to-pydantic`的`msg_to_pydantic_model`函数读取`demo_pb2`模块中的`UserMessage`对象，并生成生成对应的`Pydantic Model`对象，如下:
```Python
# pydantic version V1
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
#   'uid': FieldInfo(default='', extra={}),
#   'age': FieldInfo(default=0, extra={}),
#   'height': FieldInfo(default=0.0, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', extra={})
#  }
```
通过输出结果可以看到生成的`Pydantic Model`对象与Protobuf文件中的`UserMessage`一样包含了`uid`,`age`,`height`,`sex`,`is_adult`和`user_name`字段，且`default`属性的值与Protobuf对应类型的零值是一致的。

`msg_to_pydantic_model`函数与插件一样支持可定制，对应的拓展参数如下:

|字段| 含义                              |
|---|---------------------------------|
|default_field| 生成`Pydantic Model`中每个字段的`Field` |
|comment_prefix| 可以被解析的注释的前缀                     |
|parse_msg_desc_method| 使用的解析规则                         |
|local_dict| `local`模板使用的变量                  |
|pydantic_base| 生成`Pydantic Model`对象的父类         |
|pydantic_module| 生成`Pydantic Model`对象的`Module`   |
|template| 使用的模板类                          |
|message_type_dict_by_type_name| Protobuf类型与`Python`类型的映射      |
|message_default_factory_dict_by_type_name| Protobuf类型与`Python`类型工厂的映射    |

其中，`parse_msg_desc_method`是定义`protobuf_to_pydantic`从哪里获取到Message对象的规则信息。

### 1.2.1.parse_msg_desc_method
默认情况下，`parse_msg_desc_method`的值为空，此时`protobuf_to_pydantic`会通过Message对象的Option获取参数校验规则。

如果参数校验的规则是通过注释声明的，那么`protobuf_to_pydantic`只能通过另外两种形式来获取参数校验规则。

- 1:`parse_msg_desc_method`的值为`Message`对应的`Python`模块

  在这种情况下，`protobuf-to-pydantic`在运行的过程能够通过`Python`模块对应的`.pyi`文件中的的注释来获取Message对象中每个字段的附加信息。
  比如上述示例代码中`demo_pb2.UserMessage`对应的`Python`模块为`demo_pb2`。

  > 注：该功能需要在通过Protobuf文件生成对应的`Python`代码时使用[mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)插件，且指定的pyi文件输出路径与生成的`Python`代码路径相同时才能生效。
  > 在执行前请通过`python -m pip install protobuf-to-pydantic[mypy-protobuf]`命令安装`protobuf-to-pydantic`

- 2:`parse_msg_desc_method`的值为Protobuf文件的路径

  除了通过`.pyi`文件获取注释外，`protobuf-to-pydantic`还支持通过Message对象所属的Protobuf文件的注释来获取每个字段的注释信息。
使用这个功能很简单，只需要把`parse_msg_desc_method`的值设置为Message对象生成时指定的根目录路径即可。

  > 在使用该方法时，请确保通过`python -m pip install protobuf-to-pydantic[lark]`安装`protobuf-to-pydantic`，同时也要确保Protobuf文件存在于项目中。

  比如`protobuf-to-pydantic`示例代码的项目结构如下:
  ```bash
  ./protobuf_to_pydantic/
  ├── example/
  │ ├── python_example_proto_code/
  │ └── example_proto/
  ├── protobuf_to_pydantic/
  └── /
  ```
  其中Protobuf文件存放在`example/example_proto`文件夹中，然后在`example`目录下运行如下命令生成Protobuf对应的`Python`代码文件:
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
  那么此时`parse_msg_desc_method`需要填写的路径是`./protobuf_to_pydantic/example`。
  比如下面的示例代码：
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
  可以看到，这份代码的唯一区别就是`parse_msg_desc_method`的值不同，但是输出结果中每个字段携带的信息与通过模块获取的结果是一样的。

### 1.3.直接生成文件
除了在运行时生成对应的`Pydantic Model`对象外，`protobuf-to-pydantic`还支持在运行时将`Pydantic Model`对象转为对应的`Python`代码文本（仅兼容`protobuf-to-pydantic`生成的`Pydantic Model`对象)。
其中，`pydantic_model_to_py_code`用于生成代码源码，`pydantic_model_to_py_file`用于生成代码文件，`pydantic_model_to_py_file`函数的示例代码如下：
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
代码运行的时候，会先把`demo_pb2.NestedMessage`转换为`Pydantic Model`对象，接着传入到`pydantic_model_to_py_file`函数中，由`pydantic_model_to_py_file`生成对应的源码内容再写入到`demo_gen_code.py`文件中。

## 2.参数校验
在上一节中，Protobuf文件生成的`Pydantic Model`对象非常简单，这是因为Protobuf文件没有足够的参数验证信息。
为了使生成的`Pydantic Model`对象中的每个字段都拥有参数校验功能，需要完善Protobuf文件中每个Message的字段的参数校验规则。
目前`protobuf-to-pydantic`支持下面三种参数校验规则：
- 1.文本注释
- 2.PGV(protoc-geb-validate)
- 3.P2P

通过这些规则，可以让`protobuf-to-pydantic`生成的`Pydantic Model`对象拥有参数校验功能。
其中文本注释和P2P的规则是一致的，它们都支持`Pydantic Field`中的大多数参数，部分有变化和新增的参数见[2.4.`P2P`与文本注释的其它参数支持](#24p2p与文本注释的其它参数支持)

> NOTE:
>  - 1.文本注释规则不是后续功能迭代开发的重点，推荐使用P2P校验规则。
>  - 2.插件模式下，文本注释的编写方法略有变化，详情请参考:[example/example_proto/p2p_validate_by_comment/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate_by_comment/demo.proto)
>  - 3.插件模式会自动选择最适配的参数校验规则。

### 2.1.文本注释
在Protobuf文件中可以为每个字段编写符合`protobuf-to-pydantic`要求的注释，以便`protobuf-to-pydantic`在解析Protobuf文件时能够获得到参数的校验信息，比如下面这个例子
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
在这个例子中，每个可以被`protobuf-to-pydantic`使用的注释都是以`p2p:`开头(可以通过`comment_prefix`自定义)，并在后面跟着一个完整的Json字符串。
如果熟悉`pydantic`的用法，可以发现Json字符串包含的都是对应`pydantic.Field`的校验信息，
比如`UserMessage`中的`uid`字段总共附带的4个信息如下：

| 字段          | 含义                             |
|-------------|--------------------------------|
| required    | 表示生成的字段不带有默认值                  |
| example     | 表示生成的字段的示例值为10086              |
| title       | 表示字段的schema名称为UID              |
 | description | 表示字段的schema文档描述为 `user union id` |

> Note:
>   - 1.目前只支持单行注释且注释必须是一个完整的Json数据(不能换行)。

这样一来，`protobuf-to-pydantic`通过Message生成的`Pydantic Model`对象中的每个字段都拥有对应的信息，如下代码:
```python
# pydantic version V1
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.proto_3_20_pydanticv1.example.example_proto.demo import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(demo_pb2.UserMessage, parse_msg_desc_method=demo_pb2)
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
在执行代码后通过输出结果可以看到输出的字段中都携带着对应的信息，这些数据与Protobuf文件的注释是一致的。

### 2.2.PGV(protoc-gen-validate)
目前Protobuf生态中常用的参数校验项目是[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)，
在使用的过程中，只要编写一次`PGV`规则就能生成不同编程语言，但拥有相同校验规则的`Message`对象，已然成为Protobuf中的通用标准。

> 目前`protobuf-to-pydantic`只支持[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)小于1.0.0版本的规则

`protobuf-to-pydantic`支持解析`PGV`的校验规则并生成带有校验逻辑的`pydantic Model`对象， 在`protobuf-to-pydantic`中使用`PGV`校验规则非常简单，只要先在Protobuf文件编写对应的`PGV`规则，然后在调用`msg_to_pydantic_model`时指定`parse_msg_desc_method`的值为`PGV`即可，代码如下：
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
#   'const_test': FieldInfo(default=1.0, const=True, extra={}),
#   'range_e_test': FieldInfo(default=0.0, ge=1, le=10, extra={}),
#   'range_test': FieldInfo(default=0.0, gt=1, lt=10, extra={}),
#   'in_test': FieldInfo(default=0.0, extra={'in': [1.0, 2.0, 3.0]}),
#   'not_in_test': FieldInfo(default=0.0, extra={'not_in': [1.0, 2.0, 3.0]}),
#   'ignore_test': FieldInfo(default=0.0, extra={})
# }
```


> Note:
>  - 1.`PGV`的使用方法见:[protoc-gen-validate doc](https://github.com/bufbuild/protoc-gen-validate/blob/v0.10.2-SNAPSHOT.17/README.md)
>  - 2.可以通过以下三种方法引入validate
>    - 2.1.使用前请通过`pip install protoc_gen_validate`安装`PGV`
>    - 2.2.把[validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto)下载到项目的Protobuf目录中。
>    - 2.3.通过[buf-cli](https://github.com/so1n/protobuf_to_pydantic/blob/master/buf-plugin/README_ZH.md)安装validate


### 2.3.P2P
`PGV`校验规则是编写在`Message`每个字段的Option属性中，拥有较好的代码规范，所以使用`PGV`校验规则的Protobuf的可读性会比使用注释的Protobuf高，
同时在编写`PGV`规则时，还可以体验到IDE的自动补全带来的便利性以及通过Protobuf文件生成对应语言对象时进行校验的安全性，
不过它只支持校验相关的逻辑，功能丰富度不如文件注释模式。

`protobuf-to-pydantic`自带的`P2P`校验规则则是在`PGV`校验规则的基础上进行拓展，融合了文本注释校验规则的一些功能，该模式下满足了绝大多数`Pydantic Model`中每个`Field`的属性定制，比如下面的Protobuf文件:
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
`protobuf-to-pydantic`可以在运行时读取Protobuf生成的Message对象，并生成带有对应信息的`Pydantic Model`对象，如下代码:

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
>  - 1.local_dict等模板的使用方法见模板章节
>  - 2.如果出现引用Proto文件失败，需要将[p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/protos/protobuf_to_pydantic/protos/p2p_validate.proto)文件下载到项目中的protobuf目录中，才能在Protobuf文件中使用。



### 2.4.`P2P`与文本注释的其它参数支持
`protobuf-to-pydantic`的文本注释规则和`P2P`规则支持`FieldInfo`中的大部分参数，具体见[Pydantic Field文档](https://docs.pydantic.dev/latest/usage/fields/)。

> `Pydantic V2`新增的参数将会在下一个版本提供支持，目前`P2P`的规则命名仍是基于`Pydantic V1`编写的，但是支持自动映射为`Pydantic V2`的命名。

其它部分含义有变动和新增的参数说明如下:

| 参数               | 默认值   | 说明                                                                                                                                                                                                                                                                                                                                                                                 |
|------------------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| required         | False | 默认情况下，生成的`Pydantic Model`对象中每个字段的默认值与它对应类型的零值是一致的，不过当`required`为`True`时会取消默认值的设置。                                                                                                                                                                                                                                                                                                  |
| enable           | True  | 默认情况下，`protobuf-to-pydantic`会为`Message`生成所有字段，如果不想生成的`Message`拥有此字段，可以设置`enable`为`False`。                                                                                                                                                                                                                                                                                          |
| const            | None  | 用于指定字段的常量值，不过不同的`Pydantic`版本的表现是不一样的<br/> 对于 `Pydantic V1`，`Field`中`default`的值会被设定为`const`指定的值，`Field`中的`const`被设置为True。注: `Pydantic Model`的const只支持bool变量，当`const`为`True`时，接受的值只能是`default`设定的值，而protobuf生成的Message携带的默认值为对应类型的空值与`Pydantic Model`不匹配，所以`protobuf-to-pydantic`对这个值的输入进行了一些变动。<br/> 对于`Pydantic V2`，`Field`中`default`的值不变，但类型注解会变为`typing_extensions.Literal[xxx]` |
| type             | None  | 默认情况下，字段的默认类型与Protobuf的类型是一致的，但是可以使用[2.5.模板](#25模板)功能修改字段的类型                                                                                                                                                                                                                                                                                                              |
| extra            | None  | `Pydantic`接受的`extra`参数的类型为`Python Dict`，Protobuf不支持该类型，在Protobuf文件中需要使用[2.5.模板](#25模板)或者是对应的Json结构`protobuf-to-pydantic`才可以正常解析。                                                                                                                                                                                                                                                   |
| field            | None  | 默认情况下，参数的`Field`为`Pydantic FieldInfo`，不过可以使用[2.5.模板](#25模板)功能进行定制                                                                                                                                                                                                                                                                                                                  |
| default_template | None  | 与`default`作用类似，在非字符串类型的字段可以使用[2.5.模板](#25模板)功能进行定制默认值                                                                                                                                                                                                                                                                                                                              |


此外，针对字符串类型还支持`Pydantic type`类型的快速导入，比如想通过`pydantic.types.PaymentCardNumber`类型来增加对银行卡号码的校验，那么可以通过指定`pydantic_type`参数字段的类型为`PaymentCardNumber`，它与在`type`规则使用模板引入的功能是类似的，如下:
- 文本注释规则：
  ```protobuf
  syntax = "proto3";
  package common_validate_test;

  // common example
  message UserPayMessage {
    string bank_number=1; // p2p: {"pydantic_type": "PaymentCardNumber"}
    string other_bank_number=2; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```
- P2P规则：
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

> 支持的`Pydantic Type`见[Extra Types Overview](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/)

### 2.5.模板
在使用定义字段时，会发现有些字段填写的值是`Python`中某个库的方法或者函数(比如`type`参数和`default_factory`参数的值)，这是无法通过Json语法来实现。
这时可以使用模板参数来解决对应的问题，目前`protobuf-to-pydantic`支持多种模板功能。

> Note:模板开头的`p2p`字符串可以通过comment_prefix变量来定义

#### 2.5.1.`p2p@import`模板
`p2p@import`模板用于表示其它模块下且需要先引入再使用的变量，具体的使用方法如下:
- 注释规则的示例：
  ```protobuf
  syntax = "proto3";
  package comment_validate_test;

  // comment example
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```

- P2P规则的示例（一）：
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;
  import "example_proto/common/p2p_validate.proto";

  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
  }
  ```

- P2P规则的示例（二）：
  ```protobuf
  syntax = "proto3";
  package p2p_other_validate_test;
  import "example_proto/common/p2p_validate.proto";
  // p2p other example
  // 由于引入的类型刚好属于`pydantic.types`模块的，所以`p2p`模式下可以直接使用string.pydantic_type
  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
  }
  ```

示例的Protobuf文件使用的是`p2p@{模板的方法}|{要引入的模块:A}|{模块中的变量:B}`格式的语法，表示需要通过`from A import B`来引入`B`对象并被对应的规则使用，
通过模板的定义，`protobuf-to-pydantic`会把对应的Message转为如下的`Pydantic Model`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.5.2.`p2p@import_instance`模板
`p2p@import_instance`模板是先引入某个库的类，再结合指定的参数进行实例化后才被对应的规则使用，该模板的使用方法如下:
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
这里使用的是`p2p@{模板的方法}|{要引入的模块}|{要引入的类}|{初始化的参数}`语法，通过模板的定义，`protobuf-to-pydantic`会把对应的Message转为如下`Pydantic Model`对象:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
    )
```

#### 2.5.3.`p2p@local`模板
该模板用于引入用户自定义的变量，这里使用的是`{模板的方法}|{要使用的本地变量}`格式的语法，如下：

- 注释规则的示例:
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
- P2P规则的示例
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

不过，在调用`msg_to_pydantic_model`函数时需要通过参数`local_dict`注册对应的值，伪代码如下：
```Python
# a.py
import time

from example.proto_3_20_pydanticv1.example.example_proto.p2p_validate import demo_pb2
from protobuf_to_pydantic import msg_to_pydantic_model


def exp_time() -> float:
  return time.time()

msg_to_pydantic_model(
    demo_pb2.NestedMessage,
    local_dict={"exp_time": exp_time},  # <---- 使用local_dict
)
```
这样一来，`protobuf-to-pydantic`就可以生成符合要求的`Pydantic Model`对象：
```python
# b.py
from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from a import exp_time  # <-- 使用到a.py中的exp_time

class UserPayMessage(BaseModel):
    exp: datetime = FieldInfo(default_factory=exp_time, extra={})
```

> Note: 具体调用和生成方法见示例代码。

#### 2.5.4.`p2p@builtin`模板
当需要使用的变量来自于`Python`内建函数时，可以直接使用该模板（可以认为是`p2p@local`模板的简化版本），语法使用如下：
- 注释规则的示例:
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
- P2P规则的示例:
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
接着就可以通过调用`msg_to_pydantic_model`函数直接生成符合要求的`Pydantic Model`对象，如下：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.5.5.自定义模板
目前`protobuf-to-pydantic`只支持几种简单模板，如果有更多的模板需求，可以通过继承`Template`类来对模板进行拓展。

比如有一个奇葩的需求，要求字段的默认值为Message对象生成`Pydantic Model`对象时的时间戳，不过使用的时间戳有长度为10位和13位两个版本, 于是需要编写如下Protobuf文件来支持定义时间戳的长度：
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
在这个文件中使用了自定义的`p2p@timestamp|{x}`的语法，其中`x`只有10和13两个值，接下来就可以根据这个模板行为编写代码了，代码如下:

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
  template=CustomTemplate  # <-- 使用自定义的模板类
)
```
这段代码先是创建了一个继承于`Template`的`CustomTemplate`的类，
在执行的过程中，发现参数校验规则是以`p2p@`开头时就会把参数发到`Template`类对应的`template_{template name}`方法，所以`CustomTemplate`定义了`template_timestamp`的方法来实现`p2p@timestamp`模板功能。
此外，在这个方法中接收的`length_str`变量则是`p2p@timestamp|10`中的10或者是`p2p@timestamp|13`中的13。

在创建完`CustomTemplate`后，通过`msg_to_pydantic_model`函数加载`CustomTemplate`，那么会生成如下代码(假设在时间戳为1600000000时生成的代码)：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```

> Note: 插件模式下可以通过配置文件声明要加载的模板类。

## 3.代码格式化
通过`protobuf-to-pydantic`直接生成的代码不是完美的，但是可以通过不同的格式化工具来间接的生成符合`Python`规范的代码。
目前, `protobuf-to-pydantic`支持`autoflake`, `black`和`isort`等格式化工具。如果在当前的`Python`环境中安装了对应的格式化工具，那么`protobuf-to-pydantic`会调用工具对生成的代码进行格式化再输出到文件中。

此外，开发者可以通过`pyproject.toml`配置文件来决定格式化工具如何执行，`pyproject.toml`示例内容如下：
```toml
# 控制protobuf-to-pydantic使用哪些格式化工具，如果为false则不使用格式化工具（默认为true）
[tool.protobuf-to-pydantic.format]
black = true
isort = true
autoflake = true

# black配置文档见:https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-format
[tool.black]
line-length = 120
target-version = ['py38']

# isort配置文档见:https://pycqa.github.io/isort/docs/configuration/config_files.html#pyprojecttoml-preferred-format
[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 120

# autoflake配置文档见:https://github.com/PyCQA/autoflake#configuration
[tool.autoflake]
in-place = true
remove-all-unused-imports = true
remove-unused-variables = true
```

## 4.example
`protobuf-to-pydantic`提供了一些简单的示例代码，以下是示例代码和protobuf文件的路径，仅供参考。

### 4.1.直接生成
protobuf文件: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)

生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code.py)

生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code.py)
### 4.2.注释规则
protobuf文件: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)

基于`pyi`文件生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py)

基于`pyi`文件生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py)

基于Protobuf文件生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py)

基于Protobuf文件生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py)
### 4.3.PGV规则
protobuf文件: [validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)

生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_pgv.py)

生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_pgv.py)
### 4.4.P2P规则
protobuf文件: [p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)

生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_p2p.py)

生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_p2p.py)
### 4.5.Protoc插件
protobuf文件:
 - [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)
 - [validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)
 - [p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)
 - [p2p_validate_by_comment/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate_by_comment/demo.proto)

通过`demo/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/demo/demo_p2p.py)

通过`demo/demo.proto`生成的`Pydantic Model`(Pydantic V2):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/demo/demo_p2p.py)

通过`validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/validate/demo_p2p.py)

通过`validate/demo.proto`生成的`Pydantic Model`(Pydantic V2):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/validate/demo_p2p.py)

通过`p2p_validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/p2p_validate/demo_p2p.py)

通过`p2p_validate/demo.proto`生成的`Pydantic Model`(Pydantic V2):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/p2p_validate/demo_p2p.py)

通过`p2p_validate_by_comment/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example/example_proto/p2p_validate_by_comment](https://github.com/so1n/protobuf_to_pydantic/tree/master/example/proto_pydanticv1/example/example_proto/p2p_validate_by_comment)

通过`p2p_validate_by_comment/demo.proto`生成的`Pydantic Model`(Pydantic V2):[example/example_proto/p2p_validate_by_comment](https://github.com/so1n/protobuf_to_pydantic/tree/master/example/proto_pydanticv2/example/example_proto/p2p_validate_by_comment)
