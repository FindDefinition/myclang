from myclang.cext import clcompiler
import multiprocessing
from ccimport import compat 
from typing import List 

def _run_func(target, args, kwargs, q):
    if kwargs is None:
        kwargs = {}
    try:
        res = target(*args, **kwargs)
        q.put((res, None))
    except Exception as e:
        q.put((None, e))


def run_in_process(target, args, kwargs=None, spawn=False):
    method = "spawn" if spawn else "fork"
    if compat.InWindows:
        method = "spawn"
    ctx = multiprocessing.get_context(method)
    q = ctx.Queue()
    p = ctx.Process(target=_run_func, args=(target, args, kwargs, q))
    p.daemon = True
    p.start()
    p.join()
    res, exc = q.get()
    if exc is not None:
        raise exc
    else:
        return res

def clang_format(code: str, *args: str):
    """we need to use process to wrap clangfmt_main_bind
    because llvm append signal handler in every function call.
    """
    (retcode, res) = run_in_process(clcompiler.clangfmt_main_bind, (["-", *args], code))
    ress =  list(res.values())
    if not ress:
        return code
    return ress[0]
