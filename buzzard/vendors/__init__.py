"""Buzzard Vendors Package.

Detects system vendor and instantiates appropriate vendor backend.
"""

from typing import Type
from buzzard.vendors.asus import ASUSVendor
from buzzard.vendors.base import VendorBackend
from buzzard.vendors.generic import GenericVendor

_VENDORS: list[Type[VendorBackend]] = [
    ASUSVendor,
    GenericVendor,
]


def get_vendor_backend() -> VendorBackend:
    """Detects system vendor and returns active VendorBackend instance.

    Returns:
        Instance of matched VendorBackend (defaults to GenericVendor).
    """
    for vendor_cls in _VENDORS:
        backend = vendor_cls()
        if backend.detect():
            return backend
    return GenericVendor()
