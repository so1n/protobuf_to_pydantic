# protobuf_to_pydantic
通过Protobuf文件生成的`Python` Message对象生成带有参数校验功能的`pydantic.BaseModel`。

> NOTE:
>  - 只支持proto3
>
>  - 该项目是从[pait](https://github.com/so1n/pait)项目0.7.9版本分离出来，所以本项目也是先在内存生成`pydantic.BaseModel`对象，再根据生成的对象生成对应的`Python`代码。

# 1.安装
```bash
pip install protobuf_to_pydantic
```

# 2.使用方法
## 2.1.运行时生成`pydantic.BaseModel`对象
`protobuf_to_pydantic`可以在运行时根据`Message`对象生成对应的 `pydantic.BaseModel`对象。

例如下面Protobuf文件中的`UserMessage`：
```protobuf
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
`protobuf_to_pydantic`可以在运行时读取从Proto文件生成的Message对象来生成对应的`pydantic.BaseModel`对象:

```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

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
## 2.2.参数校验
根据Protobuf文件生成的`Message`对象只携带少量的信息，没有足够的信息使生成的`pydantic.BaseModel`具有更加详细的参数验证功能，需要一些额外的途径来完善`Message`对象的数据。
目前`protobuf_to_pydantic`支持多种方式来获取Message的其他信息，使得生成的`pydantic.Base_Model`对象具有参数校验的功能。

> NOTE: 推荐使用P2P模式
### 2.2.1.文本注释
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
在这个例子中，每个可以被`protobuf_to_pydantic`使用的注释都是以`p2p:`开头(支持自定义)，并在后面跟着一个完整的Json字符串，如果熟悉`pydantic`的用法，可以发现这个Json字符串包含的都是对应`pydantic.Field`的校验信息，
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
可以看出，输出的字段中携带着对应的信息，除此之外，这段代码与上面不同的是`msg_to_pydantic_model`函数设置了一个名为`parse_msg_desc_method`的关键字参数且它的值为`demo_pb2`,
从而使`protobuf_to_pydantic`能够通过`demo_pb2`模块的`.pyi`文件中的的注释来获取Message对象中每个字段的附加信息。

> 注：该功能需要在通过Protobuf文件生成对应的`Python`代码时使用[mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)插件，且指定的pyi文件输出路径与生成的`Python`代码路径相同时才能生效。

除了通过`.pyi`文件获取注释外, `protobuf_to_pydantic`还支持通过设置`parse_msg_desc_method`的值为Message对象生成时指定的根目录路径，
从而使`protobuf_to_pydantic`通过解析Message对象对应的Protobuf文件的注释来获取信息。


比如`protobuf_to_pydantic`的项目结构如下:
```bash
./protobuf_to_pydantic/
├── example/
│ ├── python_example_proto_code/
│ └── example_proto/
├── protobuf_to_pydantic/
└── /
```
其中protobuf文件存放在`example/example_proto`文件中，然后在`example`目录下通过如下命令生成protobuf对应的`Python`代码文件:
```bash
cd example

python -m grpc_tools.protoc
  --python_out=./python_example_proto_code \
  --grpc_python_out=./python_example_proto_code \
  -I. \
```
那么此时需要填写的路径就是`./protobuf_to_pydantic/example`，代码如下：

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
### 2.2.2.PGV
目前用得比较多的Protobuf生成对象的校验方法就是直接使用[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目，使生成的Message对象带上了参数校验逻辑。
不过`Pgv`在`Python`中的实现比较特殊，它是生成一段含有大量判断代码的函数，所以性能不是很好，而`protobuf_to_pydantic`生成的`pydantic.BaseModel`对象本身就允许携带一些校验逻辑且自带的校验逻辑大多都是使用C进行编写的，性能比较高。

所以`protobuf_to_pydantic`支持通过解析Protobuf文件中每个字段携带的`Pgv`校验信息使生成的`pydantic.BaseModel`携带`Pgv`对应的校验逻辑。

在`protobuf_to_pydantic`中使用`Pgv`校验规则非常简单，只要先在Protobuf文件编写对应的`Pgv`规则，然后指定`parse_msg_desc_method`的值为`PGV`即可，代码如下：

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
>  - 1.`Pgv`的使用方法见:[protoc-gen-validate doc](https://github.com/envoyproxy/protoc-gen-validate/blob/main/README.md)
>  - 2.需要通过`pip install protoc_gen_validate`安装`Pgv`或者把[validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto)下载到项目中的protobuf目录中，才能在Protobuf文件中编写pgv规则。


### 2.2.3.P2p
`Pgv`的校验规则是编写在`Message`每个字段的Option属性中，有比较好的代码规范，所以携带`Pgv`校验规则的Protobuf文件的可读性会比携带文件注释的Protobuf文件高，
同时开发者在编写`Pgv`规则时，还可以体验到IDE的自动补全带来的便利性以及通过Protobuf文件生成对应语言对象时进行校验的安全性，不过它只支持校验相关的逻辑，功能丰富度不如文件注释模式。

而`P2P`模式是融合了`PGV`模式和文件注释模式的优点，该模式下满足了绝大多数`pydantic.BaseModel`中每个`Field`的属性定制，比如下面的Protobuf文件:
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
>  - 1.local_dict的使用方法见模板章节
>  - 2.如果出现引用Proto文件失败，需要下载[p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/p2p_validate/p2p_validate.proto)下载到项目中的protobuf目录中，才能在Protobuf文件中使用。



### 2.2.3.其它参数支持
`protobuf_to_pydantic`的文件注释模式和`p2p`模式除了支持`FieldInfo`的参数外，还支持下面几种参数:
- miss_default：默认情况下，生成对应`pydantic.BaseModel`对象中每个字段的默认值与Message中每个字段的默认值是一样的。不过可以通过设置`miss_default`为`true`来取消默认值的设置，需要注意的是在设置`miss_default`为`true`的情况下，`default`参数将失效。
- enable: 默认情况下， `pydantic.BaseModel`会把Message中的每个字段都进行转换，如果有些字段不想被转换，可以设置`enable`为`false`
- const: 指定字段的常量的值。注：`pydantic.BaseModel`的const只支持bool变量，当`const`为`True`时，接受的值只能是`default`设定的值，而protobuf生成的Message携带的默认值为对应类型的空值与`pydantic.BaseModel`不匹配，所以`protobuf_to_pydantic`对这个值的输入进行了一些变动，但`const`设置了值后，生成的字段中`cost`属性为`True`，而`default`会变为设置的对应值。
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

### 2.2.4.模板
有些情况下，我们填写的值是某个库的方法或者函数，比如`type`参数和`default_factory`参数的值，但是无法通过Json语法来实现，这时可以使用模板参数，目前`protobuf_to_pydantic`支持多种模板参数。

#### 2.2.4.1.`p2p@import`模板
该模板用于引入其它模块下的变量，具体的使用方法如下:
```protobuf
// comment example
message UserPayMessage {
  string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
}
// p2p example
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
}
// p2p another examlpe
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
}
```
这里使用的是`{p2p的方法}|{要引入的类:A}|{类的模块:B}`格式的语法，其中开头的方法`p2p@import`表示这是需要通过`from A import B`引入`B`对象，
通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下的`pydantic.BaseModel`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.2.4.2.`p2p@import_instance`模板
`p2p@import`只是引入某个库的变量，而`p2p@import_instance`是先引入某个库的类，再结合指定的参数进行实例化，使用方法如下:
```protobuf
message AnyTest {
  google.protobuf.Any default_test = 23 [
    (p2p_validate.rules).any.default = 'p2p@import_instance|google.protobuf.any_pb2|Any|{"type_url": "type.googleapis.com/google.protobuf.Duration"}'

  ];
}
```
这里使用的是`{p2p的方法}|{要引入的模块}|{对应的类}|{对应的参数}`语法，通过模板的定义，`protobuf_to_pydantic`会把对应的Message转为如下`pydantic.BaseModel`对象:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
```

#### 2.2.4.3.`p2p@local`模板
该模板用于引入用户自定义的变量，这里使用的是`{p2p的方法}|{要使用的本地变量}`格式的语法，如下：
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"default_factory": "p2p@local|exp_time"}
}
```
然后在调用`msg_to_pydantic_model`方法时通过参数`local_dict`注册对应的值，伪代码如下：
```Python
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

#### 2.2.4.4.`p2p@builtin`模板
当需要使用的变量来自于内建函数时，可以直接使用该变量（可以认为是`p2p@local`的简化版本），语法使用如下：
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"type": "p2p@builtin|float"}
}
```
生成的`pydantic.BaseModel`对象如下：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.2.4.5.自定义模板
目前`protobuf_to_pydantic`只支持几种模板，如果有更多的模板需求，可以通过继承`DescTemplate`类来对模板进行拓展。
比如有一个奇葩的需求，要求字段的默认值为Message对象生成为`pydantic.BaseModel`对象时的时间戳，不过时间戳有10位和13位两个版本, 于是编写如下Protobuf文件：
```protobuf
message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default = "p2p@timestamp|13"];
}
```
这个文件使用了`p2p@timestamp|{x}`的语法，其中`x`只有10和13两个值，接下来就可以根据这个模板行为编写代码了，代码如下:
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
代码中创建了一个继承于`DescTemplate`的`CustomDescTemplate`的类，这个类新增了一个`template_timestamp`的方法用于匹配`p2p@timestamp`模板，
然后在`msg_to_pydantic_model`中通过`desc_template`关键参数来指定`CustomDescTemplate`模板类，这样`msg_to_pydantic_model`就会生成如下代码(假设在时间戳为1600000000时生成的代码)：
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```

## 2.3.生成对应的Python代码
除了在运行时生成对应的`pydantic.BaseModel`对象外，`protobuf_to_pydantic`支持将运行时的`pydantic.BaseModel`对象转换为`Python`代码文本（仅适用于`protobuf_to_pydantic`生成的`pydantic.BaseModel`对象)。

其中，`protobuf_to_pydantic.pydantic_model_to_py_code`用于生成代码文本，`protobuf_to_pydantic.pydantic_model_to_py_file`用于生成代码文件，`protobuf_to_pydantic.pydantic_model_to_py_file`的示例代码如下：

```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
需要注意的是，如果`protobuf_to_pydantic`检查当前环境安装了`isort`和`autoflake`，默认会通过它们格式化代码。

## 3.example
`protobuf_to_pydantic`提供了一些简单的示例代码，以下是示例代码和protobuf文件的路径，仅供参考:

|说明|Protobuf路径|示例代码|
| ---- | ---- | ---- |
|基于p2p模式生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/p2p_validate|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/p2p_validate_example|
|生成最基础的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/simple_example|
|通过.pyi文件生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/text_comment_example|
|通过protobuf文件生成带有校验规则的Model代码|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/validate|https://github.com/so1n/protobuf_to_pydantic/tree/master/example/validate_example|
