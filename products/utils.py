from typing import List, Dict
from django.db.models import Q


def build_icontains_query(fields: List[str], search_query: str) -> Q:
    """
    Build a Q object for icontains search across multiple fields.
    """
    q = Q()
    for field in fields:
        q |= Q(**{f"{field}__icontains": search_query})
    return q
