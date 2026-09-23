# Mystery Delivery System


## Overview


The Mystery Delivery System is a Python-based logistics simulation for a fictional delivery company called FastBox.


The system simulates one day of delivery operations involving:


- Warehouses

- Delivery agents

- Packages

- Customer destinations


The application determines which agent should handle each package, calculates an efficient delivery route, simulates the deliveries, calculates agent performance, and generates a final `report.json`.


---


## Project Structure


```text

Mystery-Delivery-System/

│
├── main.py
├── data.json
├── report.json
├── README.md
│
└── test_cases/
    ├── test_case_1.json
    ├── test_case_2.json
    ├── test_case_3.json
    ├── test_case_4.json
    ├── test_case_5.json
    ├── test_case_6.json
    ├── test_case_7.json
    ├── test_case_8.json
    ├── test_case_9.json
    └── test_case_10.json
```


---


## How the System Works


The application follows these steps:


1. Read the input JSON file.
2. Normalize the warehouse, agent, and package data.
3. Calculate Euclidean distances.
4. Assign each package to the nearest delivery agent.
5. Find an efficient delivery order for each agent.
6. Simulate the deliveries.
7. Calculate total distance and efficiency for each agent.
8. Determine the best agent.
9. Generate the final `report.json`.

---


## Distance Calculation


The system uses Euclidean distance between two points.


```text

Distance = √((x2 - x1)² + (y2 - y1)²)

```


This distance calculation is used for both package assignment and delivery route calculation.


---


## Package Assignment


Each package is assigned to the delivery agent whose initial location is closest to the package's warehouse.


For each package, the program calculates:


```text

Agent Location → Warehouse Location

```


The agent with the smallest distance to the warehouse is assigned the package.


If two agents are at the same distance from the warehouse, the agent with the smaller agent ID is selected.


---


## Delivery Simulation


After packages are assigned, each agent delivers the packages assigned to them.


For each package, the route is:


```text

Current Agent Location → Warehouse → Customer

```


After completing a delivery, the agent's current location becomes the customer's destination.


For example:


```text

Agent

  ↓

Warehouse 1

  ↓

Customer 1

  ↓

Warehouse 2

  ↓

Customer 2

```


The total distance travelled is calculated by adding the distance covered for each part of the delivery route.


---


## Delivery Route Optimization


The order in which packages are delivered can affect the total distance travelled by an agent.


Therefore, the program does not simply follow the package order given in the input.


For each agent, the program finds the delivery order that results in the minimum total travel distance for all packages assigned to that agent.


---


## Efficiency Calculation


Agent efficiency is calculated using:


```text

Efficiency = Total Distance / Packages Delivered

```


This represents the average distance travelled per delivered package.


For an agent with no assigned packages:


```text

Packages Delivered = 0

Total Distance = 0

Efficiency = 0

```


---


## Best Agent


The program identifies the best agent based on the lowest efficiency value among agents who delivered at least one package.


A lower efficiency value means less distance travelled per delivered package.


---


## Input Handling


The program normalizes the input data before processing so that the different input structures used by the test cases can be handled consistently.


The program supports:


- List-style and dictionary-style warehouse data

- List-style and dictionary-style agent data

- `warehouse_id` and `warehouse` package fields


---


## Assumptions


The assignment leaves some implementation details open, so the following assumptions were used:


- Euclidean distance is used for all distance calculations.

- Package assignment is based on the agent's initial location and the package's warehouse.

- The agent must visit the warehouse before travelling to the customer.

- After completing a delivery, the agent remains at the customer's destination.

- The delivery order is optimized to minimize total travel distance.

- If two agents are equally close to a warehouse, the agent with the smaller agent ID is selected.

- Agents with zero deliveries are excluded when selecting the best agent.

- The final output is always saved to `report.json`.


---


## Running the Program


### Run with the default input


```bash

python main.py

```


This uses `data.json` as the input file and generates `report.json`.


### Run with a specific test case


```bash

python main.py --input test_cases/test_case_1.json

```


The result is written to `report.json`.


The same format can be used for the remaining test cases.


---


## Output


The generated `report.json` contains the performance information for each delivery agent.


The report includes:


- Number of packages delivered

- Total distance travelled

- Efficiency

- Best agent


---


## Testing


The project contains 10 test cases with different combinations of warehouses, agents, and packages.


Each test case was executed using the `--input` option.


All 10 test cases completed successfully.


| Test Case | Result |

|-----------|--------|

| Test Case 1 | PASS |

| Test Case 2 | PASS |

| Test Case 3 | PASS |

| Test Case 4 | PASS |

| Test Case 5 | PASS |

| Test Case 6 | PASS |

| Test Case 7 | PASS |

| Test Case 8 | PASS |

| Test Case 9 | PASS |

| Test Case 10 | PASS |


---


## Challenges and Solutions


### Different Input Formats


Some test cases use different structures for warehouses, agents, and package warehouse references.


**Solution:**

The program normalizes the input data before processing so that the same delivery logic can be used across the supported formats.


### Delivery Order


Processing packages strictly in input order does not always produce the shortest route.


**Solution:**

The program searches for the delivery order that minimizes the total travel distance for each agent.


### Agents with No Packages


Some agents may not receive any packages.


**Solution:**

These agents are still included in the final report with zero packages, zero distance, and zero efficiency.


---


## Technologies Used


- Python

- JSON

- `math`

- `argparse`


No external Python packages are required.


---


## Conclusion


The project implements the complete delivery simulation workflow, including input processing, package assignment, route optimization, delivery simulation, agent performance calculation, and report generation.
