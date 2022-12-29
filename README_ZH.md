# protobuf_to_pydantic
通过Protobuf文件生成带有参数校验功能的`pydantic.BaseModel`类(以及对应的源码)

> NOTE:
>  - 只支持proto3

# 1.安装
```bash
pip install protobuf_to_pydantic
```

# 2.使用方法
`protobuf_to_pydantic`目前拥有两种方法来通过Protobuf文件生成`pydantic.BaseModel`对象，
第一种方法是以插件的方式通过Protobuf文件生成对应的`Python`代码文件供开发者使用，
第二种方法是在运行时根据`Message`对象生成对应的`pydantic.BaseModel`对象。

## 2.1.通过插件直接生成`pydantic.BaseModel`代码文件
### 2.1.1.插件的使用
插件方式是`protobuf-to-pydantic`最推荐的使用方式，它支持的功能是最全的，同时使用起来也非常简单，假设平时是通过如下命令生成Protobuf文件对应的代码:
```bash
python -m grpc_tools.protoc -I. example.proto
```
那么在安装`protobuf-to-pydantic`后可以通过`--protobuf-to-pydantic_out`选项来使用`protobuf_to_pydantic`，命令如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=. example.proto
```
> Note: `protobuf-to-pydantic`插件依赖于`mypy-protobuf`，请通过类似命令`python -m pip install protobuf-to-pydanitc[mypy-protobuf]`安装`mypy-protobuf`。

其中`--protobuf-to-pydantic_out=.`表示使用`prorobuf-to-pydanitc`插件，且声明了`protobuf-to-pydantic`插件的输出位置为`.`(表示采用`grpc_tools.proto`使用的输出路径)，
这样一来`protobuf-to-pydantic`插件会在对应的文件中写入自己生成的内容(文件名以`p2p.py`结尾)，如`protobuf-to-pydantic`为`example.proto`生成的代码文件名为`example_p2p.py`

> Note: 如果当前`Python`环境安装了`isort`和`black`那么`protobuf_to_pydantic`会通过`isort`和`black`格式化生成的代码。
### 2.1.2.插件的配置
`protobuf-to-pydantic`支持通过读取一个`Python`文件来支持配置功能。
开发者首先需要在运行命令的当前路径创建一个配置文件，文件名如`plugin_config.py`，并写入如下代码:
```Python
import logging
from typing import List, Type

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.gen_model import DescTemplate

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
```
接着，将命令中的`--protobuf-to-pydantic_out=.`更改为`--protobuf-to-pydantic_out=config_path=plugin_config.py:.`,如下：
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
```
其中`:`左边的`config_path=plugin_config.py`表示要读取的配置文件路径为`plugin_config.py`，而`:`的右边还是声明了`protobuf-to-pydantic`插件的输出位置为`.`。
这样一来`protobuf-to-pydantic`插件在运行的时候可以加载到开发者指定的配置文件，再根据配置文件定义的配置运行。
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
通过`grpc_tools.protoc`可以根据Protobuf文件生成对应的`Python`代码(这时的文件名为`demo_pb2.py`)，
而`protobuf_to_pydantic`的`msg_to_pydantic_model`方法可以在运行时读取Proto文件生成的Message对象的数据，并生成对应的`pydantic.BaseModel`对象:
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
#   'uid': FieldInfo(default='', extra={}),
#   'age': FieldInfo(default=0, extra={}),
#   'height': FieldInfo(default=0.0, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', extra={})
#  }
```
通过输出结果可以发现生成的`pydantic.BaseModel`对象一样包含`uid`,`age`,`height`,`sex`,`is_adult`和`user_name`字段，且他们对应的`default`信息与Protobuf文件中的`UserMessage`一致。

除了在运行时生成对应的`pydantic.BaseModel`对象外，`protobuf_to_pydantic`还支持在运行时将`pydantic.BaseModel`对象转为对应的`Python`代码文本（仅兼容`protobuf_to_pydantic`生成的`pydantic.BaseModel`对象)。
其中，`protobuf_to_pydantic`的`pydantic_model_to_py_code`方法用于生成代码文本，`protobuf_to_pydantic`的`pydantic_model_to_py_file`方法用于生成代码文件，`protobuf_to_pydantic`的`pydantic_model_to_py_file`方法示例代码如下：
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
该代码会先把`demo_pb2.NestedMessage`转换为`pydantic.BaseModel`对象，然后再被`pydantic_model_to_py_file`方法生成到`demo_gen_code.py`文件中。
需要注意的是，如果`protobuf_to_pydantic`检查到当前环境安装了`isort`和`black`，则默认会通过它们来格式化生成的代码。

## 2.3.参数校验
根据Protobuf文件生成的`Message`对象只会携带少量的信息，这是因为普通的Protobuf文件并没有足够的参数验证相关信息，这需要我们通过一些额外的途径来完善`Message`对象的参数验证信息。
目前`protobuf_to_pydantic`支持多种方式来获取Message的其他信息，使得生成的`pydantic.BaseModel`对象具有参数校验的功能。

> NOTE:
>  - 1.文本注释功能不是后续功能开发重点，推荐使用P2P模式。
>  - 2.插件模式只支持PGV和P2P模式

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

当编写了这些注释后，`protobuf_to_pydantic`在把Message转换成对应的`Pydantic.BaseModel`对象时都会为每个字段带上对应的信息，如下:

```python
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
#   'uid': FieldInfo(default=PydanticUndefined, title='UID', description='user union id', extra={'example': '10086'}),
#   'age': FieldInfo(default=0, title='use age', ge=0, extra={'example': 18}),
#   'height': FieldInfo(default=0.0, ge=0, le=2, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', description='user name', min_length=1, max_length=10, extra={'example': 'so1n'})
# }
```
可以看出，输出的字段中携带着对应的信息，除此之外，这段代码与上面不同的是`msg_to_pydantic_model`函数多了一个名为`parse_msg_desc_method`的关键字参数且它的值为`demo_pb2`模块,
该参数会使`protobuf_to_pydantic`能够通过`demo_pb2`模块的`.pyi`文件中的的注释来获取Message对象中每个字段的附加信息。

> 注：该功能需要在通过Protobuf文件生成对应的`Python`代码时使用[mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)插件，且指定的pyi文件输出路径与生成的`Python`代码路径相同时才能生效。

除了通过`.pyi`文件获取注释外, `protobuf_to_pydantic`还支持通过设置`parse_msg_desc_method`的值为Message对象生成时指定的根目录路径，
从而使`protobuf_to_pydantic`通过解析Message对象对应的Protobuf文件的注释来获取附加信息。


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
那么此时`parse_msg_desc_method`需要填写的路径就是`./protobuf_to_pydantic/example`，代码如下：

```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

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
通过结果可以看出字段携带的信息与通过模块获取的结果一样
> NOTE: 该方法需要提前安装[lark](https://github.com/lark-parser/lark)且Protobuf文件必须存在于运行的项目中。
### 2.3.2.PGV(protoc-gen-validate)
目前Protobuf生态中常用的对象校验方法是直接使用[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目，而[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目也支持多种语言，大部分Protobuf开发者会编写一次`pgv`规则使不同的语言都支持相同的校验规则。

而`protobuf-to-pydantic`也支持解析`pgv`的校验规则生成带有对应校验逻辑的`pydantic.BaseModel`类， 在`protobuf_to_pydantic`中使用`Pgv`校验规则非常简单，只要先在Protobuf文件编写对应的`Pgv`规则，然后在通过方法`msg_to_pydantic_model`进行转化时指定`parse_msg_desc_method`的值为`PGV`即可，代码如下：
```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.validate import demo_pb2

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
>  - 1.`Pgv`的使用方法见:[protoc-gen-validate doc](https://github.com/bufbuild/protoc-gen-validate/blob/main/README.md#constraint-rules)
>  - 2.需要通过`pip install protoc_gen_validate`安装`Pgv`或者把[validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto)下载到项目中的protobuf目录中，才能在Protobuf文件中编写pgv规则。


### 2.2.3.P2p
`Pgv`的校验规则是编写在`Message`每个字段的Option属性中，有比较好的代码规范，所以携带`Pgv`校验规则的Protobuf文件的可读性会比携带文件注释的Protobuf文件高，
同时开发者在编写`Pgv`规则时，还可以体验到IDE的自动补全带来的便利性以及通过Protobuf文件生成对应语言对象时进行校验的安全性，不过它只支持校验相关的逻辑，功能丰富度不如文件注释模式。

而`P2P`模式是在`PGV`模式进行拓展，融合了文本注释的一些功能，该模式下满足了绝大多数`pydantic.BaseModel`中每个`Field`的属性定制，比如下面的Protobuf文件:
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
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel, confloat
from pydantic.fields import FieldInfo

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.p2p_validate import demo_pb2


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
`protobuf_to_pydantic`的文件注释模式和`p2p`模式除了支持`FieldInfo`的参数外，还支持下面几种参数:
- miss_default：默认情况下，生成对应`pydantic.BaseModel`对象中每个字段的默认值与Message中每个字段的默认值是一样的，不过当`miss_default`为`true`时会取消默认值的设置。
- enable: 默认情况下， `pydantic.BaseModel`会把Message中的每个字段都进行转换，如果有些字段不想被转换，可以设置`enable`为`false`
- const: 指定字段的常量的值。注：`pydantic.BaseModel`的const只支持bool变量，当`const`为`True`时，接受的值只能是`default`设定的值，而protobuf生成的Message携带的默认值为对应类型的空值与`pydantic.BaseModel`不匹配，所以`protobuf_to_pydantic`对这个值的输入进行了一些变动，但`const`设置了值后，生成的字段中`cost`属性为`True`，而`default`会变为`const`设置的对应值。
- type: 拓展目前的类型，比如想通过`pydantic.types.PaymentCardNumber`类型来增加对银行卡号码的校验，那么可以通过如下方法来指定字段的类型为`PaymentCardNumber`:
  ```protobuf
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```

> Note:
>   如果不了解`pydantic`，可以通过下面两个URL来了解Field支持的参数是什么:
>
>   - https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
>
>   - https://pydantic-docs.helpmanual.io/usage/schema/#field-customization

### 2.3.4.模板
有些情况下，我们填写的值是`Python`中某个库的方法或者函数(比如`type`参数和`default_factory`参数的值)，这是无法通过Json语法来实现。
这时可以使用模板参数来解决对应的问题，目前`protobuf_to_pydantic`支持多种模板参数。

> Note:模板开头的`p2p`字符串可以通过comment_prefix变量来定义

#### 2.3.4.1.`p2p@import`模板
该模板用于表示该值是其它模块下的变量，具体的使用方法如下:
```protobuf
// comment example
message UserPayMessage {
  string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
}

// p2p example
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
}

// p2p other example
// 由于引入的类型刚好属于`pydantic.types`模块的，所以`p2p`模式下可以直接使用string.pydantic_type
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
}
```
这里使用的是`p2p{模板的方法}|{要引入的模块:A}|{模块中的变量:B}`格式的语法，表示这是需要通过`from A import B`来引入`B`对象并被对应的规则使用，
通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下的`pydantic.BaseModel`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.3.4.2.`p2p@import_instance`模板
`p2p@import`模板只是引入并使用某个库的变量，而`p2p@import_instance`是先引入某个库的类，再结合指定的参数进行实例化后才被对应的规则使用，该模板的使用方法如下:
```protobuf
// p2p example
message AnyTest {
  google.protobuf.Any default_test = 23 [
    (p2p_validate.rules).any.default = 'p2p@import_instance|google.protobuf.any_pb2|Any|{"type_url": "type.googleapis.com/google.protobuf.Duration"}'
  ];
}
```
这里使用的是`{模板的方法}|{要引入的模块}|{对应的类}|{对应的参数}`语法，通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下`pydantic.BaseModel`对象:
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
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"default_factory": "p2p@local|exp_time"}
}
// p2p example
message UserPayMessage {
  google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.default_factory= "p2p@local|exp_time"];
}
```
然后在调用`msg_to_pydantic_model`方法时通过参数`local_dict`注册对应的值，伪代码如下：
```Python
import time


def exp_time() -> float:
  return time.time()

msg_to_pydantic_model(
    demo_pb2.NestedMessage,
    local_dict={"exp_time": exp_time},  # <----
)
```
这样一来，`protobuf_to_pydantic`就可以生成符合要求的`pydantic.BaseModel`对象了：
```python
from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from . import exp_time

class UserPayMessage(BaseModel):
    exp: datetime = FieldInfo(default_factory=exp_time, extra={})
```

> Note: 具体调用和生成方法见示例代码。

#### 2.3.4.4.`p2p@builtin`模板
当需要使用的变量来自于内建函数时，可以直接使用该模板（可以认为是`p2p@local`模板的简化版本），语法使用如下：
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"type": "p2p@builtin|float"}
}

// p2p example
message UserPayMessage {
  google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.type= "p2p@builtin|float"];
}
```
这样一来，`protobuf_to_pydantic`就可以生成符合要求的`pydantic.BaseModel`对象了：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.3.4.5.自定义模板
目前`protobuf_to_pydantic`只支持几种简单模板，如果有更多的模板需求，可以通过继承`DescTemplate`类来对模板进行拓展。
比如有一个奇葩的需求，要求字段的默认值为Message对象生成为`pydantic.BaseModel`对象时的时间戳，不过时间戳有长度为10位和13位两个版本, 于是编写如下Protobuf文件来支持定义时间戳的长度：
```protobuf
message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default = "p2p@timestamp|13"];
}
```
这个文件中使用了自定义的`p2p@timestamp|{x}`的语法，其中`x`只有10和13两个值，接下来就可以根据这个模板行为编写代码了，代码如下:
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
    desc_template=CustomDescTemplate
)
```
这段代码先是创建了一个继承于`DescTemplate`的`CustomDescTemplate`的类，这个类新增了一个`template_timestamp`的方法用于匹配`p2p@timestamp`语法，
然后在`msg_to_pydantic_model`中通过`desc_template`关键参数来指定模板类为`CustomDescTemplate`，这样`msg_to_pydantic_model`就会生成如下代码(假设在时间戳为1600000000时生成的代码)：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```
## 3.example
`protobuf_to_pydantic`提供了一些简单的示例代码，以下是示例代码和protobuf文件的路径，仅供参考:

|说明|Protobuf路径|示例代码|
| ---- | ---- | ---- |
|基于p2p模式生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/p2p_validate|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/p2p_validate_example|
|生成最基础的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/simple_example|
|通过.pyi文件生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/text_comment_example|
|通过protobuf文件生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/validate|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/validate_example|
