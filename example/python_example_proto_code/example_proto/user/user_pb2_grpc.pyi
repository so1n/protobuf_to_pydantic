"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import example_proto.user.user_pb2
import google.protobuf.empty_pb2
import grpc

class UserStub:
    """pait: {"group": "user", "tag": [["grpc-user", "grpc_user_service"]]}"""

    def __init__(self, channel: grpc.Channel) -> None: ...
    get_uid_by_token: grpc.UnaryUnaryMultiCallable[
        example_proto.user.user_pb2.GetUidByTokenRequest, example_proto.user.user_pb2.GetUidByTokenResult
    ]
    """The interface should not be exposed for external use
    pait: {"enable": false}
    """

    logout_user: grpc.UnaryUnaryMultiCallable[
        example_proto.user.user_pb2.LogoutUserRequest, google.protobuf.empty_pb2.Empty
    ]
    """pait: {"summary": "User exit from the system", "url": "/user/logout"}"""

    login_user: grpc.UnaryUnaryMultiCallable[
        example_proto.user.user_pb2.LoginUserRequest, example_proto.user.user_pb2.LoginUserResult
    ]
    """pait: {"summary": "User login to system", "url": "/user/login"}"""

    create_user: grpc.UnaryUnaryMultiCallable[
        example_proto.user.user_pb2.CreateUserRequest, google.protobuf.empty_pb2.Empty
    ]
    """pait: {"tag": [["grpc-user", "grpc_user_service"], ["grpc-user-system", "grpc_user_service"]]}
    pait: {"summary": "Create users through the system", "url": "/user/create"}
    """

    delete_user: grpc.UnaryUnaryMultiCallable[
        example_proto.user.user_pb2.DeleteUserRequest, google.protobuf.empty_pb2.Empty
    ]
    """pait: {"url": "/user/delete", "tag": [["grpc-user", "grpc_user_service"], ["grpc-user-system", "grpc_user_service"]]}
    pait: {"desc": "This interface performs a logical delete, not a physical delete"}
    """

class UserServicer(metaclass=abc.ABCMeta):
    """pait: {"group": "user", "tag": [["grpc-user", "grpc_user_service"]]}"""

    @abc.abstractmethod
    def get_uid_by_token(
        self,
        request: example_proto.user.user_pb2.GetUidByTokenRequest,
        context: grpc.ServicerContext,
    ) -> example_proto.user.user_pb2.GetUidByTokenResult:
        """The interface should not be exposed for external use
        pait: {"enable": false}
        """
        pass
    @abc.abstractmethod
    def logout_user(
        self,
        request: example_proto.user.user_pb2.LogoutUserRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty:
        """pait: {"summary": "User exit from the system", "url": "/user/logout"}"""
        pass
    @abc.abstractmethod
    def login_user(
        self,
        request: example_proto.user.user_pb2.LoginUserRequest,
        context: grpc.ServicerContext,
    ) -> example_proto.user.user_pb2.LoginUserResult:
        """pait: {"summary": "User login to system", "url": "/user/login"}"""
        pass
    @abc.abstractmethod
    def create_user(
        self,
        request: example_proto.user.user_pb2.CreateUserRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty:
        """pait: {"tag": [["grpc-user", "grpc_user_service"], ["grpc-user-system", "grpc_user_service"]]}
        pait: {"summary": "Create users through the system", "url": "/user/create"}
        """
        pass
    @abc.abstractmethod
    def delete_user(
        self,
        request: example_proto.user.user_pb2.DeleteUserRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty:
        """pait: {"url": "/user/delete", "tag": [["grpc-user", "grpc_user_service"], ["grpc-user-system", "grpc_user_service"]]}
        pait: {"desc": "This interface performs a logical delete, not a physical delete"}
        """
        pass

def add_UserServicer_to_server(servicer: UserServicer, server: grpc.Server) -> None: ...
