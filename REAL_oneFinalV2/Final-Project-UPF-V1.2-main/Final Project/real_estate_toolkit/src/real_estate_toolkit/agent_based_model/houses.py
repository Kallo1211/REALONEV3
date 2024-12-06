from enum import Enum
from dataclasses import dataclass
from typing import Optional

class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore] = None
    available: bool = True

    def calculate_price_per_square_foot(self) -> float:
        """
        Calculate and return the price per square foot.
        """
        if self.area == 0:  # Handle edge case where area is 0
            return 0.0
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if the house is considered new construction (< 5 years old).
        """
        return (current_year - self.year_built) < 5

    def get_quality_score(self) -> QualityScore:
        """
        Return the quality score of the house. If not set, generate a score based on attributes.
        """
        if self.quality_score is not None:
            return self.quality_score

        # Generate a quality score based on house attributes
        age = 2024 - self.year_built
        if age <= 5 and self.area >= 2000 and self.bedrooms >= 4:
            return QualityScore.EXCELLENT
        elif age <= 10 and self.area >= 1500:
            return QualityScore.GOOD
        elif age <= 20:
            return QualityScore.AVERAGE
        elif age <= 50:
            return QualityScore.FAIR
        else:
            return QualityScore.POOR

    def sell_house(self) -> None:
        """
        Mark house as sold by updating the available status.
        """
        self.available = False
