import time
import random
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary

def main():
    """
    This function starts a metrics server and simulates a more complex application
    to demonstrate various Prometheus metric types and Grafana features.
    """
    # --- 1. Start the Prometheus Metrics Server ---
    # This will expose a /metrics endpoint on port 8081.
    try:
        start_http_server(8081)
        print("Prometheus metrics server started on http://localhost:8081")
    except OSError as e:
        print(f"Error starting server: {e}")
        print("Another process might be using port 8081.")
        return

    # --- 2. Define Your Metrics ---

    # COUNTER: For events that only increase.
    # We've added a 'workout_type' label to distinguish between different kinds of workouts.
    # This is great for showing how to use 'sum by (label)' in PromQL.
    workout_counter = Counter(
        'egym_workout_sessions_total',
        'Total number of workout sessions started',
        ['workout_type']
    )

    # GAUGE: For values that can go up and down.
    # We'll simulate multiple machines to show how labels work.
    # This is a perfect source for a Grafana 'variable' dropdown.
    machine_weight_gauge = Gauge(
        'egym_machine_weight_kg',
        'Current weight setting of the machine',
        ['machine_id']
    )

    # HISTOGRAM: For tracking the distribution of values, like latency.
    # We've added custom buckets to better suit our data range.
    # The 'le' (less than or equal to) label is added automatically.
    workout_duration_histogram = Histogram(
        'egym_workout_duration_seconds',
        'Histogram for the duration of a workout session.',
        ['workout_type'],
        buckets=[5, 10, 15, 20, 25, 30, 45, 60] # Custom buckets for better resolution
    )

    # HISTOGRAM for API Latency. This replaces the problematic Summary.
    # We use Histograms to calculate quantiles (p50, p90, p99) in Grafana/Prometheus.
    api_latency_histogram = Histogram(
        'egym_api_latency_seconds',
        'Histogram for the latency of an API call.',
        ['endpoint'],
        # Buckets suitable for short API latencies in seconds
        buckets=[0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5]
    )
    
    # COUNTER for ERRORS: This will be used to demonstrate Grafana annotations.
    # You can set up an alert in Prometheus/Grafana that triggers when the rate of errors
    # is greater than 0, and that alert can create an annotation on your dashboards.
    error_counter = Counter(
        'egym_application_errors_total',
        'Total number of simulated application errors',
        ['error_type']
    )


    # --- 3. Simulate a Running Application ---
    print("Application running. Metrics are being updated...")
    print("Press Ctrl+C to exit.")

    machine_ids = ['A101', 'A102', 'B202', 'C303']
    workout_types = ['individual', 'auto']
    endpoints = ['/api/user', '/api/workouts']
    
    # Initialize gauges for all machines
    for mid in machine_ids:
        machine_weight_gauge.labels(machine_id=mid).set(20.0)

    try:
        while True:
            # --- Simulate a workout session ---
            workout_type = random.choice(workout_types)
            workout_counter.labels(workout_type=workout_type).inc()
            print(f"New '{workout_type}' workout started!")

            # Observe a workout duration for the histogram
            # We introduce different distributions based on the label to make percentiles dynamic.
            if workout_type == 'auto':
                # 'auto' workouts are simulated to be faster and more consistent
                duration = max(0, random.gauss(10, 2)) # Avg 10s, std dev 2
            else: # 'individual'
                # 'individual' workouts are simulated to be longer and more variable
                duration = max(0, random.gauss(25, 8)) # Avg 25s, std dev 8
            
            workout_duration_histogram.labels(workout_type=workout_type).observe(duration)
            print(f"Workout duration was {duration:.2f} seconds.")

            # --- Simulate weight changes on a random machine ---
            chosen_machine = random.choice(machine_ids)
            new_weight = random.uniform(10.0, 100.0)
            machine_weight_gauge.labels(machine_id=chosen_machine).set(new_weight)
            print(f"Machine {chosen_machine} weight set to: {new_weight:.2f} kg")

            # --- Simulate API latency ---
            chosen_endpoint = random.choice(endpoints)
            latency = max(0, random.gauss(0.5, 0.2)) # Simulate 0.5s latency
            api_latency_histogram.labels(endpoint=chosen_endpoint).observe(latency)
            print(f"API call to {chosen_endpoint} took {latency:.2f} seconds.")

            # --- Simulate a random error event ---
            if random.random() < 0.1: # 10% chance of an error
                error_counter.labels(error_type='database_timeout').inc()
                print("!!! A simulated database timeout error occurred! !!!")

            print("-" * 20)
            time.sleep(random.uniform(1, 5)) # Sleep for a random interval

    except KeyboardInterrupt:
        print("\nShutting down.")

if __name__ == '__main__':
    main()
