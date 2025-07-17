#!/usr/bin/env python3
"""
Demo script to showcase the batch NFC decode performance test.
This script demonstrates the performance characteristics of the NFC decoder.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import time
import psutil
from services.nfc.device import NFCDevice
from services.nfc.decoder import generate_sample_payload


def main():
    """Run a demonstration of the batch NFC decode performance."""
    print("=== NFC Batch Decode Performance Demo ===")
    print()
    
    # Initialize NFC device
    device = NFCDevice()
    device.connect()
    print(f"✓ NFC Device connected")
    
    # Generate test payloads
    print("✓ Generating 1000 test NFC payloads...")
    payloads = []
    filament_types = ['PLA', 'PETG', 'ABS', 'TPU', 'PC', 'PA', 'PVA', 'HIPS']
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
    
    for i in range(1000):
        filament_type = filament_types[i % len(filament_types)]
        color = colors[i % len(colors)]
        format_type = 'bambu_v1' if i % 2 == 0 else 'bambu_v2'
        
        payload = generate_sample_payload(
            format_type=format_type,
            name=f'Demo Filament {i:04d}',
            type=filament_type,
            color=color,
            remaining_weight=1000 - (i % 100),
            remaining_length=240 - (i % 50)
        )
        payloads.append(payload)
    
    print(f"✓ Generated {len(payloads)} test payloads")
    print()
    
    # Measure memory before
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024
    
    # Perform batch decode
    print("⚡ Starting batch decode performance test...")
    start_time = time.time()
    
    results = device.batch_decode(payloads)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Measure memory after
    memory_after = process.memory_info().rss / 1024 / 1024
    memory_increase = memory_after - memory_before
    
    # Calculate statistics
    successful_decodes = sum(1 for result in results if result is not None)
    avg_time_per_payload = (total_time / 1000) * 1000  # in ms
    
    print("✓ Batch decode completed!")
    print()
    
    # Display results
    print("=== PERFORMANCE RESULTS ===")
    print(f"📊 Total payloads processed:  {len(payloads):,}")
    print(f"✅ Successful decodes:        {successful_decodes:,}")
    print(f"❌ Failed decodes:            {len(payloads) - successful_decodes:,}")
    print(f"⏱️  Total processing time:     {total_time:.3f} seconds")
    print(f"⚡ Average time per payload:  {avg_time_per_payload:.3f} ms")
    print(f"🧠 Memory usage before:       {memory_before:.1f} MB")
    print(f"🧠 Memory usage after:        {memory_after:.1f} MB")
    print(f"📈 Memory increase:           {memory_increase:.1f} MB")
    print()
    
    # Performance assessment
    print("=== PERFORMANCE ASSESSMENT ===")
    
    # Throughput
    payloads_per_second = 1000 / total_time
    print(f"🚀 Throughput:                {payloads_per_second:,.0f} payloads/second")
    
    # Performance thresholds
    max_time_per_payload = 5.0  # ms
    max_memory_increase = 50    # MB
    
    if avg_time_per_payload <= max_time_per_payload:
        print(f"✅ Decode speed:              EXCELLENT ({avg_time_per_payload:.3f}ms ≤ {max_time_per_payload}ms)")
    else:
        print(f"⚠️  Decode speed:              SLOW ({avg_time_per_payload:.3f}ms > {max_time_per_payload}ms)")
    
    if memory_increase <= max_memory_increase:
        print(f"✅ Memory efficiency:         EXCELLENT ({memory_increase:.1f}MB ≤ {max_memory_increase}MB)")
    else:
        print(f"⚠️  Memory efficiency:         POOR ({memory_increase:.1f}MB > {max_memory_increase}MB)")
    
    if successful_decodes == 1000:
        print(f"✅ Decode reliability:        PERFECT (100% success rate)")
    else:
        success_rate = (successful_decodes / 1000) * 100
        print(f"⚠️  Decode reliability:        {success_rate:.1f}% success rate")
    
    print()
    
    # Show sample decoded data
    print("=== SAMPLE DECODED DATA ===")
    if results and results[0]:
        sample = results[0]
        print(f"Sample payload #1:")
        for key, value in sample.items():
            if key != 'header':  # Skip header in display
                print(f"  {key}: {value}")
    
    print()
    print("🎉 Demo completed successfully!")


if __name__ == "__main__":
    main()