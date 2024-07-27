import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import math
import json
import os

class DroneControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Control")

        self.current_heading = tk.DoubleVar()
        self.last_received_heading = 0.0
        self.current_heading.set(math.degrees(self.last_received_heading))

        self.current_lat = 0.0
        self.current_lon = 0.0
        self.new_lat = tk.DoubleVar()
        self.new_lon = tk.DoubleVar()

        self.grid_size = 5
        self.cell_size = 100
        self.drone_icon = None

        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.create_grid()
        self.create_widgets(frame)
        self.get_initial_telemetry()

    def create_grid(self):
        """Create the grid and drone icon on the canvas."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

        self.drone_icon = self.canvas.create_oval(self.cell_size * 2 + 20, self.cell_size * 2 + 20, self.cell_size * 3 - 20, self.cell_size * 3 - 20, fill="blue")
        self.canvas.tag_bind(self.drone_icon, '<B1-Motion>', self.drag_drone)
        self.canvas.tag_bind(self.drone_icon, '<ButtonRelease-1>', self.snap_to_grid)

    def create_widgets(self, frame):
        """Create UI widgets."""
        btn_mission_pause = tk.Button(frame, text="Mission Pause", command=self.on_mission_pause_click)
        btn_mission_pause.grid(row=self.grid_size, column=0)

        btn_guided = tk.Button(frame, text="Guided", command=self.on_guided_click)
        btn_guided.grid(row=self.grid_size, column=2)

        self.slider = ttk.Scale(frame, from_=0, to=360, orient="horizontal", variable=self.current_heading)
        self.slider.grid(row=self.grid_size + 1, column=0, columnspan=3)

        tk.Label(frame, text="Heading").grid(row=self.grid_size + 2, column=0, columnspan=3)
        self.heading_label = tk.Label(frame, text="0.0°")
        self.heading_label.grid(row=self.grid_size + 3, column=0, columnspan=3)
        self.current_heading.trace("w", self.update_heading_label)

        tk.Label(frame, text="New Latitude").grid(row=self.grid_size + 4, column=0)
        self.lat_entry = tk.Entry(frame, textvariable=self.new_lat)
        self.lat_entry.grid(row=self.grid_size + 4, column=1)

        tk.Label(frame, text="New Longitude").grid(row=self.grid_size + 5, column=0)
        self.lon_entry = tk.Entry(frame, textvariable=self.new_lon)
        self.lon_entry.grid(row=self.grid_size + 5, column=1)

        self.confirm_button = tk.Button(frame, text="Confirm", command=self.confirm_waypoint)
        self.confirm_button.grid(row=self.grid_size + 6, column=0, columnspan=3)

    def update_heading_label(self, *args):
        """Update the heading label based on the slider value."""
        self.heading_label.config(text=f"{self.current_heading.get():.1f}°")

    def drag_drone(self, event):
        """Handle dragging the drone icon."""
        self.canvas.coords(self.drone_icon, event.x - 20, event.y - 20, event.x + 20, event.y + 20)

    def snap_to_grid(self, event):
        """Snap the drone icon to the nearest grid cell."""
        x, y = event.x, event.y
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)

        new_x = col * self.cell_size + self.cell_size / 2
        new_y = row * self.cell_size + self.cell_size / 2

        self.canvas.coords(self.drone_icon, new_x - 20, new_y - 20, new_x + 20, new_y + 20)

        self.on_grid_click(row, col)

    def on_grid_click(self, i, j):
        """Handle clicking on the grid to set a new waypoint."""
        print(f"Grid cell ({i}, {j}) clicked")
        distance = 0.0000003
        half_grid = self.grid_size // 2

        delta_lat = (i - half_grid) * distance
        delta_lon = (j - half_grid) * distance

        current_lat = self.current_lat
        current_lon = self.current_lon

        new_lat = current_lat + delta_lat
        new_lon = current_lon + delta_lon

        self.new_lat.set(new_lat)
        self.new_lon.set(new_lon)

    def confirm_waypoint(self):
        """Confirm and send the new waypoint to the drone."""
        lat = self.new_lat.get()
        lon = self.new_lon.get()
        heading = math.radians(self.current_heading.get())

        self.send_waypoint_command(lat, lon, heading)

    def on_mission_pause_click(self):
        """Handle the mission pause button click."""
        command = self.build_command("mission_pause", [])
        threading.Thread(target=self.run_command, args=(command,)).start()

    def on_guided_click(self):
        """Handle the guided mode button click."""
        command = self.build_command("guided", [])
        threading.Thread(target=self.run_command, args=(command,)).start()

    def send_waypoint_command(self, lat, lon, heading_radians):
        """Send a waypoint command to the drone."""
        args = [
            f"latitude={lat}",
            f"longitude={lon}",
            "altitude_agl=100.0",
            "ground_speed=5.0",
            "vertical_speed=1.0",
            f"heading={heading_radians}"
        ]
        command = self.build_command("waypoint", args)
        print("Command to execute:", " ".join(command))
        threading.Thread(target=self.run_command, args=(command,)).start()

    def build_command(self, command_type, additional_args):
        """Build the command to be run based on the command type and additional arguments."""
        classpath = os.getenv('UGCS_CLASSPATH', 'path_to_your_classpath')
        java_command = os.getenv('JAVA_COMMAND', 'java')

        command = [java_command, "-cp", classpath, "com.ugcs.ucs.client.samples.SendCommand", "-c", command_type] + additional_args + ["EMU-101"]
        return command

    def run_command(self, command):
        """Run a command using subprocess."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def get_initial_telemetry(self):
        """Get the initial telemetry data from the drone."""
        try:
            command = self.build_command("FilteredListenTelemetry", ["-t", "1"])
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout.strip().split('\n')
            lat, lon, heading = None, None, None
            for line in output:
                if "latitude" in line:
                    lat = float(line.split('=')[1].strip())
                elif "longitude" in line:
                    lon = float(line.split('=')[1].strip())
                elif "heading" in line:
                    heading = float(line.split('=')[1].strip())

            if lat is not None and lon is not None and heading is not None:
                self.current_lat = lat
                self.current_lon = lon
                self.last_received_heading = heading
                self.current_heading.set(math.degrees(heading))
                self.update_coordinates()
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def update_coordinates(self):
        """Update the coordinates and save them to a JSON file."""
        coordinates = {
            "lat": self.current_lat,
            "lon": self.current_lon
        }
        with open('coordinates.json', 'w') as f:
            json.dump(coordinates, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = DroneControlApp(root)
    root.mainloop()
