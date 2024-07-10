import frappe
import json
import os
from barcode import EAN13
from barcode.writer import ImageWriter
import cv2
from random import randrange
from functools import reduce
import base64


@frappe.whitelist()
def get_items(supplier):
    """
    Retrieves a list of items associated with a given supplier.

    Args:
        supplier (str): The name of the supplier.

    Returns:
        list: A list of dictionaries representing the items. Each dictionary contains the following keys:
            - name (str): The name of the item.
            - item_name (str): The display name of the item.

    If no items are found for the given supplier, an empty list is returned.
    """
    # Get item codes from Item Supplier
    item_codes = frappe.get_all(
        "Item Supplier", filters={"supplier": supplier}, fields=["parent"]
    )
    item_codes = [item["parent"] for item in item_codes]

    if not item_codes:
        return []

    # Get item names from Item doctype
    items = frappe.get_all(
        "Item", filters={"name": ["in", item_codes]}, fields=["name", "item_name"]
    )

    return items or []  # Return an empty list if no items are found


@frappe.whitelist()
def get_items_details(items):
    """
    Retrieves the details of a list of items.

    Args:
        items (Union[str, List[str]]): A string representing a JSON list of item names, or a list of item names.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the details of the items. Each dictionary contains the following keys:
            - name (str): The name of the item.
            - item_name (str): The display name of the item.
            - ... (Any): Other fields of the Item doctype.

    If no items are found, an empty list is returned.

    """
    if isinstance(items, str):
        items = json.loads(items)
    items = set(items)
    # Fetch details for the items
    items_details = frappe.get_all(
        "Item", filters={"name": ["in", list(items)]}, fields="*"
    )

    return items_details or []  # Return an empty list if no details are found


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += str(ele)

    # return string
    return str1


def generate_12_random_numbers():
    numbers = []
    for x in range(12):
        numbers.append(randrange(10))
    return numbers


def calculate_checksum(ean):
    """
    Calculates the checksum for an EAN13
    @param list ean: List of 12 numbers for first part of EAN13
    :returns: The checksum for `ean`.
    :rtype: Integer
    """
    assert len(ean) == 12, "EAN must be a list of 12 numbers"
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, ean[::2])
    oddsum = reduce(sum_, ean[1::2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10


@frappe.whitelist()
def create_code(
    number="", item_code="new_code1", item_name="new_code1", file_name="Itemcode"
):
    try:
        if number == "":
            number = generate_12_random_numbers()
            number.append(calculate_checksum(number))
            number = listToString(number)

        if len(number) != 13 or not number.isdigit():
            return {"status": "error", "message": "Invalid EAN-13 number"}

        file_name = file_name + "_" + number
        my_code = EAN13(number, writer=ImageWriter())

        output_file_folder = frappe.utils.get_site_path("public", "files")

        if not os.path.exists(output_file_folder):
            os.makedirs(output_file_folder)

        output_file_path = os.path.join(output_file_folder, f"{file_name}")

        my_code.save(output_file_path)

        image = cv2.imread(output_file_path + ".png")

        h, w, c = image.shape
        text = item_code + "  " + item_name
        font = cv2.FONT_HERSHEY_SIMPLEX

        fontScale = 0.5

        color = (0, 0, 0)

        thickness = 1

        textsize = cv2.getTextSize(text, font, fontScale, thickness)[0]

        offset = int(h - 10)

        textX = (image.shape[1] - textsize[0]) // 2
        org = (textX, offset)

        image = cv2.putText(
            image, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False
        )

        cv2.imwrite(output_file_path + ".png", image)

        with open(output_file_path + ".png", "rb") as imagefile:
            convert = base64.b64encode(imagefile.read())

        return {
            "status": "success",
            "message": {
                # "base": "data:image/png;base64," + convert.decode("utf-8"),
                "base": convert.decode("utf-8"),
                "image": "/files/" + file_name + ".png",
                "barcode": number,
            },
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
