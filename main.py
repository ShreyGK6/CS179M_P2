import os
import numpy as np
from inputValidator import validate_input_file
from kNearestCluster import createDronePaths
from decisionTimer import start_decision_timer, stop_decision_timer, timeout_ocurred
from waitUntil7am import check_if_7am

#this will write the solutions to files
def write_solution_file(points, base_filename, completeRoute, drone_count, output_folder):
    os.makedirs(output_folder, exist_ok = True)

    for i,route_info in enumerate(completeRoute, start=1):
        route = route_info["Route"]
        distance = route_info["Distance"]

        route_indices= []
        for point in route:
            idx = np.where((points == point).all(axis = 1)) [0][0] + 1
            route_indices.append(str(idx))

        filename = f"{base_filename}_{i}_SOLUTION_{int(distance)}.txt"
        file_path = os.path.join(output_folder, filename)
        with open(file_path, 'w') as f:
            f.write("\n".join(route_indices))
        print(f" -> Wrote{file_path}")

def main():
    check_if_7am()

    print("=== Compute Possible Solutions ===")
    filename = input("\nEnter the name of file: ").strip()
    input_folder = "TextFiles"
    output_folder = "OutputRoutesFolder"
    os.makedirs(output_folder, exist_ok = True)
    file_path = os.path.join(input_folder, filename)

    #validates the inputs
    try:
        points = validate_input_file(file_path)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return
   
    node_count = len(points)
    print(f"\nThere are {node_count} nodes: Solutions will be available shortly...\n")

    all_results = {}

    for k in range(1,5):
        totalDistance, completeRoute, OFScore = createDronePaths(points, k)
        all_results[k] = (totalDistance, completeRoute, OFScore)

        print(f"{k}) If you use {k} drones(s), the total route will be {totalDistance:.1f} meters")
        for i, route_info in enumerate(completeRoute, start = 1):
            pad = route_info["DronePad"]
            size = route_info["Size of Cluster"]
            dist = route_info["Distance"]
            print(f"    Landing Pad {i} should be at [{pad[0]:.0f}, {pad[1]:.0f}], " f"serving {size} locations, route is {dist:.1f} meters")
        #print(f"    Objective Function Score: {OFScore:.2f}\n")    #commented out OFScore so that only necessary info is shown

    print("You have 5 minutes to make your decision.\n")
    start_decision_timer(300)
    choice = None

    while choice not in [1, 2, 3, 4]:
        if timeout_ocurred:
            #program should exit on its own
            return
        try:
            choice = int(input("Please select your choice 1 to 4: ").strip())
        except ValueError:
            continue
        stop_decision_timer()
   
    totalDistance, completeRoute, _ = all_results[choice]
    base_filename = os.path.splitext(filename)[0]

    print("\nWriting solution files to disk...")
    write_solution_file(points, base_filename, completeRoute, choice, output_folder)

    #gokul add the vizualization part here

    print("\n Summary:")
    print(f" -Drones used: {choice}")
    print(f" -Total combined route distance: {totalDistance:.1f} meters")
    print(f" -Output files saved in: '{output_folder}'")
    print("\nAll done. Have a great day, Mr. Keogh!")

if __name__ == "__main__":
    main()