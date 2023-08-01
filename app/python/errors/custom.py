import typing
from anchorpy.error import ProgramError


class InvalidAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Invalid authority")

    code = 6000
    name = "InvalidAuthority"
    msg = "Invalid authority"


class MathOverflow(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Overflow in arithmetic operation")

    code = 6001
    name = "MathOverflow"
    msg = "Overflow in arithmetic operation"


class InvalidGroupState(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Invalid group state")

    code = 6002
    name = "InvalidGroupState"
    msg = "Invalid group state"


class InvalidProtocolConfig(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Invalid protocol config")

    code = 6003
    name = "InvalidProtocolConfig"
    msg = "Invalid protocol config"


class InvalidGroupConfig(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Invalid group config")

    code = 6004
    name = "InvalidGroupConfig"
    msg = "Invalid group config"


class InvalidParticipantConfig(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Invalid participant config")

    code = 6005
    name = "InvalidParticipantConfig"
    msg = "Invalid participant config"


class InvalidGroupAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Invalid group address")

    code = 6006
    name = "InvalidGroupAddress"
    msg = "Invalid group address"


class InvalidCustodyAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Invalid custody address")

    code = 6007
    name = "InvalidCustodyAddress"
    msg = "Invalid custody address"


class InstructionNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Instruction is not allowed at this time")

    code = 6008
    name = "InstructionNotAllowed"
    msg = "Instruction is not allowed at this time"


class InvalidEnvironment(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Instruction is not allowed in production")

    code = 6009
    name = "InvalidEnvironment"
    msg = "Instruction is not allowed in production"


CustomError = typing.Union[
    InvalidAuthority,
    MathOverflow,
    InvalidGroupState,
    InvalidProtocolConfig,
    InvalidGroupConfig,
    InvalidParticipantConfig,
    InvalidGroupAddress,
    InvalidCustodyAddress,
    InstructionNotAllowed,
    InvalidEnvironment,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InvalidAuthority(),
    6001: MathOverflow(),
    6002: InvalidGroupState(),
    6003: InvalidProtocolConfig(),
    6004: InvalidGroupConfig(),
    6005: InvalidParticipantConfig(),
    6006: InvalidGroupAddress(),
    6007: InvalidCustodyAddress(),
    6008: InstructionNotAllowed(),
    6009: InvalidEnvironment(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
