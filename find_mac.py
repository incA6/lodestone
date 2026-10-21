# Govee lightbulb

import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for local BLE devices... (This will take 10 seconds)")
    devices = await BleakScanner.discover(timeout=10.0)
    
    print("\nFound Devices:")
    print(f"{'MAC / UUID Address':<40} | {'Device Name (Device ID)'}")
    print("-" * 75)
    
    for d in devices:
        # Filter for known Govee naming patterns, or display everything if name exists
        if d.name:
            name_lower = d.name.lower()
            is_govee = any(x in name_lower for x in ["govee", "ihoment", "minger", "h60", "h61"])
            
            # Star them so they stand out in the terminal list
            prefix = "----> [GOVEE?] " if is_govee else "  "
            print(f"{prefix}{d.address:<31} | {d.name}")

if __name__ == "__main__":
    asyncio.run(main())
