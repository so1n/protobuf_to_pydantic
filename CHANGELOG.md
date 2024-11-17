## 0.4[Future]
- Feature, support protovalidate(proto-gen-validate version >= 1.0.0) rule
## 0.3.x[Future]
- CommentHandler
- FormatHandler
## 0.3.0.1[Now]
- Fix, fix pydantic issue 6506
- Fix, fix issue 74
## 0.3
- Note: Template is the introduction method that changes
  - OLD: `from protobuf_to_pydantic.desc_template import DescTemplate`
  - NEW: `from protobuf_to_pydantic.template import Template`

- Feat, Plugin config support pkg config
- Feat, Support all field can be set optional
- Fix, `check_one_of` not support alias field(#67)
- Fix, Fixed the issue that some message references could not be parsed properly
- Refactor, Refactored the internal implementation and changed the directory name(Prepare for version 4.0)

## 0.2.7
- Fix, (#57)
- Feat, Plugin support comment rule
- Test, fix ge le gt lt value

## 0.2.6.2
- Feat, support google.protobuf.xxx message and plugin add protobuf type gen config (#51)

## 0.2.6.1
- Fix, Remove dependency:grpcio-tools and fix dependencies clash with protobuf-5.26.1 (#48)

## 0.2.6
- Fix, fix nested message gen code syntax error (#44)
- Feat, support field mask (#43)

## 0.2.5
- Feat, support `google.protobuf.Struct` (#41)
- Fix, Fix use of `base_model_class` parameter value in code generation (#40)

## 0.2.4
- Fix, fix missing typing import for optional field (#38)
- Feat, py311 support

## 0.2.3
- Feat, add oneof optional support

## 0.2.2
- Feat, add buf-cli support

## 0.2.1
- Feature, support buf-cli
- Feature, Remove redundant parameters in con_type
- Feature, plugin support create dynamic plugin config module
- Build, change requirements and script

## 0.2.0.x(1-4)
- Fix, fix option field has default and default_factory value
- Fix, default factory and default generated together
## 0.2.0
- Feature, support Pydantic Version 2.0.0+
- Feature, datetime compared by timestamp
- Feature, support optional field
- Feature, field add required attr
- Feature, change format feature optional default value
- Feature, p2p rule support default template feature
- Refactor, refactor model's validator code gen(Use Pydantic's validator naming standard)
## 0.1.7
- Fix, fix plugin cli not use param
- Feature, Plugin CodeGen support customer config and support Field config
- Feature, Plugin CodeGen support customer head&tail content
- Feature, Plugin CodeGen support Struct
- Feature, support [after refer Message(#4)](https://github.com/so1n/protobuf_to_pydantic/issues/4) and [Self-referencing Message(#7)](https://github.com/so1n/protobuf_to_pydantic/issues/7)
- Feature, support 3.20.x and 4.20.x Protobuf ([See the differences in versions](https://protobuf.dev/news/2022-05-06/#python-updates))
- Refactor, Enhanced module path matching
- Refactor, format code
  - 1.remove yapf support
  - 2.support format tool load config from pyproject.toml
  - 3.fix parse auto_flake fix_code func param error
## 0.1.6
- Feature, support proto plugin feature

## 0.1
- Feature, add get desc from p2p
- Feature, add DescTemplate class
- Refactor, change pydantic validate param type (datetime -> float)

## 0.0.3
- Feature, add simple get desc from pgv
- Feature, support gpv other validation by pydantic validator
- Feature, Any, Duration, Enum, Timestamp, Repeated, Map and one of support

## 0.0.2
- Fix, fix parse_method_by_protobuf not support TAIL comment
- Feature, support customer field.type and field.default_factory
- Feature, support module path
- Refactor, refactor gen model func -> class
## 0.0.1
 - description: The first version
 - Feature: support gen pydantic.basemodel in runtime
 - Feature: support gen python code from pydantic.basemodel
 - Feature: support parameter verification
