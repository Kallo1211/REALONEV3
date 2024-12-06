from typing import List, Optional
from .houses import House

class HousingMarket:
    def __init__(self, houses: List[House]):
        """
        Initialize the housing market with a list of houses.
        """
        self.houses: List[House] = houses

    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve a specific house by its ID.
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        return None  # Return None if the house is not found

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate the average house price, optionally filtered by number of bedrooms.
        """
        filtered_houses = [house for house in self.houses if (bedrooms is None or house.bedrooms == bedrooms) and house.available]

        if not filtered_houses:  # Handle case with no matching houses
            return 0.0

        total_price = sum(house.price for house in filtered_houses)
        return round(total_price / len(filtered_houses), 2)

    def get_houses_that_meet_requirements(self, max_price: float, min_area: float) -> Optional[List[House]]:
        """
        Filter houses based on buyer requirements (max price and min area).
        """
        matching_houses = [
            house for house in self.houses
            if house.price <= max_price and house.area >= min_area and house.available
        ]

        if not matching_houses:  # Handle case where no houses match
            return None

        return matching_houses
