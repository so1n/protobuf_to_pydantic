# protobuf_to_pydantic
Generate a `pydantic.BaseModel` with parameter verification function from the `Python` Message object(by the Protobuf file).

> NOTE:
>  - Only supports proto3
>
>  - The project is from [pait](https://github.com/so1n/pait) separated，Therefore, this project also generates the `pydantic.BaseModel` object in memory first, and then generates the corresponding `Python` code according to the generated object.

[中文文档](https://github.com/so1n/protobuf_to_pydantic/blob/master/README_ZH.md)
# 1.Installation
```bash
pip install protobuf_to_pydantic
```

# 2.Quick Start
## 2.1.Generate a `pydantic.BaseModel` object at runtime
`protobuf_to_pydantic` can generate the corresponding `pydantic.BaseModel` object based on the `Message` object at runtime。

For example, the `UserMessage` in the Protobuf file below：
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
`protobuf_to_pydantic` can read the Message object generated from the Proto file at runtime and generate the corresponding `pydantic.BaseModel` object:
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
## 2.2.Parameter verification
The `Message` object generated according to the Protobuf file only carries a small amount of information, and there is not enough information to make the generated `pydantic.BaseModel` have more detailed parameter verification functions, and some additional ways are needed to improve the data of the `Message` object.
At present, `protobuf_to_pydantic` supports multiple ways to obtain other information of Message, so that the generated `pydantic.BaseModel` object has the function of parameter verification.

> NOTE: P2P mode is recommended
### 2.2.1.Text annotation
Developers can write comments that meet the requirements of `protobuf_to_pydantic` for each field in the Protobuf file to provide parameter verification information for `protobuf_to_pydantic`, such as the following example:
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
In this example, each annotation that can be used by `protobuf_to_pydantic` starts with `p2p:` (supports customization) and is followed by a complete Json string. If you are familiar with the usage of `pydantic`, you can find This Json string contains the verification information corresponding to `pydantic.Field`. For example, the `uid` field in `UserMessage` contains a total of 4 pieces of information as follows：

| Column       | Meaning                                                                               |
|--------------|---------------------------------------------------------------------------------------|
| miss_default | Indicates that the generated field does not have a default value                      |
| example      | An example value representing the generated field is 10086                            |
| title        | Indicates that the schema name of the field is UID                                    |
 | description  | The schema documentation for the representation field is described as `user_union_id` |

> Note:
>   - 1.Currently only single-line comments are supported and comments must be a complete Json data (no line breaks).
>   - 2.multi line comments are not supported。

When these annotations are written, `protobuf_to_pydantic` will bring the corresponding information for each field when converting the Message into the corresponding `Pydantic.BaseModel` object, as follows:
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
It can be seen from the output results that the output fields carry the corresponding information. In addition, the difference between this code and the above is that the `msg_to_pydantic_model` function sets a keyword parameter named `parse_msg_desc_method` and its value is `demo_pb2`, which enables `protobuf_to_pydantic` to obtain additional information for each field in the Message object through comments in the `.pyi` file of the `demo_pb2` module.

> Note：This function requires the use of the [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf) plugin when generating the corresponding `Python` code from the Protobuf file, and the specified output path of the pyi file is the same as the generated `Python` code path to take effect at the same time.

In addition to obtaining comments through the `.pyi` file, `protobuf_to_pydantic` also supports setting the value of `parse_msg_desc_method` to the root directory path specified when the Message object is generated, so that `protobuf_to_pydantic` can parse the comments of the Protobuf file corresponding to the Message object. getting information。


For example, the project structure of `protobuf_to_pydantic` is as follows:
```bash
./protobuf_to_pydantic/
├── example/
│ ├── python_example_proto_code/
│ └── example_proto/
├── protobuf_to_pydantic/
└── /
```
The protobuf file is stored in the `example/example_proto` file, and then the `Python` code file corresponding to protobuf is generated by the following command in the `example` directory:
```bash
cd example

python -m grpc_tools.protoc
  --python_out=./python_example_proto_code \
  --grpc_python_out=./python_example_proto_code \
  -I. \
```
Then the path to be filled in at this time is `./protobuf_to_pydantic/example`, the code is as follows：
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
From the result, it can be seen that the information carried by the field is the same as the result obtained by the module
> NOTE: This method requires [lark](https://github.com/lark-parser/lark) to be installed in advance and the Protobuf file must exist in the running project.

### 2.2.2.PGV
At present, the verification method of Protobuf-generated objects that is widely used is to directly use the [protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate) project, so that the generated Message object has parameter verification logic.
However, the implementation of `Pgv` in `Python` is quite special. It checks all possibilities every time it checks, so the performance is not very good, and the `pydantic.BaseModel` object generated by `protobuf_to_pydantic` itself It is allowed to carry some verification logic and most of the built-in verification logic is written in C, and the performance is relatively high.

`protobuf_to_pydantic` supports parsing the `Pgv` verification information carried by each field in the Protobuf file so that the generated `pydantic.BaseModel` carries the verification logic corresponding to `Pgv`。

It is very simple to use `Pgv` check rules in `protobuf_to_pydantic`, as long as you write the corresponding `Pgv` rules in the Protobuf file, and then specify the value of `parse_msg_desc_method` as `PGV`, the code is as follows：
```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.validate import demo_pb2

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
>  - 1.For the usage of `Pgv`, see: [protoc-gen-validate doc](https://github.com/envoyproxy/protoc-gen-validate/blob/main/README.md)
>  - 2.Need to install `Pgv` through `pip install protoc_gen_validate` Or download [validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto) to the protobuf directory in the project to write pgv rules in the Protobuf file.


### 2.2.3.P2p
The verification rules of `Pgv` are written in the Option attribute of each field of `Message`, and there are better code specifications, so the readability of Protobuf files carrying `Pgv` verification rules is higher than that of Protobuf carrying comments At the same time, when writing `Pgv` rules, you can also experience the convenience brought by IDE auto-completion, but it only supports verification-related logic, and the feature richness is not as good as the file comment mode.

The `P2P` mode combines the advantages of the `PGV` mode and the file comment mode. This mode satisfies most of the attribute customization of each `Field` in the `pydantic.BaseModel`, such as the following Protobuf file:
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
`protobuf_to_pydantic` can read the generated Message object at runtime and generate a `pydantic.BaseModel` object with the corresponding information:
```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel, confloat
from pydantic.fields import FieldInfo

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.p2p_validate import demo_pb2


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
It is worth noting that this code does not explicitly specify that the value of `parse_msg_desc_method` is `p2p`, because `p2p` is already the default rule of `protobuf_to_pydantic`.

> Note: See the template chapter for the usage of `local_dict`

 > Note:
>  - 1.See the template chapter for the usage of `local_dict`
>  - 2.If the reference to the Proto file fails, you need to download [p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/p2p_validate/p2p_validate.proto) in the project and use it in the Protobuf file。




### 2.2.3.Other parameter support
In addition to the parameters of `FieldInfo`, the file comment mode and `p2p` mode of `protobuf_to_pydantic` also support the following parameters:
- miss_default：By default, the default values generated for each field in the `pydantic.BaseModel` object are the same as the default values for each field in the Message. However, you can cancel the default value setting by setting `miss default` to `true`. It should be noted that when `miss default` is set to `true`, the `default` parameter will be invalid.。
- enable: By default, `pydantic.BaseModel` will convert every field in the Message. If some fields do not want to be converted, you can set `enable` to `false`
- const: Specifies the value of the field's constant. Note: The const of `pydantic.BaseModel` only supports bool variables. When `const` is `True`, the accepted value can only be the value set by `default`, and the default value carried by the Message generated by protobuf corresponds to The null value of type does not match `pydantic.BaseModel`, so `protobuf_to_pydantic` makes some changes to the input of this value, but after `const` sets the value, the `cost` property in the generated field is `True` `, and `default` becomes the corresponding value of the setting.
- type: To expand the current type, for example, if you want to increase the verification of the bank card number through the `pydantic.types.Payment Card Number` type, you can specify the field type as `Payment Card Number` by the following method:
  ```protobuf
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  ```

> Note:
>   If you don't know `pydantic`, you can use the following two URLs to learn what parameters Field supports:
>
>   - https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
>
>   - https://pydantic-docs.helpmanual.io/usage/schema/#field-customization

### 2.2.4.Template
In some cases, the value we fill in is a method or function of a library, such as the value of the `type` parameter and the `default_factory` parameter, but it cannot be implemented through Json syntax. In this case, template parameters can be used. Currently, `protobuf_to_pydantic` supports a variety of template parameters.

#### 2.2.4.1.`p2p@import`
This template is used to import variables under other modules. The specific usage is as follows:
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
The syntax used here is the format of `{p2p method}|{imported class:A}|{class module:B}`, where the method `p2p@import` at the beginning indicates that it needs to pass `from A import B` introduces the `B` object. Through the definition of the template, `protobuf_to_pydantic` will convert the corresponding Message to the following `pydantic.BaseModel`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.2.4.2.`p2p@import_instance`
`p2p@import` is just to import the variables of a certain library, and `p2p@import_instance` is to import the class of a certain library first, and then instantiate it with the specified parameters. The usage is as follows:
```protobuf
message AnyTest {
  google.protobuf.Any default_test = 23 [
    (p2p_validate.rules).any.default = 'p2p@import_instance|google.protobuf.any_pb2|Any|{"type_url": "type.googleapis.com/google.protobuf.Duration"}'

  ];
}
```
Here is the `{p2p method}|{module to be imported}|{corresponding class}|{corresponding parameter}` syntax, through the definition of the template, `protobuf_to_pydantic` will convert the corresponding Message is the following `pydantic.BaseModel` object:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
    )
```

#### 2.2.4.3.`p2p@local`
This template is used to introduce user-defined variables. Here, the syntax of the `{p2p method}|{local variable to be used}` format is used, as follows:
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"default_factory": "p2p@local|exp_time"}
}
```
Then register the corresponding value through the parameter `local_dict` when calling the `msg_to_pydantic_model` method. The fake code is as follows:
```Python
def exp_time() -> float:
  return time.time()

msg_to_pydantic_model(
    demo_pb2.NestedMessage,
    local_dict={"exp_time": exp_time},  # <----
)
```
In this way, `protobuf_to_pydantic` can generate a `pydantic.BaseModel` object that meets the requirements:
```python
from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from . import exp_time

class UserPayMessage(BaseModel):
    exp: datetime = FieldInfo(default_factory=exp_time, extra={})
```

> Note: See the sample code for specific calling and generation methods.

#### 2.2.4.4.`p2p@builtin`
When the variable to be used comes from a built-in function, the variable can be used directly (it can be considered as a simplified version of `p2p@local`), the syntax is as follows:
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"type": "p2p@builtin|float"}
}
```
The generated `pydantic.BaseModel` object is as follows:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.2.4.5.Custom template
Currently, `protobuf_to_pydantic` only supports several templates. If you have more template requirements, you can extend the template by inheriting the `DescTemplate` class.
For example, there is a strange requirement that the default value of the field is the timestamp when the Message object is generated as a `pydantic.BaseModel` object, but the timestamp has two versions, one version has a timestamp of length 10 and the other has a length of 13, so write the following Protobuf file:
```protobuf
message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default = "p2p@timestamp|13"];
}
```
This file uses the syntax of `p2p@timestamp|{x}`, where `x` has only two values 10 and 13, and then you can write code according to this template behavior, the code is as follows:
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
The code creates a `CustomDescTemplate` class that inherits from `DescTemplate`, this class adds a `template_timestamp` method to match the `p2p@timestamp` template, and then passes the `desc_template` key parameter in `msg_to_pydantic_model` to specify the template class to use as `CustomDescTemplate`, so that `msg_to_pydantic_model` will generate the following code (assuming the code generated when the timestamp is 1600000000):
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```

## 2.3.Generate the corresponding Python code
In addition to generating corresponding `pydantic.BaseModel` objects at runtime, `protobuf_to_pydantic` supports converting `pydantic.BaseModel` objects to `Python` code at runtime (only for `protobuf_to_pydantic` generation `pydantic.BaseModel` object).

Among them, `protobuf_to_pydantic.pydantic_model_to_py_code` is used to generate the code text, `protobuf_to_pydantic.pydantic_model_to_py_file` is used to generate the code file, and the example code of `protobuf_to_pydantic.pydantic_model_to_py_file` as follows:
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.python_example_proto_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
Note that if `protobuf_to_pydantic` checks that the current environment has `isort` and `autoflake` installed, they will be used to format code by default.

## 3.example
`protobuf_to_pydantic` provides some simple sample code, the following is the path of the sample code and protobuf file, just for reference:

| Implication                           | Example Protobuf                                                                            | Example code                                                                         |
|------------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Generate Model code with validation rules based on p2p schema | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/p2p_validate | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/p2p_validate_example |
| Generate the basic Model code               | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo         | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/simple_example      |
| Generate Model code with validation rules from .pyi files     | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo         | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/text_comment_example |
| Generate Model code with validation rules from protobuf files | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/validate     | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/validate_example    |
