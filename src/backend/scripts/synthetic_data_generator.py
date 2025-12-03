#!/usr/bin/env python3
# Copyright (c) 2025 Green Wave Team
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Synthetic Data Generator for GreenWave Environmental Monitoring

This script generates realistic synthetic data for environmental monitoring models:
- TrafficEnvironmentImpact
- AirQualityObserved
- CarbonFootprint
- WaterQualityObserved
Features:
- Generates data every second with realistic values
- Clean, modular design with factory classes
- Extensible for additional models and frequencies
- Graceful shutdown with Ctrl+C
- Console output and future service integration hooks

Usage:
    python synthetic_data_generator.py

Press Ctrl+C to stop the generator gracefully.
"""

import logging
import signal
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from random import Random
from typing import Any, Dict, List

# Add parent directory to Python path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.AirQualityObserved import Type6 as AirQualityType
from app.models.AirQualityObserved import TypeofLocation
from app.models.CarbonFootprint import Type6 as CarbonType
from app.models.TrafficEnvironmentImpact import (
    Type6 as TrafficType,
)
from app.models.WaterQualityObserved import Type6 as WaterType

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataGenerator(ABC):
    """
    Abstract base class for data generators.
    Each generator creates realistic synthetic data for a specific model type.
    """

    def __init__(self, seed: int = 42):
        """Initialize generator with random seed for reproducible results."""
        self.random = Random(seed)
        self.entity_counter = 0

    @abstractmethod
    def generate_data(self) -> Dict[str, Any]:
        """Generate synthetic data as dictionary."""
        pass

    def _get_timestamp(self) -> str:
        """Get current ISO 8601 timestamp."""
        return datetime.now(timezone.utc).isoformat()

    def _get_entity_id(self, prefix: str) -> str:
        """Generate unique entity ID with given prefix."""
        self.entity_counter += 1
        return f"urn:ngsi-ld:{prefix}:{self.entity_counter:03d}"


class TrafficEnvironmentImpactGenerator(DataGenerator):
    """Generate realistic TrafficEnvironmentImpact data."""

    def __init__(self, seed: int = 42):
        super().__init__(seed)
        # Traffic simulation parameters
        self.base_co2 = 300.0  # ppm baseline
        self.traffic_intensity = self.random.uniform(
            0.3, 0.9
        )  # Current traffic density

    def generate_data(self) -> Dict[str, Any]:
        """Generate TrafficEnvironmentImpact data with realistic CO2 levels."""
        # Simulate traffic flow variations
        self.traffic_intensity += self.random.uniform(-0.1, 0.1)
        self.traffic_intensity = max(0.1, min(1.0, self.traffic_intensity))

        # CO2 levels correlate with traffic intensity (300-500 ppm range)
        co2_level = (
            self.base_co2
            + (self.traffic_intensity * 200)
            + self.random.uniform(-20, 20)
        )

        return {
            "id": self._get_entity_id("TrafficEnvironmentImpact"),
            "type": TrafficType.TrafficEnvironmentImpact.value,
            "dateObservedFrom": self._get_timestamp(),
            "dateObservedTo": self._get_timestamp(),
            "co2": round(co2_level, 2),
            "description": f"Traffic impact measurement at intensity {self.traffic_intensity:.2f}",
            "dataProvider": "GreenWave Synthetic Generator",
            "source": "https://github.com/greenwave/synthetic-generator",
            "traffic": [
                {
                    "vehicleClass": "passenger_car",
                    "refTrafficFlowObserved": f"urn:ngsi-ld:TrafficFlowObserved:{self.entity_counter:03d}",
                }
            ],
        }


class AirQualityObservedGenerator(DataGenerator):
    """Generate realistic AirQualityObserved data."""

    def __init__(self, seed: int = 42):
        super().__init__(seed)
        # Air quality simulation parameters
        self.pollution_level = self.random.uniform(0.2, 0.8)
        self.time_of_day_factor = 1.0  # Will vary with time

    def generate_data(self) -> Dict[str, Any]:
        """Generate AirQualityObserved data with realistic pollutant levels."""
        # Simulate daily pollution patterns
        current_hour = datetime.now().hour
        if 7 <= current_hour <= 9 or 17 <= current_hour <= 19:  # Rush hours
            self.time_of_day_factor = 1.5
        elif 22 <= current_hour or current_hour <= 5:  # Night time
            self.time_of_day_factor = 0.7
        else:
            self.time_of_day_factor = 1.0

        # Add random variation
        self.pollution_level += self.random.uniform(-0.05, 0.05)
        self.pollution_level = max(0.1, min(1.0, self.pollution_level))

        # Generate realistic pollutant values based on pollution level
        base_factor = self.pollution_level * self.time_of_day_factor

        data = {
            "id": self._get_entity_id("AirQualityObserved"),
            "type": AirQualityType.AirQualityObserved.value,
            "dateObserved": self._get_timestamp(),
            "dataProvider": "GreenWave Synthetic Generator",
            "source": "https://github.com/greenwave/synthetic-generator",
            "typeofLocation": self.random.choice(
                [TypeofLocation.indoor, TypeofLocation.outdoor]
            ),
            "airQualityIndex": round(50 + (base_factor * 150), 1),  # 50-200 AQI range
            "airQualityLevel": self._get_aqi_level(base_factor),
        }

        # Add pollutants with realistic concentrations
        pollutants = {
            "pm25": round(base_factor * 35 + self.random.uniform(-5, 5), 2),  # µg/m³
            "pm10": round(base_factor * 50 + self.random.uniform(-10, 10), 2),  # µg/m³
            "no2": round(base_factor * 40 + self.random.uniform(-8, 8), 2),  # ppb
            "o3": round(base_factor * 60 + self.random.uniform(-15, 15), 2),  # ppb
            "co": round(base_factor * 2 + self.random.uniform(-0.5, 0.5), 2),  # ppm
            "so2": round(base_factor * 10 + self.random.uniform(-3, 3), 2),  # ppb
            "co2": round(
                400 + base_factor * 100 + self.random.uniform(-20, 20), 2
            ),  # ppm
            "temperature": round(20 + self.random.uniform(-10, 15), 1),  # °C
            "relativeHumidity": round(
                0.4 + self.random.uniform(0.0, 0.4), 3
            ),  # 0-1 range
            "windSpeed": round(self.random.uniform(0.5, 8.0), 1),  # m/s
            "windDirection": round(self.random.uniform(-180, 180), 1),  # degrees
        }

        data.update(pollutants)
        return data

    def _get_aqi_level(self, pollution_factor: float) -> str:
        """Get AQI level based on pollution factor."""
        if pollution_factor < 0.2:
            return "Good"
        elif pollution_factor < 0.4:
            return "Moderate"
        elif pollution_factor < 0.6:
            return "Unhealthy for Sensitive Groups"
        elif pollution_factor < 0.8:
            return "Unhealthy"
        else:
            return "Hazardous"


class CarbonFootprintGenerator(DataGenerator):
    """Generate realistic CarbonFootprint data."""

    def __init__(self, seed: int = 42):
        super().__init__(seed)
        self.emission_sources = [
            "Transport",
            "Industry",
            "Agriculture",
            "Residential",
            "Commercial",
        ]
        self.base_emission_rate = self.random.uniform(50.0, 200.0)  # kg CO2eq/day

    def generate_data(self) -> Dict[str, Any]:
        """Generate CarbonFootprint data with realistic emission values."""
        # Vary emissions based on time and random factors
        hourly_variation = 1.0 + 0.3 * self.random.uniform(-1, 1)
        daily_emission = self.base_emission_rate * hourly_variation

        # Convert to kg CO2eq per hour for the data point
        co2eq_per_hour = daily_emission / 24

        return {
            "id": self._get_entity_id("CarbonFootprint"),
            "type": CarbonType.CarbonFootprint.value,
            "dateCreated": self._get_timestamp(),
            "dateModified": self._get_timestamp(),
            "emissionDate": self._get_timestamp(),
            "CO2eq": round(co2eq_per_hour, 3),  # kg CO2eq
            "emissionSource": self.random.choice(self.emission_sources),
            "description": f"Carbon emissions from {self.emission_sources[-1]} sector",
            "dataProvider": "GreenWave Synthetic Generator",
            "source": "https://github.com/greenwave/synthetic-generator",
            "tags": [
                self.random.choice(["urban", "industrial", "residential", "commercial"])
            ],
        }


class WaterQualityObservedGenerator(DataGenerator):
    """Generate realistic WaterQualityObserved data."""

    def __init__(self, seed: int = 42):
        super().__init__(seed)
        self.water_sources = [
            "River",
            "Lake",
            "Reservoir",
            "Groundwater",
            "Treatment Plant",
        ]
        self.water_quality_trend = self.random.uniform(0.3, 0.8)

    def generate_data(self) -> Dict[str, Any]:
        """Generate WaterQualityObserved data with realistic water quality parameters."""
        # Simulate water quality variations
        self.water_quality_trend += self.random.uniform(-0.02, 0.02)
        self.water_quality_trend = max(0.1, min(1.0, self.water_quality_trend))

        # Good water quality has lower values for contaminants
        quality_factor = (
            1.0 - self.water_quality_trend
        )  # Invert: higher trend = better quality

        data = {
            "id": self._get_entity_id("WaterQualityObserved"),
            "type": WaterType.WaterQualityObserved.value,
            "dateObserved": self._get_timestamp(),
            "dataProvider": "GreenWave Synthetic Generator",
            "source": "https://github.com/greenwave/synthetic-generator",
            "description": f"Water quality measurement from {self.water_sources[0]}",
            "temperature": round(15 + self.random.uniform(-5, 10), 1),  # °C
            "pH": round(
                7.0 + self.random.uniform(-1.5, 1.5), 2
            ),  # 6.5-8.5 typical range
        }

        # Add water quality parameters
        water_params = {
            # Chemical parameters
            "dissolvedOxygen": round(
                8.0 - (quality_factor * 3) + self.random.uniform(-1, 1), 2
            ),  # mg/L
            "conductivity": round(
                200 + (quality_factor * 800) + self.random.uniform(-50, 50), 1
            ),  # µS/cm
            "turbidity": round(
                quality_factor * 20 + self.random.uniform(-2, 2), 1
            ),  # NTU
            "alkalinity": round(100 + self.random.uniform(-20, 40), 1),  # mg/L as CaCO3
            # Nutrients
            "nitrates": round(
                quality_factor * 10 + self.random.uniform(-1, 2), 2
            ),  # mg/L
            "phosphates": round(
                quality_factor * 2 + self.random.uniform(-0.2, 0.3), 2
            ),  # mg/L
            "ammonia": round(
                quality_factor * 1.5 + self.random.uniform(-0.1, 0.2), 2
            ),  # mg/L
            # Heavy metals (µg/L - typically very low)
            "lead": round(quality_factor * 5 + self.random.uniform(-1, 2), 3),
            "mercury": round(quality_factor * 0.5 + self.random.uniform(-0.1, 0.1), 3),
            "cadmium": round(quality_factor * 1 + self.random.uniform(-0.2, 0.2), 3),
            "arsenic": round(quality_factor * 3 + self.random.uniform(-0.5, 0.5), 3),
            # Organic matter
            "bod": round(quality_factor * 8 + self.random.uniform(-1, 2), 1),  # mg/L
            "cod": round(quality_factor * 25 + self.random.uniform(-3, 5), 1),  # mg/L
            # Other parameters
            "chlorides": round(20 + self.random.uniform(-5, 15), 1),  # mg/L
            "sulfates": round(30 + self.random.uniform(-8, 20), 1),  # mg/L
            "totalSuspendedSolids": round(
                quality_factor * 25 + self.random.uniform(-5, 10), 1
            ),  # mg/L
        }

        data.update(water_params)
        return data


class SyntheticDataOrchestrator:
    """
    Orchestrates the generation of synthetic data from multiple generators.
    Handles scheduling, output, and graceful shutdown.
    """

    def __init__(self, interval_seconds: int = 1, save_to_database: bool = False):
        """Initialize orchestrator with generation interval and database option."""
        self.interval_seconds = interval_seconds
        self.save_to_database = save_to_database
        self.generators = {
            "TrafficEnvironmentImpact": TrafficEnvironmentImpactGenerator(),
            "AirQualityObserved": AirQualityObservedGenerator(),
            "CarbonFootprint": CarbonFootprintGenerator(),
            "WaterQualityObserved": WaterQualityObservedGenerator(),
        }
        self.running = False
        self._service = None

    def generate_all_data(self) -> Dict[str, Dict[str, Any]]:
        """Generate data from all configured generators."""
        return {
            name: generator.generate_data()
            for name, generator in self.generators.items()
        }

    def output_data(self, data: Dict[str, Dict[str, Any]]) -> None:
        """Output generated data to console. Override this method for custom output."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*80}")
        print(f"🌍 GreenWave Synthetic Data Generation - {timestamp}")
        print(f"{'='*80}")

        for model_name, model_data in data.items():
            print(f"\n📊 {model_name}:")
            print(f"   ID: {model_data.get('id', 'N/A')}")
            print(f"   Type: {model_data.get('type', 'N/A')}")

            # Display key measurement fields
            key_fields = self._get_key_fields(model_name)
            for field in key_fields:
                if field in model_data and model_data[field] is not None:
                    print(f"   {field}: {model_data[field]}")

        print(f"{'='*80}")
        print("Press Ctrl+C to stop the generator...")

    def _get_key_fields(self, model_name: str) -> List[str]:
        """Get key measurement fields for each model type."""
        field_mapping = {
            "TrafficEnvironmentImpact": ["co2", "description"],
            "AirQualityObserved": ["airQualityIndex", "airQualityLevel", "pm25", "no2"],
            "CarbonFootprint": ["CO2eq", "emissionSource"],
            "WaterQualityObserved": [
                "pH",
                "temperature",
                "dissolvedOxygen",
                "turbidity",
            ],
        }
        return field_mapping.get(model_name, ["description"])

    def save_to_service(self, data: Dict[str, Dict[str, Any]]) -> None:
        """
        Placeholder for saving data to external services.
        Override this method to implement:
        - Database storage
        - API calls to external services
        - Message queue publishing
        - File logging

        Args:
            data: Generated data from all models
        """
        # Example implementation:
        # for model_name, model_data in data.items():
        #     requests.post(f"https://api.example.com/{model_name.lower()}", json=model_data)
        pass

    def run(self) -> None:
        """Main execution loop with graceful shutdown handling."""
        self.running = True

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print("🚀 Starting GreenWave Synthetic Data Generator")
        print(f"⏰ Generation interval: {self.interval_seconds} second(s)")
        print(f"📝 Active models: {', '.join(self.generators.keys())}")
        print("\n" + "=" * 80)

        try:
            while self.running:
                start_time = time.time()

                # Generate data
                data = self.generate_all_data()

                # Output to console
                self.output_data(data)

                # Optionally save to services (uncomment to enable)
                # self.save_to_service(data)

                # Calculate sleep time to maintain consistent interval
                elapsed = time.time() - start_time
                sleep_time = max(0, self.interval_seconds - elapsed)

                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass  # Handled by signal handler
        finally:
            print("\n\n🛑 Synthetic Data Generator stopped gracefully")

    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals gracefully."""
        print(f"\n\n⚠️  Received signal {signum}. Shutting down gracefully...")
        self.running = False

    def add_generator(self, name: str, generator: DataGenerator) -> None:
        """Add a new generator to the orchestrator."""
        self.generators[name] = generator
        print(f"✅ Added new generator: {name}")

    def remove_generator(self, name: str) -> None:
        """Remove a generator from the orchestrator."""
        if name in self.generators:
            del self.generators[name]
            print(f"🗑️  Removed generator: {name}")


def main():
    """Main entry point for the synthetic data generator."""
    import argparse

    parser = argparse.ArgumentParser(description="GreenWave Synthetic Data Generator")
    parser.add_argument(
        "--interval",
        type=int,
        default=1,
        help="Generation interval in seconds (default: 1)",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        choices=[
            "TrafficEnvironmentImpact",
            "AirQualityObserved",
            "CarbonFootprint",
            "WaterQualityObserved",
        ],
        help="Specify which models to generate data for (default: all)",
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = SyntheticDataOrchestrator(interval_seconds=args.interval)

    # Filter generators if specific models requested
    if args.models:
        generators_to_keep = {}
        for model_name in args.models:
            if model_name in orchestrator.generators:
                generators_to_keep[model_name] = orchestrator.generators[model_name]
        orchestrator.generators = generators_to_keep
        print(f"🎯 Generating data for: {', '.join(args.models)}")

    # Run the generator
    orchestrator.run()


if __name__ == "__main__":
    main()
