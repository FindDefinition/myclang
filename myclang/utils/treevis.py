"""copy from codeai.core.dump.tree
"""
from typing import Generic, TypeVar, Any, Callable, List, Iterable
import io

_T = TypeVar("_T")


class TreeDumpStatus(Generic[_T]):
    def __init__(self, node: _T, indent: int, depth: int, direct_prefix: str,
                 child_prefixes: List[str]):
        self.node = node
        self.indent = indent
        self.depth = depth
        # node prefix: "".join(child_prefixes[:-1]) + direct_prefix
        self.direct_prefix = direct_prefix
        self.child_prefixes = child_prefixes

    def get_prefix(self):
        return "".join(self.child_prefixes[:-1]) + self.direct_prefix


def tree_dumps(node: _T,
               printer: Callable[[_T], str],
               getchild: Callable[[_T], Iterable[_T]],
               indent: int = 2,
               start_indent=0,
               max_depth=9999,
               tree_formatter=lambda x: x) -> str:
    ss = io.StringIO()
    q = [TreeDumpStatus(node, start_indent, 0, "",
                        [])]  # type: List[TreeDumpStatus]
    while q:
        status = q.pop()
        cur_node = status.node
        ind = status.indent
        if status.depth >= max_depth:
            continue
        cu_str = printer(cur_node)
        print(tree_formatter(status.get_prefix()) + cu_str, file=ss)
        nexts = []
        childs = list(getchild(cur_node))
        for i, c in enumerate(childs):
            direct_prefix = "|-"
            child_prefixes = status.child_prefixes + ["| "]
            if i == len(childs) - 1:
                direct_prefix = "`-"
                child_prefixes = status.child_prefixes + ["  "]
            next_status = TreeDumpStatus(c, ind + indent, status.depth + 1,
                                         direct_prefix, child_prefixes)
            nexts.append(next_status)
        q.extend(nexts[::-1])
    return ss.getvalue()
