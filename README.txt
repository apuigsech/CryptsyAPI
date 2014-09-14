# CryptsyAPI

A Python Cryptsy API implementation.

## Installation

	python setup.py install

## Usage

    import CryptsyAPI

    api = CryptsyAPI.CryptsyAPI(API_KEY, API_SECRET)
    api.getmarkets()