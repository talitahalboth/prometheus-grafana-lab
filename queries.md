# Workout Performance Overview Dashboard

---
**Gauge machine weights**

**Description**: Shows the weight of each machine

**Panel Type**: Gauge

**Legend**: Custom `{{machine_id}}`

**PromQL Query:**

`egym_machine_weight_kg`


---
**Workout Mix**

**Description**: Shows the ratio of 'individual' vs 'auto' workouts over the selected time range.

**Panel Type:** Pie Chart

**PromQL Query:**

`sum by (workout_type) (increase(egym_workout_sessions_total[$__range]))`


---
**Workout Rate (Sessions/min)**

**Description**: Shows the number of workout sessions being started per minute (averaged over the 
last 5 minutes).

**Panel Type:** Time series

**PromQL Query:**

`sum(rate(egym_workout_sessions_total{workout_type=~"$workout_type"}[$__interval]) * 60)`


---
**95th Percentile Workout Duration**

**Description**: Shows the 95th percentile duration for workouts, helping you understand the typical 
"long" session for most users.

**Panel Type:** Time series

**Unit**: Seconds

**PromQL Query:**

`histogram_quantile(0.95, sum(rate(egym_workout_duration_seconds_bucket{workout_type=~"$workout_type"}[5m])) by (le, workout_type))`


---
**Workout Duration Heatmap**

**Description**: Visualizes the full distribution of workout durations over time. Great for spotting shifts in user behavior.

**Panel Type:** Heatmap

**PromQL Query:**

`sum by (le) (rate(egym_workout_duration_seconds_bucket{workout_type=~"$workout_type"}[5m]))`


# Machine & System Health Dashboard

---
**Percentiles API Latency** 
**Description**:  Shows the P99, P90 and Median latency for our api


**Panel Type:** Time series

**Unit:** seconds

**PromQL Query:**

`histogram_quantile(0.99, sum(rate(egym_api_latency_seconds_bucket{endpoint=~"$endpoint"}[5m])) by (le, endpoint))`
`histogram_quantile(0.90, sum(rate(egym_api_latency_seconds_bucket{endpoint=~"$endpoint"}[5m])) by (le, endpoint))`
`histogram_quantile(0.50, sum(rate(egym_api_latency_seconds_bucket{endpoint=~"$endpoint"}[5m])) by (le, endpoint))`


---
**Average API Latency**

**Description**:  Baseline overview of the typical performance of your API endpoints.

**Panel Type:** Time series

**Unit:** seconds

**PromQL Query:**

```
sum(rate(egym_api_latency_seconds_sum{endpoint=~"$endpoint"}[5m])) by (endpoint)`
/
sum(rate(egym_api_latency_seconds_count{endpoint=~"$endpoint"}[5m])) by (endpoint)
```

---
**Name: Application Errors**

**Data source**: Your Prometheus source

**Query**: `changes(egym_application_errors_total[1m]) > 3`

**Text**: `Error: {{ error_type }}`




---
**Application Error Rate (Errors/min)**

**Description**:  Tracks the rate of critical application errors.

**Panel Type**: Time series

**PromQL Query:**

`sum(rate(egym_application_errors_total[1m]) * 60)`





