import re

def humanize_view_name(name: str) -> str:
    """
    Convert a Django view name into a readable title.
    Example: "truck_list" → "Truck List"
             "purchase_order_detail" → "Purchase Order Detail"
    """
    return re.sub(r'[_-]+', ' ', name).title()

def page_title(request):
    try:
        view_name = request.resolver_match.view_name  # from urls.py
    except AttributeError:
        view_name = None

    default_title = "RF Dispatch"

    if not view_name:
        return {"page_title": default_title}

    # Auto-generate title
    title = humanize_view_name(view_name)

    return {"page_title": f"{title} - RF Dispatch"}
