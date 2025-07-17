"""
Performance tests for batch NFC decode operations.
Tests the decoding performance and resource usage for batches of NFC payloads.
"""
import pytest
import time
import psutil
import gc
import os
from typing import List
from services.nfc.device import NFCDevice
from services.nfc.decoder import NFCDecoder, generate_sample_payload


class TestBatchNFCDecodePerformance:
    """Performance tests for batch NFC decode operations."""
    
    # Performance thresholds
    MAX_DECODE_TIME_PER_PAYLOAD_MS = 5.0  # 5ms per payload maximum
    MAX_TOTAL_BATCH_TIME_SECONDS = 10.0   # 10 seconds for 1000 payloads maximum
    MAX_MEMORY_INCREASE_MB = 50           # 50MB memory increase maximum
    
    @pytest.fixture
    def nfc_device(self):
        """Create an NFC device for testing."""
        device = NFCDevice()
        device.connect()
        return device
    
    @pytest.fixture
    def sample_payloads_1000(self):
        """Generate 1000 sample NFC payloads for performance testing."""
        payloads = []
        
        # Generate diverse payloads to simulate real-world scenarios
        filament_types = ['PLA', 'PETG', 'ABS', 'TPU', 'PC', 'PA', 'PVA', 'HIPS']
        colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF', '#000000']
        
        for i in range(1000):
            # Create variety in the test data
            filament_type = filament_types[i % len(filament_types)]
            color = colors[i % len(colors)]
            format_type = 'bambu_v1' if i % 2 == 0 else 'bambu_v2'
            
            payload = generate_sample_payload(
                format_type=format_type,
                name=f'Test Filament {i:04d}',
                type=filament_type,
                color=color,
                remaining_weight=1000 - (i % 100),
                remaining_length=240 - (i % 50),
                nozzle_temp=200 + (i % 50),
                bed_temp=60 + (i % 40)
            )
            payloads.append(payload)
        
        return payloads
    
    def get_memory_usage_mb(self):
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def test_batch_decode_performance_1000_payloads(self, nfc_device, sample_payloads_1000):
        """
        Test batch decode performance with 1000 NFC payloads.
        
        Requirements:
        - All payloads decoded within performance threshold
        - No memory leaks
        - Total batch time under limit
        """
        # Record initial memory usage
        gc.collect()  # Force garbage collection before measurement
        initial_memory_mb = self.get_memory_usage_mb()
        
        # Measure batch decode performance
        start_time = time.time()
        
        results = nfc_device.batch_decode(sample_payloads_1000)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Record final memory usage
        gc.collect()  # Force garbage collection after operations
        final_memory_mb = self.get_memory_usage_mb()
        memory_increase_mb = final_memory_mb - initial_memory_mb
        
        # Validate results
        assert len(results) == 1000, f"Expected 1000 results, got {len(results)}"
        
        # Count successful decodes
        successful_decodes = sum(1 for result in results if result is not None)
        
        # All payloads should decode successfully (they are all valid test data)
        assert successful_decodes == 1000, f"Expected 1000 successful decodes, got {successful_decodes}"
        
        # Performance assertions
        avg_time_per_payload_ms = (total_time / 1000) * 1000
        
        print(f"\n=== Batch NFC Decode Performance Results ===")
        print(f"Total payloads: 1000")
        print(f"Successful decodes: {successful_decodes}")
        print(f"Total decode time: {total_time:.3f} seconds")
        print(f"Average time per payload: {avg_time_per_payload_ms:.3f} ms")
        print(f"Memory usage before: {initial_memory_mb:.2f} MB")
        print(f"Memory usage after: {final_memory_mb:.2f} MB")
        print(f"Memory increase: {memory_increase_mb:.2f} MB")
        print(f"=== Performance Thresholds ===")
        print(f"Max time per payload: {self.MAX_DECODE_TIME_PER_PAYLOAD_MS} ms")
        print(f"Max total batch time: {self.MAX_TOTAL_BATCH_TIME_SECONDS} seconds")
        print(f"Max memory increase: {self.MAX_MEMORY_INCREASE_MB} MB")
        
        # Assert performance thresholds
        assert total_time <= self.MAX_TOTAL_BATCH_TIME_SECONDS, \
            f"Batch decode took {total_time:.3f}s, exceeds threshold of {self.MAX_TOTAL_BATCH_TIME_SECONDS}s"
        
        assert avg_time_per_payload_ms <= self.MAX_DECODE_TIME_PER_PAYLOAD_MS, \
            f"Average decode time {avg_time_per_payload_ms:.3f}ms per payload exceeds threshold of {self.MAX_DECODE_TIME_PER_PAYLOAD_MS}ms"
        
        # Memory leak check
        assert memory_increase_mb <= self.MAX_MEMORY_INCREASE_MB, \
            f"Memory increased by {memory_increase_mb:.2f}MB, exceeds threshold of {self.MAX_MEMORY_INCREASE_MB}MB"
        
        # Validate sample results content
        sample_result = results[0]
        assert isinstance(sample_result, dict), "Decoded result should be a dictionary"
        assert 'name' in sample_result, "Result should contain 'name' field"
        assert 'type' in sample_result, "Result should contain 'type' field"
        assert 'remaining_weight' in sample_result, "Result should contain 'remaining_weight' field"
    
    def test_individual_decode_performance(self, nfc_device, sample_payloads_1000):
        """
        Test individual decode performance to verify single payload decode speed.
        """
        # Test with first 100 payloads for detailed timing
        test_payloads = sample_payloads_1000[:100]
        
        decode_times = []
        
        for payload in test_payloads:
            start_time = time.time()
            result = nfc_device.decode_payload(payload)
            end_time = time.time()
            
            decode_time_ms = (end_time - start_time) * 1000
            decode_times.append(decode_time_ms)
            
            assert result is not None, "Individual payload should decode successfully"
        
        avg_decode_time_ms = sum(decode_times) / len(decode_times)
        max_decode_time_ms = max(decode_times)
        min_decode_time_ms = min(decode_times)
        
        print(f"\n=== Individual Decode Performance ===")
        print(f"Tested payloads: {len(test_payloads)}")
        print(f"Average decode time: {avg_decode_time_ms:.3f} ms")
        print(f"Min decode time: {min_decode_time_ms:.3f} ms")
        print(f"Max decode time: {max_decode_time_ms:.3f} ms")
        
        assert avg_decode_time_ms <= self.MAX_DECODE_TIME_PER_PAYLOAD_MS, \
            f"Average individual decode time {avg_decode_time_ms:.3f}ms exceeds threshold"
    
    def test_memory_stability_repeated_batches(self, nfc_device, sample_payloads_1000):
        """
        Test memory stability across multiple batch decode operations.
        Ensures no cumulative memory leaks across repeated operations.
        """
        gc.collect()
        initial_memory_mb = self.get_memory_usage_mb()
        
        # Run batch decode 5 times
        for i in range(5):
            results = nfc_device.batch_decode(sample_payloads_1000)
            assert len(results) == 1000, f"Batch {i+1} should decode 1000 payloads"
            
            # Force garbage collection between batches
            gc.collect()
        
        final_memory_mb = self.get_memory_usage_mb()
        memory_increase_mb = final_memory_mb - initial_memory_mb
        
        print(f"\n=== Memory Stability Test (5 batches) ===")
        print(f"Initial memory: {initial_memory_mb:.2f} MB")
        print(f"Final memory: {final_memory_mb:.2f} MB")
        print(f"Memory increase: {memory_increase_mb:.2f} MB")
        
        # Allow for slightly higher memory increase for repeated operations
        max_repeated_memory_increase = self.MAX_MEMORY_INCREASE_MB * 1.5
        
        assert memory_increase_mb <= max_repeated_memory_increase, \
            f"Memory increased by {memory_increase_mb:.2f}MB after 5 batches, exceeds threshold of {max_repeated_memory_increase:.2f}MB"
    
    def test_concurrent_decode_operations(self, nfc_device, sample_payloads_1000):
        """
        Test performance when multiple decode operations are performed concurrently.
        """
        import threading
        import queue
        
        # Split payloads into 4 chunks for concurrent processing
        chunk_size = 250
        payload_chunks = [
            sample_payloads_1000[i:i + chunk_size] 
            for i in range(0, 1000, chunk_size)
        ]
        
        results_queue = queue.Queue()
        start_time = time.time()
        
        def decode_chunk(chunk, chunk_id):
            """Decode a chunk of payloads in a separate thread."""
            chunk_results = nfc_device.batch_decode(chunk)
            results_queue.put((chunk_id, chunk_results))
        
        # Start threads for concurrent decoding
        threads = []
        for i, chunk in enumerate(payload_chunks):
            thread = threading.Thread(target=decode_chunk, args=(chunk, i))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect results
        all_results = []
        while not results_queue.empty():
            chunk_id, chunk_results = results_queue.get()
            all_results.extend(chunk_results)
        
        print(f"\n=== Concurrent Decode Performance ===")
        print(f"Total payloads: 1000 (4 chunks of 250)")
        print(f"Total concurrent decode time: {total_time:.3f} seconds")
        print(f"Successful decodes: {sum(1 for r in all_results if r is not None)}")
        
        assert len(all_results) == 1000, f"Expected 1000 total results, got {len(all_results)}"
        assert total_time <= self.MAX_TOTAL_BATCH_TIME_SECONDS, \
            f"Concurrent decode took {total_time:.3f}s, exceeds threshold"


if __name__ == "__main__":
    # Allow running the test directly for development
    pytest.main([__file__, "-v", "-s"])