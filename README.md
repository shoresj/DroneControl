# 🚁 Drone Control Application

![Drone Control](https://img.shields.io/badge/Drone-Control-blue)
![UGCS SDK](https://img.shields.io/badge/UGCS-SDK-important)

A GUI-based drone control application written in Python using the Tkinter library. This application allows users to control a drone, manage its waypoints, and visualize its position on a grid. The application is designed to work seamlessly with the UGCS SDK.

## 🌟 Features

- **Drone Position Visualization:** Visualize the drone's position on a grid.
- **Waypoint Management:** Set new latitude and longitude waypoints.
- **Mission Control:** Pause and resume missions, switch to guided mode.
- **Heading Adjustment:** Adjust the drone's heading using a slider.
- **UGCS SDK Integration:** Fully integrated with UGCS SDK for executing drone commands.

## 🛠️ Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Java (for running UGCS SDK commands)
- UGCS SDK

## 📦 Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/shoresj/DroneControl.git
    cd DroneControl
    ```

2. **Install Dependencies:**
    Ensure Java is installed. If not, download and install it from [here](https://www.oracle.com/java/technologies/javase-downloads.html).

3. **Set Environment Variables:**
    Set the following environment variables in your system:
    - `UGCS_CLASSPATH`: The classpath for the UGCS SDK.
    - `JAVA_COMMAND`: The path to the Java executable (usually just `java` if it's in your PATH).

    For example, on Unix-like systems, you can add these to your `.bashrc` or `.zshrc`:
    ```sh
    export UGCS_CLASSPATH="/path/to/ugcs-java-sdk/*"
    export JAVA_COMMAND="java"
    ```

    On Windows, set the environment variables through the System Properties.

4. **Run the Application:**
    ```sh
    python drone_control.py
    ```

## 🚀 Usage

1. **Start the Application:**
    Run the script as shown above. The main window of the application will open.

2. **Visualize the Drone's Position:**
    The grid on the left side of the window represents the area where the drone can move. The blue circle represents the drone.

3. **Adjust the Heading:**
    Use the heading slider to adjust the drone's heading. The current heading is displayed below the slider.

4. **Set New Waypoints:**
    Enter new latitude and longitude values in the provided text boxes and click "Confirm" to set a new waypoint.

5. **Mission Control:**
    - **Pause Mission:** Click the "Mission Pause" button to pause the current mission.
    - **Switch to Guided Mode:** Click the "Guided" button to switch the drone to guided mode.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) file for details.

## 🛠️ Troubleshooting

If you encounter issues, ensure that:
- The Java SDK and UGCS SDK are correctly installed.
- The environment variables are correctly set.
- You have the necessary permissions to run Java commands from your terminal.

Feel free to open an issue if you need further assistance.

---

<p align="center">
    <b>Made with ❤️ by Joe</b>
</p>
