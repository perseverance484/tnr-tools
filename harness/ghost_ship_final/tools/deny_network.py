#!/usr/bin/env python3
"""Run an offline harness child with network syscalls denied (no namespace privileges)."""
import ctypes
import errno
import os
import sys

lib = ctypes.CDLL("libseccomp.so.2", use_errno=True)
lib.seccomp_init.argtypes = [ctypes.c_uint32]
lib.seccomp_init.restype = ctypes.c_void_p
lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
lib.seccomp_syscall_resolve_name.restype = ctypes.c_int
lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
lib.seccomp_rule_add.restype = ctypes.c_int
lib.seccomp_load.argtypes = [ctypes.c_void_p]
lib.seccomp_load.restype = ctypes.c_int
lib.seccomp_release.argtypes = [ctypes.c_void_p]
if len(sys.argv) < 2:
    raise SystemExit("usage: deny_network.py COMMAND [ARGS...]")
ctx = lib.seccomp_init(0x7FFF0000)
if not ctx:
    raise RuntimeError("seccomp_init failed")
for name in ("socket", "socketpair", "connect", "bind", "listen", "accept", "accept4",
             "sendto", "sendmsg", "sendmmsg", "io_uring_setup"):
    number = lib.seccomp_syscall_resolve_name(name.encode())
    if number < 0 or lib.seccomp_rule_add(ctx, 0x00050000 | errno.EPERM, number, 0) != 0:
        raise RuntimeError(f"failed to deny {name}")
if lib.seccomp_load(ctx) != 0:
    raise RuntimeError("seccomp_load failed")
lib.seccomp_release(ctx)
# An inherited socket could otherwise use read/write without creating a socket.
# Keep only the three caller-supplied standard streams.
for entry in os.listdir("/proc/self/fd"):
    fd = int(entry)
    if fd >= 3:
        try:
            os.close(fd)
        except OSError as exc:
            if exc.errno != errno.EBADF:
                raise
os.execvp(sys.argv[1], sys.argv[1:])
