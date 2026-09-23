import json
import math
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "--input",
    default="data.json",
    help="Path to input JSON file"
)

args = parser.parse_args()

# reading the input data
with open(args.input, "r") as file:
    data = json.load(file)


# normalizing warehouses
if isinstance(data["warehouses"], dict):
    warehouses = [
        {
            "id": warehouse_id,
            "location": location
        }
        for warehouse_id, location in data["warehouses"].items()
    ]
else:
    warehouses = data["warehouses"]


# normalizing agents
if isinstance(data["agents"], dict):
    agents = [
        {
            "id": agent_id,
            "location": location
        }
        for agent_id, location in data["agents"].items()
    ]
else:
    agents = data["agents"]


# normalizing packages
packages = []

for package in data["packages"]:

    warehouse_id = package.get(
        "warehouse_id",
        package.get("warehouse")
    )

    if warehouse_id is None:
        raise ValueError(
            f"Package {package['id']} has no warehouse"
        )

    packages.append({
        "id": package["id"],
        "warehouse_id": warehouse_id,
        "destination": package["destination"]
    })


# calculating euclidean distance
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2
    )

    return distance


# finding the nearest agent
def find_nearest_agent(package, agents, warehouses):
    warehouse_id = package["warehouse_id"]

    warehouse_location = None

    for warehouse in warehouses:
        if warehouse["id"] == warehouse_id:
            warehouse_location = warehouse["location"]
            break

    if warehouse_location is None:
        raise ValueError(
            f"Warehouse {warehouse_id} not found"
        )

    nearest_agent = None
    shortest_distance = float("inf")

    for agent in agents:
        distance = calculate_distance(
            agent["location"],
            warehouse_location
        )

        if (
            distance < shortest_distance
            or (
                math.isclose(distance, shortest_distance)
                and (
                    nearest_agent is None
                    or agent["id"] < nearest_agent
                )
            )
        ):
            shortest_distance = distance
            nearest_agent = agent["id"]

    return nearest_agent


# assigning packages to agents
assignments = {}

for agent in agents:
    assignments[agent["id"]] = []

for package in packages:
    nearest_agent = find_nearest_agent(
        package,
        agents,
        warehouses
    )

    assignments[nearest_agent].append(
        package["id"]
    )


# calculating distance for a delivery route
def calculate_route_distance(
    agent_location,
    package_ids,
    packages,
    warehouses
):
    current_location = agent_location
    total_distance = 0

    package_map = {
        package["id"]: package
        for package in packages
    }

    for package_id in package_ids:

        if package_id not in package_map:
            raise ValueError(
                f"Package {package_id} not found"
            )

        package = package_map[package_id]

        warehouse_location = None

        for warehouse in warehouses:
            if warehouse["id"] == package["warehouse_id"]:
                warehouse_location = warehouse["location"]
                break

        if warehouse_location is None:
            raise ValueError(
                f"Warehouse "
                f"{package['warehouse_id']} "
                f"not found"
            )

        distance_to_warehouse = calculate_distance(
            current_location,
            warehouse_location
        )

        distance_to_customer = calculate_distance(
            warehouse_location,
            package["destination"]
        )

        total_distance += (
            distance_to_warehouse
            + distance_to_customer
        )

        current_location = package["destination"]

    return total_distance


# finding the best delivery route
def find_best_route(
    agent_location,
    package_ids,
    packages,
    warehouses
):
    if not package_ids:
        return [], 0

    if len(package_ids) == 1:
        distance = calculate_route_distance(
            agent_location,
            package_ids,
            packages,
            warehouses
        )

        return package_ids, distance

    package_map = {
        package["id"]: package
        for package in packages
    }

    ids = list(package_ids)
    number_of_packages = len(ids)

    dp = {}
    routes = {}

    for i in range(number_of_packages):

        package_id = ids[i]
        package = package_map[package_id]

        warehouse_location = None

        for warehouse in warehouses:
            if warehouse["id"] == package["warehouse_id"]:
                warehouse_location = warehouse["location"]
                break

        if warehouse_location is None:
            raise ValueError(
                f"Warehouse "
                f"{package['warehouse_id']} "
                f"not found"
            )

        distance_to_warehouse = calculate_distance(
            agent_location,
            warehouse_location
        )

        distance_to_customer = calculate_distance(
            warehouse_location,
            package["destination"]
        )

        total_distance = (
            distance_to_warehouse
            + distance_to_customer
        )

        mask = 1 << i

        dp[(mask, i)] = total_distance
        routes[(mask, i)] = [package_id]

    for mask_size in range(1, number_of_packages + 1):

        for mask in range(1 << number_of_packages):

            if mask.bit_count() != mask_size:
                continue

            for last in range(number_of_packages):

                state = (mask, last)

                if state not in dp:
                    continue

                current_distance = dp[state]
                current_route = routes[state]

                current_package = package_map[
                    ids[last]
                ]

                current_location = (
                    current_package["destination"]
                )

                for next_index in range(
                    number_of_packages
                ):

                    if mask & (1 << next_index):
                        continue

                    next_package = package_map[
                        ids[next_index]
                    ]

                    next_warehouse = None

                    for warehouse in warehouses:

                        if (
                            warehouse["id"]
                            == next_package["warehouse_id"]
                        ):
                            next_warehouse = warehouse["location"]
                            break

                    if next_warehouse is None:
                        raise ValueError(
                            f"Warehouse "
                            f"{next_package['warehouse_id']} "
                            f"not found"
                        )

                    distance_to_warehouse = calculate_distance(
                        current_location,
                        next_warehouse
                    )

                    distance_to_customer = calculate_distance(
                        next_warehouse,
                        next_package["destination"]
                    )

                    travel_distance = (
                        distance_to_warehouse
                        + distance_to_customer
                    )

                    new_distance = (
                        current_distance
                        + travel_distance
                    )

                    new_mask = (
                        mask
                        | (1 << next_index)
                    )

                    new_state = (
                        new_mask,
                        next_index
                    )

                    new_route = (
                        current_route
                        + [ids[next_index]]
                    )

                    if new_state not in dp:

                        dp[new_state] = new_distance
                        routes[new_state] = new_route

                    elif (
                        new_distance
                        < dp[new_state]
                    ):

                        dp[new_state] = new_distance
                        routes[new_state] = new_route

    full_mask = (
        1 << number_of_packages
    ) - 1

    best_distance = float("inf")
    best_route = None

    for last in range(number_of_packages):

        state = (
            full_mask,
            last
        )

        if state not in dp:
            continue

        if dp[state] < best_distance:
            best_distance = dp[state]
            best_route = routes[state]

    return best_route, best_distance


# simulating deliveries
def simulate_agent(
    agent,
    package_ids,
    packages,
    warehouses
):
    best_route, total_distance = find_best_route(
        agent["location"],
        package_ids,
        packages,
        warehouses
    )

    current_location = agent["location"]

    package_map = {
        package["id"]: package
        for package in packages
    }

    for package_id in best_route:

        package = package_map[package_id]

        warehouse_location = None

        for warehouse in warehouses:

            if warehouse["id"] == package["warehouse_id"]:
                warehouse_location = warehouse["location"]
                break

        distance_to_warehouse = calculate_distance(
            current_location,
            warehouse_location
        )

        distance_to_customer = calculate_distance(
            warehouse_location,
            package["destination"]
        )

        current_location = package["destination"]

    return {
        "packages_delivered": len(best_route),
        "total_distance": total_distance,
        "final_location": current_location,
        "route": best_route
    }


# simulating all agents
agent_results = {}

for agent in agents:

    agent_id = agent["id"]

    result = simulate_agent(
        agent,
        assignments[agent_id],
        packages,
        warehouses
    )

    agent_results[agent_id] = result


# generating the final report
report = {}

for agent_id, result in agent_results.items():

    packages_delivered = result["packages_delivered"]
    total_distance = result["total_distance"]

    if packages_delivered > 0:
        efficiency = (
            total_distance / packages_delivered
        )
    else:
        efficiency = 0

    report[agent_id] = {
        "packages_delivered": packages_delivered,
        "total_distance": round(
            total_distance,
            2
        ),
        "efficiency": round(
            efficiency,
            2
        )
    }


# finding the best agent
agents_with_packages = [
    agent_id
    for agent_id in report
    if report[agent_id]["packages_delivered"] > 0
]

if agents_with_packages:

    best_agent = min(
        agents_with_packages,
        key=lambda agent_id: (
            report[agent_id]["efficiency"],
            report[agent_id]["total_distance"],
            agent_id
        )
    )

else:
    best_agent = None

report["best_agent"] = best_agent


# validating the result
total_delivered = sum(
    result["packages_delivered"]
    for result in report.values()
    if isinstance(result, dict)
)

if total_delivered != len(packages):
    raise ValueError(
        f"Package count mismatch: "
        f"{total_delivered} delivered, "
        f"{len(packages)} expected"
    )


# saving the report
with open("report.json", "w") as file:
    json.dump(
        report,
        file,
        indent=4
    )

# displaying the final result
print("\n========== DELIVERY REPORT ==========\n")

for agent in agents:

    agent_id = agent["id"]
    result = report[agent_id]

    print(f"{agent_id}:")
    print(
        f"  Packages Delivered: "
        f"{result['packages_delivered']}"
    )
    print(
        f"  Total Distance: "
        f"{result['total_distance']:.2f}"
    )
    print(
        f"  Efficiency: "
        f"{result['efficiency']:.2f}"
    )
    print()

print(
    f"Best Agent: {report['best_agent']}"
)

print("\nReport saved to report.json")