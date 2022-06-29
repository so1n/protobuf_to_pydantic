# protobuf_to_pydantic
将Protobuf文件生成的`Python` Message对象转为带有参数校验功能的`pydantic.BaseModel`对象。

> NOTE: Only support proto3

# 1.安装
```bash
pip install protobuf_to_pydantic
```

# 2.使用方法
## 2.1.运行时转换对象
`protobuf_to_pydantic` 可以在运行时根据`Message`对象生成对应的 `pydantic.BaseModel`对象。

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
`protobuf_to_pydantic`可以在运行时读取生成的Message对象，并转换为对应的`pydantic.BaseModel`对象:
```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.demo import demo_pb2


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
## 2.2.校验
根据protobuf文件生成的`Message`对象只携带少量的信息，没有足够的信息使生成的`pydantic.BaseModel`具有更加详细的参数验证功能，需要一些拓展途径来完善`Message`对象的数据。
目前`protobuf_to_pydantic`通过三种方式来获取Message的其他信息，使得生成的`pydantic.Base_Model`对象具有参数校验的功能。

### 2.2.1.文本注释
使用者可以在protobuf文件中为每个字段编写符合`protobuf_to_pydantic`要求的注释来为`protobuf_to_pydantic`提供参数校验信息，比如下面这个例子
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
在这个例子中，每个可以被`protobuf_to_pydantic`使用的注释都是以`p2p:`开头，并在后面跟着一个完整的Json字符串，如果熟悉`pydantic`的用法的话，可以发现这个Json字符串包含的都是对应字段的校验信息，
比如`UserMessage`中的uid附带了如下4个信息：
- miss_default: 表示生成的字段不带有默认值
- example: 表示生成的字段的示例值为10086
- title: 表示字段的名称为UID
- description: 表示字段的文档描述为`user union id`

> Note:
>   - 1.目前只支持单行注释且注释必须是一个完整的Json数据(不能换行)。
>   - 2.不支持多行注释。

当编写了这些注释后，`protobuf_to_pydantic`在把Message转换成对应的`Pydantic.BaseModel`对象时都会为每个字段带上对应的信息，如下:
```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.demo import demo_pb2

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

#### 2.2.1.1.By pyi file
由于`Python`中负责把protobuf文件转为`Python`代码时并不会把Message的注释带到生成的`Python`代码中，所以上面的示例会把Message对象所属的模块传入`parse_msg_desc_method`中，
使得`protobuf_to_pydantic`可以通过读取Message对应的pyi文件的注释来获取Message对象的附加信息。

> 注：该功能需要在通过Protobuf文件生成对应的`Python`代码时使用[mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf)插件，且指定的pyi文件输出路径与生成的`Python`代码路径时，才能生效

#### 2.2.1.1.By Protobuf file
如果生成Message的原始Protobuf文件存在与项目中， 那么可以设置`parse_msg_desc_method`的值为Message生成时指定的根目录路径，
这样`protobuf_to_pydantic`就可以通过Protobuf生成对应`Python`对象时指定的路径来获取到Message对象的protobuf文件路径，再通过解析protobuf文件的注释获取到Message的附带信息。

比如`protobuf_to_pydantic`的项目结构如下:
```bash
.protobuf_to_pydantic/
├── example/
│ ├── python_example_proto_code/
│ └── example_proto/
├── protobuf_to_pydantic/
└── /
```
其中protobuf文件存放在`example/example_proto`文件中，然后在`example`目录下通过如下命令生成protobuf对应的`Python`代码文件:
```bash
python -m grpc_tools.protoc
  --python_out=./python_example_proto_code \
  --grpc_python_out=./python_example_proto_code \
  -I. \
```
那么此时需要填写的路径就是`./protobuf_to_pydantic/example`。
```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.demo import demo_pb2

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

### 2.2.2.Protobuf Field Option(PGV)

> Note 正在开发中...

这是最推荐的方式，该方式参考了[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目，大多数Protobuf文件API参考了[protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate)项目

### 2.2.3.其它参数支持
`protobuf_to_pydantic`除了支持`FieldInfo`的参数外，还支持下面几种参数:
- miss_default：默认情况下，生成对应`pydantic.BaseModel`对象中每个字段的默认值与Message中每个字段的默认值是一样的。不过可以通过设置`miss_default`为`true`来取消默认值的设置，需要注意的是在设置`miss_default`为`true`的情况下，`default`参数将失效。
- enable: 默认情况下， `pydantic.BaseModel`会把Message中的每个字段都进行转换，如果有些字段不想被转换，可以设置`enable`为`false`

> Note `FieldInfo`支持的参数见:https://pydantic-docs.helpmanual.io/usage/types/#constrained-types


## 2.3.生成对应的Python代码
除了在运行时生成对应的`pydantic.BaseModel`对象外，`protobuf_to_pydantic`支持将运行时`pydantic.BaseModel`对象转换为`Python`代码文本（仅适用于`protobuf to pydantic`生成的`pydantic .Base Model`对象)。

其中，`protobuf_to_pydantic.pydantic_model_to_py_code`用于生成代码文本，`protobuf_to_pydantic.pydantic_model_to_py_file`用于生成代码文件，`protobuf_to_pydantic.pydantic_model_to_py_file`的示例如下：
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.demo import demo_pb2

# gen code: url: https://github.com/so1n/protobuf_to_pydantic/blob/master/example/demo_gen_code.py
pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)

# gen code: url: https://github.com/so1n/protobuf_to_pydantic/blob/master/example/demo_gen_code_by_pyi.py
pydantic_model_to_py_file(
    "./demo_gen_code_by_pyi.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage, parse_msg_desc_method=demo_pb2),
)

# gen code: url: https://github.com/so1n/protobuf_to_pydantic/blob/master/example/demo_gen_code_by_protobuf_field.py
pydantic_model_to_py_file(
    "./demo_gen_code_by_protobuf_field.py",
    msg_to_pydantic_model(
        demo_pb2.NestedMessage, parse_msg_desc_method="/home/so1n/github/protobuf_to_pydantic/example"
    ),
)
```
具体生成的代码可以通过对应的url查看。需要注意的是，如果`protobuf_to_pydantic`检查当前环境安装了`isort`和`autoflake`，默认会通过它们格式化代码。
