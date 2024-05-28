# Parking Lot Challenge

## Overview

This project implements a parking lot management system using Python. The parking lot can be initialized with a given square footage size and allows cars with 7-digit license plates to be parked in random spots.

## Features

- Calculate the number of parking spots based on configurable spot dimensions.
- Park cars in specified spots and handle collisions by trying different spots.
- Output parking status to the terminal.
- Optionally, save the parking lot data to a JSON file and upload it to an S3 bucket.

## How to Run

1. Ensure you have Python 3 installed.
2. Clone this repository.
3. Navigate to the repository directory.
4. Run the script:

```bash
python parking_lot.py
