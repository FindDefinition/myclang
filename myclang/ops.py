from .betterenums import NodeKind
from . import constants

def nkind_is_decl(nkind: NodeKind):
    K = nkind.value
    return ((K >= constants.CXCURSOR_FIRST_DECL and K <= constants.CXCURSOR_LAST_DECL) or
            (K >= constants.CXCURSOR_FIRST_EXTRA_DECL and K <= constants.CXCURSOR_LAST_EXTRA_DECL) or
            (K >= constants.CXCURSOREX_FIRST_DECL and K <= constants.CXCURSOREX_LAST_DECL))
