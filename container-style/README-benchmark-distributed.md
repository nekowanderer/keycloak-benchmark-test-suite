# Distributed Benchmarking for Keycloak: Why Use Multiple EC2 Instances?

## Background

When running performance benchmarks against Keycloak, especially at high loads (e.g., 300+ new users per second), you may encounter issues where the load generator stalls or fails to establish new connections. This is often due to the exhaustion of available TCP ports on the load generator host, caused by a large number of connections in the `TIME_WAIT` state.

## Why Does This Happen?

- **TCP TIME_WAIT State:**
  - Every closed TCP connection enters the `TIME_WAIT` state for a short period (typically 60 seconds).
  - Each connection in `TIME_WAIT` occupies a local ephemeral port, which cannot be reused until the state expires.
  - The number of available ephemeral ports is limited (usually a few tens of thousands per host).
  - At high connection rates, the host quickly runs out of available ports, causing new connections to fail or stall.

- **Resource Bottlenecks:**
  - In addition to port exhaustion, a single host may also hit CPU, memory, or network bandwidth limits under heavy load.

## Limitation of Docker Compose Scale on a Single Host

- Using `docker compose up --scale benchmark=N` to simulate multiple clients only distributes the load across multiple containers **on the same physical machine**.
- All containers still share the same host's network stack, ephemeral port range, CPU, and network bandwidth.
- This means you will still hit the same physical limitations (TIME_WAIT, port exhaustion, CPU, bandwidth) as a single process would.

## Hardware Upgrade vs. Multi-Host Distribution

- **Upgrading Single Host Hardware:**
  - Increases the limits for CPU, memory, and network bandwidth.
  - However, the ephemeral port range and TIME_WAIT limitations remain, and you will eventually hit a ceiling.
  - Suitable for small to medium scale, but not truly scalable for very high loads.

- **Using Multiple Hosts (e.g., Multiple TeamCity Agents):**
  - Each host has its own independent ephemeral port range, CPU, and network resources.
  - Load and resource usage are distributed, allowing for near-linear scalability.
  - This is the only way to truly overcome the single-host bottlenecks and achieve large-scale, realistic benchmarking.

**Conclusion:**
- While upgrading hardware can help to a certain extent, distributing the load across multiple hosts (e.g., multiple TeamCity agents or EC2 instances) provides a much more significant and scalable improvement for high-load benchmarking scenarios.

## Solution: Distributed Load Generation with Multiple EC2 Instances

- **Port Range is Per Host:**
  - By distributing the load across multiple EC2 instances, each instance has its own set of ephemeral ports.
  - This allows the total number of concurrent connections to scale linearly with the number of hosts.

- **Resource Distribution:**
  - CPU, memory, and network usage are also distributed, reducing the risk of bottlenecks on any single machine.

- **Network Proximity:**
  - Deploying load generators in the same AWS region as Keycloak reduces network latency and simulates real-world conditions more accurately.
  - Alternatively, you can deploy in different regions to simulate user latency from various geographies.

## Official Recommendation

Keycloak's official documentation recommends using Ansible and EC2 for distributed benchmarking when a single load generator is insufficient. This approach helps avoid connection stalls and ensures more reliable, scalable, and realistic performance testing.

## References
- [Keycloak Benchmark Documentation](https://www.keycloak.org/benchmark/)
- [Linux TCP TIME_WAIT Tuning](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/overview.html)
