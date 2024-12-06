from pathlib import Path
from src.real_estate_toolkit.data.loader import DataLoader
from src.real_estate_toolkit.data.cleaner import Cleaner
from src.real_estate_toolkit.data.descriptor import Descriptor

def main():
    # Define the data path and file name
    data_path = Path("src/real_estate_toolkit/data/data_files")
    train_file = "train.csv"

    print("Testing Descriptor: Sale Price Median and 75th Percentile...")

    # Step 1: Load and convert data types using DataLoader
    loader = DataLoader(data_path=data_path)
    try:
        data = loader.load_data_from_csv(train_file)
        data = loader.infer_and_convert_types(data)  # Convert numeric columns
        print(f"Loaded {len(data)} rows from {train_file}.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Step 2: Clean the data using Cleaner
    cleaner = Cleaner(data=data)
    try:
        cleaner.rename_with_best_practices()
        cleaner.na_to_none()
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        return

    # Step 3: Initialize Descriptor
    descriptor = Descriptor(data=data)

    # Step 4: Test Median and Percentile for Sale Price
    try:
        print("\nCalculating median and 75th percentile for sale_price...")

        # Median
        medians = descriptor.median(columns=["sale_price"])
        sale_price_median = medians.get("sale_price", None)
        print(f"Median Sale Price: {sale_price_median}")

        # 75th Percentile
        percentiles = descriptor.percentile(columns=["sale_price"], percentile=75)
        sale_price_75th_percentile = percentiles.get("sale_price", None)
        print(f"75th Percentile Sale Price: {sale_price_75th_percentile}")

    except Exception as e:
        print(f"Error during descriptor operations: {e}")

if __name__ == "__main__":
    main()

# end of part 1 


# test for houses

from src.real_estate_toolkit.agent_based_model.houses import House, QualityScore

def main():
    house = House(id=1, price=300000, area=1500, bedrooms=3, year_built=2020)
    print("Price per square foot:", house.calculate_price_per_square_foot())
    print("Is new construction:", house.is_new_construction())
    print("Quality score:", house.get_quality_score())
    house.sell_house()
    print("Available status after selling:", house.available)

if __name__ == "__main__":
    main()


# testing housing market

from src.real_estate_toolkit.agent_based_model.houses import House
from src.real_estate_toolkit.agent_based_model.house_market import HousingMarket

def main():
    house1 = House(id=1, price=300000, area=1500, bedrooms=3, year_built=2010)
    house2 = House(id=2, price=450000, area=2000, bedrooms=4, year_built=2015, available=False)
    house3 = House(id=3, price=350000, area=1800, bedrooms=3, year_built=2020)

    market = HousingMarket(houses=[house1, house2, house3])

    print("House with ID 1:", market.get_house_by_id(1))
    print("Average price (3 bedrooms):", market.calculate_average_price(bedrooms=3))
    print("Matching houses (max price 400k, min area 1600):", market.get_houses_that_meet_requirements(max_price=400000, min_area=1600))

if __name__ == "__main__":
    main()

# testing consumers.py

from src.real_estate_toolkit.agent_based_model.houses import House, QualityScore
from src.real_estate_toolkit.agent_based_model.house_market import HousingMarket
from src.real_estate_toolkit.agent_based_model.consumers import Consumer, Segment

def main():
    # Create sample houses
    house1 = House(id=1, price=300000, area=1500, bedrooms=3, year_built=2020, quality_score=QualityScore.EXCELLENT)
    house2 = House(id=2, price=200000, area=1200, bedrooms=2, year_built=2015, quality_score=QualityScore.GOOD)
    house3 = House(id=3, price=350000, area=1800, bedrooms=4, year_built=2018, quality_score=QualityScore.AVERAGE)

    # Initialize housing market
    market = HousingMarket(houses=[house1, house2, house3])

    # Create sample consumers
    consumer1 = Consumer(id=1, annual_income=120000, children_number=2, segment=Segment.FANCY)
    consumer2 = Consumer(id=2, annual_income=80000, children_number=1, segment=Segment.OPTIMIZER)
    consumer3 = Consumer(id=3, annual_income=60000, children_number=0, segment=Segment.AVERAGE)

    # Simulate savings
    consumer1.compute_savings(5)
    consumer2.compute_savings(3)
    consumer3.compute_savings(2)

    print(f"Consumer 1 savings: {consumer1.savings}")
    print(f"Consumer 2 savings: {consumer2.savings}")
    print(f"Consumer 3 savings: {consumer3.savings}")

    # Simulate house purchases
    consumer1.buy_a_house(market)
    consumer2.buy_a_house(market)
    consumer3.buy_a_house(market)

if __name__ == "__main__":
    main()

# test simulation

from src.real_estate_toolkit.agent_based_model.simulation import Simulation, AnnualIncomeStatistics, ChildrenRange, CleaningMarketMechanism
from src.real_estate_toolkit.agent_based_model.houses import QualityScore

def main():
    # Example housing market data
    housing_market_data = [
        {"id": 1, "price": 300000, "area": 1500, "bedrooms": 3, "year_built": 2020, "quality_score": 5},
        {"id": 2, "price": 250000, "area": 1200, "bedrooms": 2, "year_built": 2018, "quality_score": 4},
        {"id": 3, "price": 400000, "area": 1800, "bedrooms": 4, "year_built": 2019, "quality_score": 5},
    ]

    # Simulation parameters
    simulation = Simulation(
        housing_market_data=housing_market_data,
        consumers_number=10,
        years=5,
        annual_income=AnnualIncomeStatistics(minimum=30000, average=75000, standard_deviation=15000, maximum=150000),
        children_range=ChildrenRange(minimum=0, maximum=3),
        cleaning_market_mechanism=CleaningMarketMechanism.INCOME_ORDER_DESCENDANT
    )

    # Run the simulation
    simulation.create_consumers()
    simulation.compute_consumers_savings()
    simulation.clean_the_market()

    # Print results
    print(f"Owners population rate: {simulation.compute_owners_population_rate()}%")
    print(f"Houses availability rate: {simulation.compute_houses_availability_rate()}%")

if __name__ == "__main__":
    main()


# test the numpy:

import numpy as np
from src.real_estate_toolkit.data.loader import DataLoader
from src.real_estate_toolkit.data.cleaner import Cleaner
from src.real_estate_toolkit.data.descriptor import DescriptorNumpy

def test_descriptor_numpy_with_project_data():
    # Step 1: Load the dataset
    data_loader = DataLoader(data_path="src/real_estate_toolkit/data/data_files")
    data = data_loader.load_data_from_csv("train.csv")

    # Step 2: Clean the dataset
    cleaner = Cleaner(data)
    cleaner.rename_with_best_practices()
    cleaner.na_to_none()

    # Step 3: Convert cleaned data to NumPy format
    column_names = list(data[0].keys())  # Extract column names from the cleaned dataset
    numpy_data = np.array([[row[col] for col in column_names] for row in data], dtype=object)

    # Step 4: Initialize DescriptorNumpy
    descriptor_numpy = DescriptorNumpy(data=numpy_data, column_names=column_names)

    # Step 5: Run DescriptorNumpy tests
    print("Testing DescriptorNumpy with Project Data...")
    print("None ratios:", descriptor_numpy.none_ratio())
    print("Averages (lot_area, sale_price):", descriptor_numpy.average(["lot_area", "sale_price"]))
    print("Medians (lot_area, sale_price):", descriptor_numpy.median(["lot_area", "sale_price"]))
    print("75th Percentile (lot_area, sale_price):", descriptor_numpy.percentile(["lot_area", "sale_price"], 75))

# Run the test
if __name__ == "__main__":
    test_descriptor_numpy_with_project_data()

