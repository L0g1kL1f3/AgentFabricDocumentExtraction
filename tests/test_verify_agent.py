from fabricagent import find_empty_fields


def test_nested_empty_values():
    data = {
        "InvoiceID": None,
        "DueDate": "",
        "Items": [
            {"Product": None, "Quantity": 2},
        ],
    }
    assert find_empty_fields(data) == [
        "InvoiceID",
        "DueDate",
        "Items[0].Product",
    ]


def test_empty_list_is_reported():
    assert find_empty_fields({"Items": []}) == ["Items"]


def test_populated_document_has_no_empty_fields():
    data = {
        "InvoiceID": "INV-001",
        "TotalAmount": 100.0,
        "Items": [{"Product": "Service", "Quantity": 1}],
    }
    assert find_empty_fields(data) == []
