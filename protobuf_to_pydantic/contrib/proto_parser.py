# The original author hasn't updated it for a long time,
# so fork this code and make some optimizations and bug fixes for this project
#
# Original project name: protoparser
# Original project url: https://github.com/khadgarmage/protoparser
# Original project author: khadgarmage
#
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from lark import Lark, Token, Transformer, Tree
from lark.tree import ParseTree  # type: ignore

BNF = r"""
OCTALDIGIT: "0..7"
IDENT: ( "_" )* LETTER ( LETTER | DECIMALDIGIT | "_" )*
FULLIDENT: IDENT ( "." IDENT )*
MESSAGENAME: IDENT
ENUMNAME: IDENT
FIELDNAME: IDENT
ONEOFNAME: IDENT
MAPNAME: IDENT
SERVICENAME: IDENT
TAGNAME: IDENT
TAGVALUE: IDENT
RPCNAME: IDENT
MESSAGETYPE: [ "." ] ( IDENT "." )* MESSAGENAME
ENUMTYPE: [ "." ] ( IDENT "." )* ENUMNAME
INTLIT    : DECIMALLIT | OCTALLIT | HEXLIT
DECIMALLIT: ( "1".."9" ) ( DECIMALDIGIT )*
OCTALLIT  : "0" ( OCTALDIGIT )*
HEXLIT    : "0" ( "x" | "X" ) HEXDIGIT ( HEXDIGIT )*
FLOATLIT: ( DECIMALS "." [ DECIMALS ] [ EXPONENT ] | DECIMALS EXPONENT | "."DECIMALS [ EXPONENT ] ) | "inf" | "nan"
DECIMALS : DECIMALDIGIT ( DECIMALDIGIT )*
EXPONENT : ( "e" | "E" ) [ "+" | "-" ] DECIMALS
BOOLLIT: "true" | "false"
STRLIT: ( "'" ( CHARVALUE )* "'" ) |  ( "\"" ( CHARVALUE )* "\"" )
CHARVALUE: HEXESCAPE | OCTESCAPE | CHARESCAPE |  /[^\0\n\\]/
HEXESCAPE: "\\" ( "x" | "X" ) HEXDIGIT HEXDIGIT
OCTESCAPE: "\\" OCTALDIGIT OCTALDIGIT OCTALDIGIT
CHARESCAPE: "\\" ( "a" | "b" | "f" | "n" | "r" | "t" | "v" | "\\" | "'" | "\"" )
QUOTE: "'" | "\""
EMPTYSTATEMENT: ";"
CONSTANT: FULLIDENT | ( [ "-" | "+" ] INTLIT ) | ( [ "-" | "+" ] FLOATLIT ) | STRLIT | BOOLLIT
syntax: "syntax" "=" QUOTE "proto3" QUOTE ";"
import: "import" [ "weak" | "public" ] STRLIT ";"
package: "package" FULLIDENT ";"
option: "option" OPTIONNAME  "=" CONSTANT ";"
OPTIONNAME: ( IDENT | "(" FULLIDENT ")" ) ( "." IDENT )*
TYPE: "double" | "float" | "int32" | "int64" | "uint32" | "uint64" | "sint32" | "sint64" | "fixed32"
    | "fixed64" | "sfixed32" | "sfixed64" | "bool" | "string" | "bytes" | MESSAGETYPE | ENUMTYPE
FIELDNUMBER: INTLIT
field: [ comments ] TYPE FIELDNAME "=" FIELDNUMBER [ "[" fieldoptions "]" ] TAIL
fieldoptions: fieldoption ( ","  fieldoption )*
fieldoption: OPTIONNAME "=" CONSTANT
repeatedfield: [ comments ] "repeated" field
oneof: "oneof" ONEOFNAME "{" ( oneoffield | EMPTYSTATEMENT )* "}"
oneoffield: TYPE FIELDNAME "=" FIELDNUMBER [ "[" fieldoptions "]" ] ";"
mapfield: [ comments ] "map" "<" KEYTYPE "," TYPE ">" MAPNAME "=" FIELDNUMBER [ "[" fieldoptions "]" ] TAIL
KEYTYPE: "int32" | "int64" | "uint32" | "uint64" | "sint32" | "sint64" | "fixed32" | "fixed64" | "sfixed32"
    | "sfixed64" | "bool" | "string"
reserved: "reserved" ( ranges | fieldnames ) ";"
ranges: range ( "," range )*
range:  INTLIT [ "to" ( INTLIT | "max" ) ]
fieldnames: FIELDNAME ( "," FIELDNAME )*
enum: [ comments ] "enum" ENUMNAME enumbody
enumbody: "{" ( enumfield | EMPTYSTATEMENT )* "}"
enumfield: [ COMMENTS ] IDENT "=" INTLIT [ "[" enumvalueoption ( ","  enumvalueoption )* "]" ] TAIL
enumvalueoption: OPTIONNAME "=" CONSTANT
message: [ comments ] "message" MESSAGENAME messagebody
messagebody: "{" ( repeatedfield | field | enum | message | option | oneof | mapfield | reserved | EMPTYSTATEMENT )* "}"
googleoption: "option" "(google.api.http)"  "=" "{" [ "post:" CONSTANT [ "body:" CONSTANT ] ] "}" ";"
service: [ comments ] "service" SERVICENAME "{" ( option | rpc | EMPTYSTATEMENT )* "}"
rpc: [ comments ] "rpc" RPCNAME "(" [ "stream" ] MESSAGETYPE ")" "returns" "(" [ "stream" ] MESSAGETYPE ")" \
 ( ( "{" ( googleoption | option | EMPTYSTATEMENT )* "}" ) | ";" )
proto:[ comments ] syntax ( import | package | option | topleveldef | EMPTYSTATEMENT )*
topleveldef: message | enum | service | comments
TAIL: ";" [/[\s|\t]/] [ COMMENT ]
COMMENT: "//" /.*/ [ "\n" ]
comments: COMMENT ( COMMENT )*
COMMENTS: COMMENT ( COMMENT )*
%import common.HEXDIGIT
%import common.DIGIT -> DECIMALDIGIT
%import common.LETTER
%import common.WS
%import common.NEWLINE
%ignore WS
"""


@dataclass
class Comment(object):
    content: str
    tags: Dict[str, Any]


@dataclass
class Field(object):
    comment: Comment
    type: str
    key_type: str
    val_type: str
    name: str
    number: int


@dataclass
class Enum(object):
    comment: Comment
    name: str
    fields: Dict[str, Field]


@dataclass
class Message(object):
    comment: Comment
    name: str
    fields: List[Field]
    messages: Dict[str, "Message"]
    enums: Dict[str, Enum]


@dataclass
class RpcFunc(object):
    name: str
    in_type: str
    out_type: str
    uri: str


@dataclass
class Service(object):
    name: str
    functions: List[RpcFunc]


@dataclass
class ProtoFile(object):
    messages: Dict[str, Message]
    enums: Dict[str, Enum]
    services: Dict[str, Service]
    imports: List[str]
    options: Dict[str, str]
    package: str


class ProtoTransformer(Transformer):
    """Converts syntax tree token into more easily usable namedtuple objects"""

    @staticmethod
    def message(tokens: list) -> Message:
        """Returns a Message namedtuple"""
        comment: Comment = Comment("", {})
        if len(tokens) < 3:
            name_token, body = tokens
        else:
            comment, name_token, body = tokens
        return Message(comment, name_token.value, *body)

    @staticmethod
    def messagebody(
        items: List[Union[Message, Enum, Field]]
    ) -> Tuple[List[Field], Dict[str, Message], Dict[str, Enum]]:
        """Returns a tuple of message body namedtuples"""
        messages: Dict[str, Message] = {}
        enums: Dict[str, Enum] = {}
        fields: List[Field] = []
        for item in items:
            if isinstance(item, Message):
                messages[item.name] = item
            elif isinstance(item, Enum):
                enums[item.name] = item
            elif isinstance(item, Field):
                fields.append(item)
        return fields, messages, enums

    @staticmethod
    def field(tokens: list) -> Field:
        """Returns a Field namedtuple"""
        comment: Comment = Comment("", {})
        type_token: Token = Token("TYPE", "")
        field_name_token: Token = Token("FIELDNAME", "")
        field_number_token: Token = Token("FIELDNUMBER", "")
        for token in tokens:
            if isinstance(token, Comment):
                comment = token
            elif isinstance(token, Token):
                if token.type == "TYPE":
                    type_token = token
                elif token.type == "FIELDNAME":
                    field_name_token = token
                elif token.type == "FIELDNUMBER":
                    field_number_token = token
                elif token.type == "COMMENT":
                    if not comment:
                        comment = Comment(token.value, {})
                    else:
                        comment.content += token.value
                elif token.type == "TAIL" and "//" in token.value:
                    value = token.value.strip(";").strip()
                    if not comment:
                        comment = Comment(value, {})
                    else:
                        comment.content += value
        return Field(
            comment,
            type_token.value,
            type_token.value,
            type_token.value,
            field_name_token.value,
            int(field_number_token.value),
        )

    @staticmethod
    def repeatedfield(tokens: list) -> Field:
        """Returns a Field namedtuple"""
        comment: Comment = Comment("", {})
        if len(tokens) < 2:
            field: Field = tokens[0]
        else:
            comment, field = tuple(tokens)
        return Field(comment, "repeated", field.type, field.type, field.name, field.number)

    @staticmethod
    def mapfield(tokens: list) -> Field:
        """Returns a Field namedtuple"""
        comment = Comment("", {})
        val_type = Token("TYPE", "")
        key_type = Token("KEYTYPE", "")
        fieldname = Token("MAPNAME", "")
        fieldnumber = Token("FIELDNUMBER", "")
        for token in tokens:
            if isinstance(token, Comment):
                comment = token
            elif isinstance(token, Token):
                if token.type == "TYPE":
                    val_type = token
                elif token.type == "KEYTYPE":
                    key_type = token
                elif token.type == "MAPNAME":
                    fieldname = token
                elif token.type == "FIELDNUMBER":
                    fieldnumber = token
                elif token.type == "COMMENT":
                    comment = Comment(token.value, {})
        return Field(comment, "map", key_type.value, val_type.value, fieldname.value, int(fieldnumber.value))

    @staticmethod
    def comments(tokens: list) -> Comment:
        """Returns a Tag namedtuple"""
        comment: str = ""
        tags: Dict[str, Any] = {}
        for token in tokens:
            comment += token
            if token.find("@") < 0:
                continue
            kvs = token.strip(" /\n").split("@")
            for kv in kvs:
                kv = kv.strip(" /\n")
                if not kv:
                    continue
                tmp = kv.split("=")
                key = tmp[0].strip(" /\n").lower()
                if key.find(" ") >= 0:
                    continue
                if len(tmp) > 1:
                    tags[key] = tmp[1].lower()
                else:
                    tags[key] = True
        return Comment(comment, tags)

    @staticmethod
    def enum(tokens: list) -> Enum:
        """Returns an Enum namedtuple"""
        comment: Comment = Comment("", {})
        if len(tokens) < 3:
            name, fields = tokens
        else:
            comment, name, fields = tokens
        return Enum(comment, name.value, fields)

    @staticmethod
    def enumbody(tokens: list) -> List[Field]:
        """Returns a sequence of enum identifiers"""
        enumitems: List[Field] = []
        for tree in tokens:
            if tree.data != "enumfield":
                continue
            comment: Comment = Comment("", {})
            name: Token = Token("IDENT", "")
            value: Token = Token("INTLIT", "")
            for token in tree.children:
                if isinstance(token, Comment):
                    comment = token
                elif isinstance(token, Token):
                    if token.type == "IDENT":
                        name = token
                    elif token.type == "INTLIT":
                        value = token
                    elif token.type == "COMMENTS":
                        comment = Comment(token.value, {})
            enumitems.append(Field(comment, "enum", "enum", "enum", name.value, value.value))
        return enumitems

    @staticmethod
    def service(tokens: list) -> Service:
        """Returns a Service namedtuple"""
        functions: List[RpcFunc] = []
        name: str = ""
        for token in tokens:
            if token is None:
                continue
            if not isinstance(token, Comment):
                if isinstance(token, RpcFunc):
                    functions.append(token)
                else:
                    name = token.value
        return Service(name, functions)

    @staticmethod
    def rpc(tokens: List) -> RpcFunc:
        """Returns a RpcFunc namedtuple"""
        uri: str = ""
        name: Token = Token("RPCNAME", "")
        in_type: Token = Token("MESSAGETYPE", "")
        out_type: Token = Token("MESSAGETYPE", "")

        for token in tokens:
            if token is None:
                continue
            if isinstance(token, Token):
                if token.type == "RPCNAME":
                    name = token
                elif token.type == "MESSAGETYPE":
                    if in_type:
                        out_type = token
                    else:
                        in_type = token
            elif not isinstance(token, Comment):
                option_token = token
                uri = option_token.children[0].value
        return RpcFunc(name.value, in_type.value, out_type.value, uri.strip('"'))


def _recursive_to_dict(obj: Any) -> Dict[str, Any]:
    _dict: Dict[str, Any] = {}

    if hasattr(obj, "__dataclass_fields__"):
        node: Dict[str, Any] = asdict(obj)
        for item in node:
            if isinstance(node[item], list):  # Process as a list
                _dict[item] = [_recursive_to_dict(x) for x in (node[item])]
            elif isinstance(node[item], tuple):  # Process as a NamedTuple
                _dict[item] = _recursive_to_dict(node[item])
            elif isinstance(node[item], dict):
                for k in node[item]:
                    if isinstance(node[item][k], tuple):
                        node[item][k] = _recursive_to_dict(node[item][k])
                _dict[item] = node[item]
            else:  # Process as a regular element
                _dict[item] = node[item]
    return _dict


def parse_from_file(file: str) -> Optional[ProtoFile]:
    with open(file, "r") as f:
        data = f.read()
    if data:
        return parse(data)
    return None


def parse(data: str) -> ProtoFile:
    parser: Lark = Lark(BNF, start="proto", parser="lalr")
    tree: ParseTree = parser.parse(data)
    trans_tree: Tree = ProtoTransformer().transform(tree)
    enums: Dict[str, Enum] = {}
    messages: Dict[str, Message] = {}
    services: Dict[str, Service] = {}
    imports: List[str] = []
    options: Dict[str, str] = {}
    package: str = ""

    import_tree = trans_tree.find_data("import")
    for tree in import_tree:
        for child in tree.children:
            imports.append(child.value.strip('"'))

    option_tree = trans_tree.find_data("option")
    for tree in option_tree:
        options[tree.children[0]] = tree.children[1].strip('"')

    package_tree = trans_tree.find_data("package")
    for tree in package_tree:
        package = tree.children[0]

    top_data = trans_tree.find_data("topleveldef")
    for top_level in top_data:
        for child in top_level.children:
            if isinstance(child, Message):
                messages[child.name] = child
            if isinstance(child, Enum):
                enums[child.name] = child
            if isinstance(child, Service):
                services[child.name] = child
    return ProtoFile(messages, enums, services, imports, options, package)


def serialize2json(data: str) -> str:
    return json.dumps(_recursive_to_dict(parse(data)))


def serialize2json_from_file(file: str) -> Optional[str]:
    with open(file, "r") as f:
        data = f.read()
    if data:
        return json.dumps(_recursive_to_dict(parse(data)))
    return None
