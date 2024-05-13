def pytest_itemcollected(item):
    parent = item.parent.obj
    node = item.obj
    parent_name = parent.__doc__.strip() if parent and parent.__doc__ else parent.__class__.__name__
    node_name = node.__doc__.strip() if node.__doc__ else node.__name__
    if parent_name or node_name:
        item._nodeid = ' '.join((parent_name or '', node_name or ''))
