from fabricagent import find_empty_fields


def test_none_blank_and_empty_list():
    value = {
        "InvoiceID": None,
        "DueDate": "   ",
        "Items": [],
        "TotalAmount": 0,
    }
    assert find_empty_fields(value) == ["InvoiceID", "DueDate", "Items"]


def test_nested_item_path():
    value = {"Items": [{"Product": None, "Quantity": 1}]}
    assert find_empty_fields(value) == ["Items[0].Product"]


def test_complete_value():
    value = {"InvoiceID": "INV-001", "Items": [{"Product": "Service"}]}
    assert find_empty_fields(value) == []
