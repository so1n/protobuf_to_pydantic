# protobuf_to_pydantic
基于Protobuf文件生成带有参数校验功能的`Pydantic Model`或者是源码。

![protobuf-to-pydantic](https://github.com/so1n/protobuf_to_pydantic/blob/master/images/protobuf-to-pydantic_index.png?raw=true)

功能：
- 通过`Protobuf`插件生成源码。
- 在`Python`运行时通过解析`Protobuf Message`生成`Pydantic Model`或者是源码。
- 兼容`Pydantic`的`V1`和`V2`版本。
- 生成的源码自动格式化。
- 支持多种校验规则，兼容`proto-gen-validate`(后续版本将支持`proto-gen-validate`1.0的规则)。
- 通过模板支持自定义功能。

> NOTE:
>  - 当前只支持proto3版本的protobuf

# 1.安装
```bash
pip install protobuf_to_pydantic
```

# 2.使用方法
`protobuf_to_pydantic`目前拥有两种方法来通过Protobuf文件生成`pydantic.BaseModel`对象：
- 1: 以`Protoc`插件的方式通过Protobuf文件生成对应的`Python`代码文件供开发者使用，
- 2: 运行时根据`Message`对象生成对应的`pydantic.BaseModel`对象。

## 2.1.通过插件直接生成`pydantic.BaseModel`代码文件
## 2.1.0.安装依赖
```bash
python -m pip install protobuf-to-pydantic[mypy-protobuf]
```
or
```bash
poetry add protobuf-to-pydantic -E mypy-protobuf
```
### 2.1.1.使用插件
插件是`protobuf-to-pydantic`最推荐的`Pydantic Model`源码生成的方式，它支持的功能是最全的，同时使用起来也非常简单，假设平时是通过如下命令生成Protobuf文件对应的代码:
```bash
python -m grpc_tools.protoc -I. example.proto
```
那么在安装`protobuf-to-pydantic`后可以通过`--protobuf-to-pydantic_out`选项来使用`protobuf_to_pydantic`的插件，命令如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=. example.proto
```
在这个命令中`--protobuf-to-pydantic_out=.`表示使用`prorobuf-to-pydantic`插件，
且声明了`protobuf-to-pydantic`插件的输出位置为`.`(表示采用`grpc_tools.proto`使用的输出路径)。
在运行命令后`protobuf-to-pydantic`插件会在对应的文件中写入自己生成的内容(默认情况下，文件名后缀为`p2p.py`)，如`protobuf-to-pydantic`为`example.proto`生成的代码文件名为`example_p2p.py`

### 2.1.2.插件的配置
`protobuf-to-pydantic`支持通过读取一个`Python`文件来加载配置。

> 为了保证能够正常的引入配置文件的变量，配置文件必须存放在运行命令的当前路径下。

一个示例配置内容如下:
```Python
import logging
from typing import List, Type

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.desc_template import DescTemplate

# 配置插件的日志输出格式，和日志等级，在DEBUG的时候非常有用
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.DEBUG)


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
desc_template: Type[DescTemplate] = DescTemplate
# 指定要忽略的哪些package的protobuf文件，被忽略的package的message不会被解析
ignore_pkg_list: List[str] = ["validate", "p2p_validate"]
# 指定生成的文件名后缀(不包含.py)
file_name_suffix = "_p2p"
```
为了能读取到这个文件，需要将命令中的`--protobuf-to-pydantic_out=.`更改为`--protobuf-to-pydantic_out=config_path=plugin_config.py:.`，
其中`:`左边的`config_path=plugin_config.py`表示要读取的配置文件路径为`plugin_config.py`，而`:`的右边还是跟之前的`.`一样，声明了`protobuf-to-pydantic`插件的输出位置。
最终完整的命令如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
```
通过这个命令就可以加载对应的配置再运行`protobuf-to-pydantic`插件。


支持的配置说明如下：
|配置名|类型|含义|
|---|---|---|
|local_dict|dict|存放变量供`local`模板使用|
|desc_template|protobuf_to_pydantic.desc_template.DescTemplate|模板类的实现|
|comment_prefix|str|注释前缀，只有固定前缀的字符串才会被模板使用|
|customer_import_set|`Set[str]`|自定义import语句的集合，会写入到源码文件中，如`from typing import Set`或者是`import typing`|
|customer_deque|`deque[str]`|自定义源码文件内容，用于增加自定义内容|
|module_path|str|用于定义项目/模块的根路径，辅助`protobuf-to-pydantic`能更好的自动生成模块的引入语句|
|pyproject_file_path|str|定义pyproject文件路径，默认为当前项目的路径|
|code_indent|int|定义代码的缩进空格数量，默认为4|
|ignore_pkg_list|`list[str]`|定义忽略指定package文件的解析|
|base_model_class|`Type[BaseModel]`|定义生成的Model的父类|
|file_name_suffix|str|定义生成的文件后缀，默认为`_p2p.py`|
|file_descriptor_proto_to_code|`Type[FileDescriptorProtoToCode]`|定义使用的FileDescriptorProtoToCode|


## 2.2.在Python运行时生成`pydantic.BaseModel`对象
`protobuf_to_pydantic`可以在运行时根据`Message`对象生成对应的 `pydantic.BaseModel`对象。

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
通过`grpc_tools.protoc`可以生成`Protobuf`文件对应的`Python`代码(这时的文件名为`demo_pb2.py`)，
而`protobuf_to_pydantic`的`msg_to_pydantic_model`方法可以在运行时读取Proto文件生成的Message对象生成对应的`pydantic.BaseModel`对象，如下:
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
通过输出结果可以发现生成的`pydantic.BaseModel`对象与`Protobuf`文件中的`UserMessage`一样包含了`uid`,`age`,`height`,`sex`,`is_adult`和`user_name`字段，且`default`属性的值与Protobuf对应类型的零值是一致的。

除了在运行时生成对应的`pydantic.BaseModel`对象外，`protobuf_to_pydantic`还支持在运行时将`pydantic.BaseModel`对象转为对应的`Python`代码文本（仅兼容`protobuf_to_pydantic`生成的`pydantic.BaseModel`对象)。
其中，`pydantic_model_to_py_code`用于生成代码源码，`pydantic_model_to_py_file`用于生成代码文件，`pydantic_model_to_py_file`方法示例代码如下：
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
代码运行的时候，会先把`demo_pb2.NestedMessage`转换为`pydantic Model`对象，接着传入到`pydantic_model_to_py_file`方法中，由`pydantic_model_to_py_file`生成对应的源码内容再写入到`demo_gen_code.py`文件中。

## 2.3.参数校验
在上一节中，Protobuf文件生成的`Pydantic Model`对象只会携带少量的信息，这是因为Protobuf文件并没有携带足够的参数验证相关信息。
为了使生成的`Pydantic Model`对象中的每个字段都拥有参数校验功能，需要在Protobuf文件中完善字段对应的参数校验规则。
目前`protobuf_to_pydantic`支持多种方式来获取Message的其他信息，使得生成的`pydantic.BaseModel`对象具有参数校验的功能。

> NOTE:
>  - 1.文本注释功能不是后续功能开发重点，推荐使用P2P校验规则。
>  - 2.插件只支持PGV和P2P校验规则。

### 2.3.1.文本注释
开发者可以在Protobuf文件中为每个字段编写符合`protobuf_to_pydantic`要求的注释来为`protobuf_to_pydantic`提供参数校验信息，比如下面这个例子
```protobuf
syntax = "proto3";
package user;

enum SexType {
  man = 0;
  women = 1;
}

// user info
message UserMessage {
  // p2p: {"miss_default": true, "example": "10086"}
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
在这个例子中，每个可以被`protobuf_to_pydantic`使用的注释都是以`p2p:`开头(支持自定义)，并在后面跟着一个完整的Json字符串，如果熟悉`pydantic`的用法，可以发现Json字符串包含的都是对应`pydantic.Field`的校验信息，
比如`UserMessage`中的`uid`字段总共附带的4个信息如下：

| 字段           | 含义                             |
|--------------|--------------------------------|
| miss_default | 表示生成的字段不带有默认值                  |
| example      | 表示生成的字段的示例值为10086              |
| title        | 表示字段的schema名称为UID              |
 | description  | 表示字段的schema文档描述为 `user union id` |

> Note:
>   - 1.目前只支持单行注释且注释必须是一个完整的Json数据(不能换行)。
>   - 2.不支持多行注释。

当编写了这些注释后，`protobuf_to_pydantic`在把Message转换成对应的`Pydantic Model`对象时都会为每个字段带上对应的信息，如下代码:
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
可以看出，输出的字段中都携带着对应的信息，这些数据与Protobuf文件的注释是一致的。
除此之外，这段代码与上一节不同的是`msg_to_pydantic_model`函数多了一个名为`parse_msg_desc_method`的关键字参数且它的值为`demo_pb2`模块,
该参数会使`protobuf_to_pydantic`能够通过`demo_pb2`模块的`.pyi`文件中的的注释来获取Message对象中每个字段的附加信息。

> 注：该功能需要在通过Protobuf文件生成对应的`Python`代码时使用[mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)插件，且指定的pyi文件输出路径与生成的`Python`代码路径相同时才能生效。

除了通过`.pyi`文件获取注释外，`protobuf_to_pydantic`还支持通过解析Message对象所属的Protobuf文件的注释来获取每个字段注释信息，为了使用这个功能，需要把`parse_msg_desc_method`的值设置为Message对象生成时指定的根目录路径。

> 在使用该方法时，请确保通过`python -m pip install protobuf-to-pydantic[lark]`安装`protobuf-to-pydantic`，同时也要确保Protobuf文件存在于项目中。

比如`protobuf_to_pydantic`示例代码的项目结构如下:
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
可以看到，这份代码的唯一区别就是`parse_msg_desc_method`的值不同，但是通过输出结果可以看出字段携带的信息与通过模块获取的结果一样。
### 2.3.2.PGV(protoc-gen-validate)
目前Protobuf生态中常用的对象校验方法是直接使用[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目，而[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目也支持多种语言，大部分Protobuf开发者会编写一次`pgv`规则使不同的语言都支持相同的校验规则。

> 目前`protobuf-to-pydantic`只支持[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)小于1.0.0版本的规则

而`protobuf-to-pydantic`也支持解析`pgv`的校验规则并生成带有对应校验逻辑的`pydantic Model`对象， 在`protobuf_to_pydantic`中使用`Pgv`校验规则非常简单，只要先在Protobuf文件编写对应的`Pgv`规则，然后在通过方法`msg_to_pydantic_model`进行转化时指定`parse_msg_desc_method`的值为`PGV`即可，代码如下：
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
>  - 1.`Pgv`的使用方法见:[protoc-gen-validate doc](https://github.com/bufbuild/protoc-gen-validate/blob/v0.10.2-SNAPSHOT.17/README.md)
>  - 2.使用前请通过`pip install protoc_gen_validate`安装`Pgv`或者把[validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto)下载到项目中的protobuf目录中，才能在Protobuf文件中编写pgv规则。


### 2.2.3.P2P
`PGV`校验规则是编写在`Message`每个字段的Option属性中，拥有较好的代码规范，所以使用`PGV`校验规则的Protobuf文件的可读性会比携带文件注释的Protobuf文件高，
同时开发者在编写`PGV`规则时，还可以体验到IDE的自动补全带来的便利性以及通过Protobuf文件生成对应语言对象时进行校验的安全性。
不过它只支持校验相关的逻辑，功能丰富度不如文件注释模式。

`P2P`校验规则则是在`PGV`校验规则的基础上进行拓展，融合了文本注释校验规则的一些功能，该模式下满足了绝大多数`Pydantic Model`中每个`Field`的属性定制，比如下面的Protobuf文件:
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
`protobuf_to_pydantic`可以在运行时读取生成的Message对象，并生成带有对应信息的`pydantic.BaseModel`对象:

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
值得注意的是，这段代码没有显示的指明`parse_msg_desc_method`的值是`p2p`，因为`p2p`已经是`protobuf_to_pydantic`的默认规则了。

> Note:
>  - 1.local_dict等模板的使用方法见模板章节
>  - 2.如果出现引用Proto文件失败，需要将[p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/protos/protobuf_to_pydantic/protos/p2p_validate.proto)文件下载到项目中的protobuf目录中，才能在Protobuf文件中使用。



### 2.3.3.其它参数支持
`protobuf_to_pydantic`的文件注释校验规则和`P2P`校验规则除了支持`FieldInfo`的参数外，还支持下面几种参数:
- miss_default：默认情况下，生成的`Pydantic Model`对象中每个字段的默认值与它对应类型的零值是一致的，不过当`miss_default`为`true`时会取消默认值的设置。
- enable: 默认情况下， `Pydantic Model`会把Message中的每个字段都进行转换，如果有些字段不想被转换，可以设置`enable`为`false`
- const: 指定字段的常量的值。特别说明，当设定了`coset`后生成的`Pydantic Model`会根据`pydantic`的版本生成不一样的代码。
  - `Pydantic V1`： `Field`中`default`的值为`conse`指定的值，`const`被设置为True。注: `Pydantic Model`的const只支持bool变量，当`const`为`True`时，接受的值只能是`default`设定的值，而protobuf生成的Message携带的默认值为对应类型的空值与`Pydantic Model`不匹配，所以`protobuf_to_pydantic`对这个值的输入进行了一些变动，但`const`设置了值后，生成的字段中`cost`属性为`True`，而`default`会变为`const`设置的对应值。
  - `Pydnatic V2`: `Field`中`default`的值不变，但类型注解会变为`typing_extensions.Literal[xxx]`
- type: 拓展目前的类型，比如想通过`pydantic.types.PaymentCardNumber`类型来增加对银行卡号码的校验，那么可以通过如下方法来指定字段的类型为`PaymentCardNumber`:
  ```protobuf
  syntax = "proto3";
  package common_validate_test;

  // common example
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```
  ```protobuf
  syntax = "proto3";
  package p2p_validate_test;

  import "example_proto/common/p2p_validate.proto";
  // p2p example
  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
  }
  ```

> Note:
>   如果不了解`pydantic`，可以通过下面的URL了解Field的用途:
>
>   - https://docs.pydantic.dev/latest/usage/fields/

### 2.3.4.模板
有些情况下，我们填写的值是`Python`中某个库的方法或者函数(比如`type`参数和`default_factory`参数的值)，这是无法通过Json语法来实现。
这时可以使用模板参数来解决对应的问题，目前`protobuf_to_pydantic`支持多种模板参数。

> Note:模板开头的`p2p`字符串可以通过comment_prefix变量来定义

#### 2.3.4.1.`p2p@import`模板
`p2p@import`模板用于表示该值是其它模块下的变量，需要先引入再使用，具体的使用方法如下:

注释规则的示例：
```protobuf
syntax = "proto3";
package comment_validate_test;

// comment example
message UserPayMessage {
  string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
}
```

P2P规则的示例一：
```protobuf
syntax = "proto3";
package p2p_validate_test;
import "example_proto/common/p2p_validate.proto";

message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
}
```

P2P规则的示例二：
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
示例的Protobuf文件中使用的是`p2p@{模板的方法}|{要引入的模块:A}|{模块中的变量:B}`格式的语法，表示这是需要通过`from A import B`来引入`B`对象并被对应的规则使用，
通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下的`Pydantic Model`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.3.4.2.`p2p@import_instance`模板
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
这里使用的是`p2p@{模板的方法}|{要引入的模块}|{要引入的类}|{初始化的参数}`语法，通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下`Pydantic Model`对象:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
    )
```

#### 2.3.4.3.`p2p@local`模板
该模板用于引入用户自定义的变量，这里使用的是`{模板的方法}|{要使用的本地变量}`格式的语法，如下：

注释规则的示例:
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
P2P规则的示例
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
然后在调用`msg_to_pydantic_model`方法时通过参数`local_dict`注册对应的值，伪代码如下：
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
这样一来，`protobuf_to_pydantic`就可以生成符合要求的`Pydantic Model`对象：
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

#### 2.3.4.4.`p2p@builtin`模板
当需要使用的变量来自于`Python`内建函数时，可以直接使用该模板（可以认为是`p2p@local`模板的简化版本），语法使用如下：
注释规则的示例
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
P2P规则的示例
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
在调用`msg_to_pydantic_model`方法时无需进行任何修改，`protobuf_to_pydantic`可以直接生成符合要求的`Pydantic Model`对象，如下：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.3.4.5.自定义模板
目前`protobuf_to_pydantic`只支持几种简单模板，如果有更多的模板需求，可以通过继承`DescTemplate`类来对模板进行拓展。

比如有一个奇葩的需求，要求字段的默认值为Message对象生成`Pydantic Model`对象时的时间戳，不过使用的时间戳有长度为10位和13位两个版本, 于是需要编写如下Protobuf文件来支持定义时间戳的长度：
```protobuf
syntax = "proto3";
package p2p_validate_test;
import "google/protobuf/timestamp.proto";
import "example_proto/common/p2p_validate.proto";

message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default = "p2p@timestamp|13"];
}
```
在这个文件中使用了自定义的`p2p@timestamp|{x}`的语法，其中`x`只有10和13两个值，接下来就可以根据这个模板行为编写代码了，代码如下:
```python
import time
from typing import Any, List
from protobuf_to_pydantic.gen_model import DescTemplate


class CustomDescTemplate(DescTemplate):
    def template_timestamp(self, template_var_list: List[str]) -> Any:
        timestamp: float = time.time()
        length: str = template_var_list[0]
        if length == "10":
            return int(timestamp)
        elif length == "13":
            return int(timestamp * 100)
        else:
            raise KeyError(f"timestamp template not support value:{length}")


from .demo_pb2 import TimestampTest # fake code
from protobuf_to_pydantic import msg_to_pydantic_model

msg_to_pydantic_model(
    TimestampTest,
    desc_template=CustomDescTemplate   # <-- 使用自定义的模板类
)
```
这段代码先是创建了一个继承于`DescTemplate`的`CustomDescTemplate`的类，
由于`DescTemplate`会根据模板的命名转发到对应的`template_{template name}`方法，所以这个类定义了`template_timestamp`的方法来实现`p2p@timestamp`模板功能。
此外，在这个方法中接收的`template_var_list`变量则是`p2p@timestamp|10`中的10或者是`p2p@timestamp|13`中的13。

实现完`CustomDescTemplate`后，在`msg_to_pydantic_model`中通过`desc_template`关键参数来指定模板类为`CustomDescTemplate`，
这样一来，通过`msg_to_pydantic_model`生成的`Pydantic Model`代码会发生变化，如下(假设在时间戳为1600000000时生成的代码)：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```
## 3.代码格式化
通过`protobuf_to_pydantic`直接生成的代码不是完美的，但是可以通过不同的格式化工具来间接的生成符合`Python`规范的代码。
目前支持的格式化工具有`autoflake`, `black`和`isort`，如果在当前的`Python`环境中安装了对应的格式化工具，那么`protobuf_to_pydantic`在生成代码后会调用工具对生成的代码进行格式化再输出到文件中。

此外，开发者可以通过`pyproject.toml`配置文件来决定格式化工具如何执行，`pyproject.toml`示例内容如下：
```toml
# 控制protobuf-to-pydantic使用哪些格式化工具，如果为false则表示不对应的使用格式化工具（默认为true）
[tool.protobuf-to-pydantic.format]
black = true
isort = true
autoflake = true

# black配置文档见:https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-format
[tool.black]
line-length = 120
target-version = ['py37']

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
`protobuf_to_pydantic`提供了一些简单的示例代码，以下是示例代码和protobuf文件的路径，仅供参考。

### 4.1.直接生成
protobuf文件: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)
生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code.py)
生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code.py)
### 4.2.使用注释规则
protobuf文件: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)
基于`pyi`文件生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_pyi.py)
基于`pyi`文件生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_pyi.py)
基于Protobuf文件生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_text_comment_protobuf_field.py)
基于Protobuf文件生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_text_comment_protobuf_field.py)
### 4.3.使用PGV规则
protobuf文件: [validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)
生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_pgv.py)
生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_pgv.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_pgv.py)
### 4.4.使用P2P规则
protobuf文件: [p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)
生成的`Pydantic Model`(Pydantic V1): [proto_pydanticv1/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/demo_gen_code_by_p2p.py)
生成的`Pydantic Model`(Pydantic V2): [proto_pydanticv2/demo_gen_code_by_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/demo_gen_code_by_p2p.py)
### 4.5.Protoc插件
protobuf文件: [demo/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/demo/demo.proto)，[validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/validate/demo.proto)，[p2p_validate/demo.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/p2p_validate/demo.proto)

> Note: Protoc插件只支持P2P和PGV校验规则

通过`demo/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/demo/demo_p2p.py)
通过`demo/demo.proto`生成的`Pydantic Model`(Pydantic V2):[example_proto/demo/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/demo/demo_p2p.py)
通过`validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/validate/demo_p2p.py)
通过`validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/validate/demo_p2p.py)
通过`p2p_validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv1/example/example_proto/p2p_validate/demo_p2p.py)
通过`p2p_validate/demo.proto`生成的`Pydantic Model`(Pydantic V1):[example_proto/p2p_validate/demo_p2p.py](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/proto_pydanticv2/example/example_proto/p2p_validate/demo_p2p.py)
