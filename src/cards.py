"""
Object Character Recognition (OCR) modularity for image processing using the Tesseract algorithm.

Author: Dillon Barendt
Organization: Concord Capital Management, LLC
Modified: 11/23/2022

TODO: Turn OCR into a python pipeline generator
"""
from typing import Generator

import re

import pytesseract as pytesseract
import cv2

FIRST_NUMBER = {
    "American Express": "3",
    "Visa": "4",
    "MasterCard": "5",
    "Discover Card": "6"
}

CARD_ATTRS = {
    "NUMBER": "",
    "EXP": "",
    "CVV": "",
}


def ocr_generate(
        tesseract_path: str,
        image_path: str
) -> Generator:
    """
    Yields characters from an image.

    :param tesseract_path: The path to the tesseract executable
    :type tesseract_path: str
    :param image_path: The image path for processing
    :type image_path: str
    """
    tesseract = tesseract_path
    ocr_response = pytesseract.image_to_string(
        image_path,
        lang='eng',
        nice=True
    )
    yield ocr_response


def ocr_response(
        image_path: str
) -> list:
    """
    Data preparation for card processing.

    :return: A list of all ocr values
    :rtype: list
    """
    preprocessed_result = []

    ocr_response = list(ocr_generate(tesseract_path, image_path))
    for line in ocr_response[0].split('\n'):
        preprocessed_result.append(line.strip(' '))
    return preprocessed_result


def map_front_attrs(
        img_card_front: str,
        img_card_back: str
):
    """
    Returns the attributes found on the front of the card image.

    :return: A dictionary of card attributes
    :rtype:
    """
    result_front = ocr_response(img_card_front)
    result_back = ocr_response(img_card_back)

    for value in result_front:
        num_values = len(
            re.sub(
                "[^0-9]",
                "",
                value
            )
        )
        if num_values == 16:
            CARD_ATTRS["NUMBER"] = value

        elif "/" in value and num_values == 4:
            date_separator = value.find("/")
            date = value[date_separator-2: date_separator + 3]
            CARD_ATTRS['EXP'] = date

    for value in result_back:
        print(f"BACK_VALUE={result_back}")

    return CARD_ATTRS

