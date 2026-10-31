"""Windows Credential Manager generic credentials. No plaintext tokens in workspace."""
import ctypes
import getpass
import os
from ctypes import wintypes

TARGET = "WORKSHOP_DESKTOP_V1_GITHUB"
SIGNING = "WORKSHOP_DESKTOP_V1_APPROVAL_KEY"


def _allowed(name):
    return name in (TARGET, SIGNING) or (isinstance(name, str) and name.startswith("WORKSHOP_DESKTOP_V1_TEST_") and len(name) <= 100)


class VaultError(RuntimeError):
    pass


class WindowsVault:
    def __init__(self):
        if os.name != "nt":
            raise VaultError("WINDOWS_CREDENTIAL_MANAGER_REQUIRED")

    @staticmethod
    def _types():
        class CREDENTIAL(ctypes.Structure):
            _fields_ = [("Flags", wintypes.DWORD), ("Type", wintypes.DWORD),
                        ("TargetName", wintypes.LPWSTR), ("Comment", wintypes.LPWSTR),
                        ("LastWritten", wintypes.FILETIME), ("CredentialBlobSize", wintypes.DWORD),
                        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)), ("Persist", wintypes.DWORD),
                        ("AttributeCount", wintypes.DWORD), ("Attributes", ctypes.c_void_p),
                        ("TargetAlias", wintypes.LPWSTR), ("UserName", wintypes.LPWSTR)]
        return CREDENTIAL

    def put(self, name, value):
        if not _allowed(name) or not isinstance(value, str):
            raise VaultError("INVALID_CREDENTIAL")
        raw = value.encode("utf-8")
        if not raw or len(raw) > 2048:
            raise VaultError("CREDENTIAL_SIZE")
        credential_type = self._types()
        blob = (ctypes.c_ubyte * len(raw)).from_buffer_copy(raw)
        credential = credential_type()
        credential.Type = 1  # CRED_TYPE_GENERIC
        credential.TargetName = name
        credential.CredentialBlobSize = len(raw)
        credential.CredentialBlob = ctypes.cast(blob, ctypes.POINTER(ctypes.c_ubyte))
        credential.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
        credential.UserName = getpass.getuser()
        advapi = ctypes.WinDLL("Advapi32", use_last_error=True)
        write = advapi.CredWriteW
        write.argtypes = (ctypes.POINTER(credential_type), wintypes.DWORD)
        write.restype = wintypes.BOOL
        if not write(ctypes.byref(credential), 0):
            raise VaultError("CREDENTIAL_WRITE_FAILED")

    def get(self, name):
        if not _allowed(name):
            raise VaultError("INVALID_CREDENTIAL")
        credential_type = self._types()
        pointer = ctypes.POINTER(credential_type)()
        advapi = ctypes.WinDLL("Advapi32", use_last_error=True)
        read = advapi.CredReadW
        read.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                         ctypes.POINTER(ctypes.POINTER(credential_type)))
        read.restype = wintypes.BOOL
        if not read(name, 1, 0, ctypes.byref(pointer)):
            if ctypes.get_last_error() == 1168:
                return None
            raise VaultError("CREDENTIAL_READ_FAILED")
        try:
            data = ctypes.string_at(pointer.contents.CredentialBlob, pointer.contents.CredentialBlobSize)
            return data.decode("utf-8")
        finally:
            advapi.CredFree.argtypes = (ctypes.c_void_p,)
            advapi.CredFree(pointer)

    def delete(self, name):
        if not _allowed(name):
            raise VaultError("INVALID_CREDENTIAL")
        advapi = ctypes.WinDLL("Advapi32", use_last_error=True)
        delete = advapi.CredDeleteW
        delete.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD)
        delete.restype = wintypes.BOOL
        if not delete(name, 1, 0) and ctypes.get_last_error() != 1168:
            raise VaultError("CREDENTIAL_DELETE_FAILED")


class MemoryVault:
    """Non-persistent test fixture; never used for customer secrets."""
    def __init__(self):
        self.data = {}

    def put(self, name, value):
        self.data[name] = value

    def get(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)
