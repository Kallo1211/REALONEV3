from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from .houses import House
from .house_market import HousingMarket

class Segment(Enum):
    FANCY = auto()  # Prefers new construction and high quality scores
    OPTIMIZER = auto()  # Focuses on price per square foot value
    AVERAGE = auto()  # Considers houses below average market price

@dataclass
class Consumer:
    id: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House] = None
    savings: float = 0.0
    saving_rate: float = 0.3  # Portion of annual income saved each year
    interest_rate: float = 0.05  # Annual compound interest rate on savings

    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time.
        """
        for _ in range(years):
            self.savings += self.saving_rate * self.annual_income
            self.savings *= (1 + self.interest_rate)  # Apply compound interest

    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house based on segment preferences.
        """
        if self.house is not None:
            print(f"Consumer {self.id} already owns a house.")
            return

        # Retrieve available houses
        available_houses = [house for house in housing_market.houses if house.available]

        if not available_houses:
            print("No houses available for purchase.")
            return

        suitable_houses = []

        # Apply segment-specific filtering
        if self.segment == Segment.FANCY:
            suitable_houses = [
                house for house in available_houses
                if house.is_new_construction() and house.get_quality_score().value == 5
            ]
        elif self.segment == Segment.OPTIMIZER:
            suitable_houses = [
                house for house in available_houses
                if house.calculate_price_per_square_foot() <= (self.annual_income / 12)
            ]
        elif self.segment == Segment.AVERAGE:
            average_price = housing_market.calculate_average_price()
            suitable_houses = [
                house for house in available_houses
                if house.price <= average_price
            ]

        if not suitable_houses:
            print(f"No suitable houses found for Consumer {self.id}.")
            return

        # Find the most suitable house (smallest price for simplicity)
        chosen_house = min(suitable_houses, key=lambda h: h.price)

        # Check if savings are sufficient for a 20% down payment
        down_payment = 0.2 * chosen_house.price
        if self.savings >= down_payment:
            self.savings -= down_payment
            chosen_house.sell_house()  # Mark the house as sold
            self.house = chosen_house
            print(f"Consumer {self.id} purchased house ID {chosen_house.id}.")
        else:
            print(f"Consumer {self.id} cannot afford the down payment for house ID {chosen_house.id}.")



