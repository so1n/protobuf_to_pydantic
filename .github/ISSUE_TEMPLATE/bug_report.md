---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.


**Dependencies**

> Input cmd:
> ```bash
> python -m protobuf_to_pydantic --info
> # OR
> python -m protobuf_to_pydantic.plugin --info
> ```

> Result:
> ```bash
> # Paste the output of the command here
> ```

**Protobuf File Content**

> Please check the Protobuf content for sensitive information

> Example:
> Filename: `path1/demo1.proto`
> ```protobuf
> package demo1;
>
> message Demo1{};
> ```
>
> Filename: `path2/demo2.proto`
> ```protobuf
> package demo2;
>
> message Demo2{};
> ```

**CLI(if use plugin mode)**
> Example:
> ```bash
> python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
> ```

**Output content**

> Example:
> Filename: `path1/demo1.p2p`
> ```python
> class Demo1(BaseModel):
>     pass
> ```
>
> Filename: `path2/demo2.p2p`
> ```python
> class Demo2(BaseModel):
>     pass
> ```



**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.
