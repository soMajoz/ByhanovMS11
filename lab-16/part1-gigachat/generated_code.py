"""Utility functions generated for the GigaChat lab and manually verified."""

from __future__ import annotations

import re


def is_prime(number: int) -> bool:
    """Return True if number is prime."""
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def fibonacci(length: int) -> list[int]:
    """Return a Fibonacci sequence with the requested length."""
    if length < 0:
        raise ValueError("length must be non-negative")
    sequence: list[int] = []
    a, b = 0, 1
    for _ in range(length):
        sequence.append(a)
        a, b = b, a + b
    return sequence


def normalize_phone(phone: str) -> str:
    """Normalize Russian phone number to +7XXXXXXXXXX."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits[0] in {"7", "8"}:
        return "+7" + digits[1:]
    if len(digits) == 10:
        return "+7" + digits
    raise ValueError("phone must contain 10 or 11 digits")

