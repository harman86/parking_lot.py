import random
import json
import boto3
from typing import List

class ParkingLot:
    def __init__(self, size: int, spot_length: int = 8, spot_width: int = 12):
        """
        Initialize the ParkingLot with a given size and optional parking spot dimensions.
        :param size: Total square footage of the parking lot.
        :param spot_length: Length of each parking spot in feet. Default is 8.
        :param spot_width: Width of each parking spot in feet. Default is 12.
        """
        self.size = size
        self.spot_size = spot_length * spot_width
        self.num_spots = self.size // self.spot_size
        self.spots = [None] * self.num_spots

    def park_car(self, car, spot: int) -> bool:
        """
        Park a car in a specific spot if the spot is empty.
        :param car: Instance of the Car class.
        :param spot: Spot number where the car should be parked.
        :return: True if the car was parked successfully, False otherwise.
        """
        if self.spots[spot] is None:
            self.spots[spot] = car
            return True
        return False

    def to_json(self) -> str:
        """
        Convert the current parking lot status to a JSON string.
        :return: JSON string representation of the parking lot.
        """
        parking_map = {f"Spot {i}": str(car) for i, car in enumerate(self.spots) if car is not None}
        return json.dumps(parking_map, indent=4)

    def upload_to_s3(self, bucket_name: str, file_name: str):
        """
        Upload the JSON representation of the parking lot to an S3 bucket.
        :param bucket_name: Name of the S3 bucket.
        :param file_name: Name of the file to be saved in the S3 bucket.
        """
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=self.to_json())
        print(f"Uploaded parking lot data to S3 bucket {bucket_name} as {file_name}.")


class Car:
    def __init__(self, license_plate: str):
        """
        Initialize a Car with a given license plate.
        :param license_plate: License plate number of the car.
        """
        self.license_plate = license_plate

    def __str__(self):
        """
        Return the license plate when the car is converted to a string.
        :return: License plate number.
        """
        return self.license_plate

    def park(self, parking_lot: ParkingLot, spot: int) -> bool:
        """
        Try to park the car in a given spot in the parking lot.
        :param parking_lot: Instance of the ParkingLot class.
        :param spot: Spot number where the car should be parked.
        :return: True if the car was parked successfully, False otherwise.
        """
        success = parking_lot.park_car(self, spot)
        if success:
            print(f"Car with license plate {self.license_plate} parked successfully in spot {spot}.")
        else:
            print(f"Car with license plate {self.license_plate} failed to park in spot {spot}.")
        return success


def generate_random_license_plate() -> str:
    """
    Generate a random 7-digit license plate number.
    :return: Random 7-digit license plate number as a string.
    """
    return str(random.randint(1000000, 9999999))


def create_cars(num_cars: int) -> List[Car]:
    """
    Create a list of cars with random license plates.
    :param num_cars: Number of cars to create.
    :return: List of Car instances.
    """
    return [Car(generate_random_license_plate()) for _ in range(num_cars)]


def park_cars_randomly(parking_lot: ParkingLot, cars: List[Car]):
    """
    Park each car in the parking lot in a random spot.
    :param parking_lot: Instance of the ParkingLot class.
    :param cars: List of Car instances to be parked.
    """
    available_spots = list(range(parking_lot.num_spots))
    for car in cars:
        while True:
            if not available_spots:
                print("Parking lot is full.")
                return
            spot = random.choice(available_spots)
            if car.park(parking_lot, spot):
                break


def main():
    """
    Main function to execute the parking lot challenge.
    """
    parking_lot_size = 2000  # Example size in square feet
    num_cars = 25  # Example number of cars

    parking_lot = ParkingLot(parking_lot_size)
    cars = create_cars(num_cars)
    park_cars_randomly(parking_lot, cars)

    # Optional: Save to JSON and upload to S3
    json_data = parking_lot.to_json()
    with open('parking_lot.json', 'w') as file:
        file.write(json_data)

    # Uncomment the following line to upload to S3
    # parking_lot.upload_to_s3('your-s3-bucket-name', 'parking_lot.json')

if __name__ == "__main__":
    main()
