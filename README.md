# Base system frab10

The base system with user interface for FRA262 (Robotics Studio III) R-theta robot

$~$

## Installation
1. Install all fonts that are in `/font` in your computer
2. Install the libraries by using following command
```bash
cd code && pip install -r requirements.txt
```
$~$

## Configuration 
You might need to change **`device_port`** same as display in Device Manager the **`protocol.py`** file.


$~$

## How to use
### 1. Launching the Program
- Open the `code` folder in Visual Studio Code or any IDE
- Run the `main.py` file:
  ```bash
  cd code
  python main.py
  ```
- The GUI will appear for controlling the R-Theta Robot

### 2. Operation Modes
There are two main control modes available in the system:

1. **Jog Mode**  
   - Activate this mode by clicking the **Jog Mode** radio button in the GUI.
   - The user manually controls the robot’s **R** and **Theta** axes using a **joystick**.
   - The current values of **R** and **Theta** are displayed live in the GUI.
   - The user moves the robot to different positions and **records 10 positions manually**.
   - After recording, the robot’s positions are **sent to the Base System** just for acknowledgment (no movement yet).
   - Then, press the **Run button on the joystick** to command the robot to **move through the 10 recorded positions sequentially**.



2. **Point Mode**  
   - Activate this mode by clicking the **Point Mode** radio button in the GUI.
   - Enter the target values for **R** (0–500 mm) and **Theta** (–180° to 180°) into the input fields.
   - Press **Run** to send the values to the robot.
   - The robot will **automatically move to the specified position**.


---

## Protocol: Address & Function

### 1. Register Address Table

| Address     | Description                                 | Operation  |
|-------------|---------------------------------------------|------------|
| `0x00`      | Heartbeat Protocol                          | Read/Write |
| `0x01`      | Base System Status                          | Write      |
| `0x03`      | Servo (Pen) Limit Switch Status (UP/DOWN)   | Read       |
| `0x04`      | Servo Command – UP                          | Write      |
| `0x05`      | Servo Command – DOWN                        | Write      |
| `0x10`      | R-Theta Moving Status                       | Read       |
| `0x11`      | R-Axis Actual Position (signed, mm*10)      | Read       |
| `0x12`      | Theta-Axis Actual Position (signed, deg*10) | Read       |
| `0x13`      | R-Axis Actual Speed (mm/s*10)               | Read       |
| `0x14`      | Theta-Axis Actual Speed (deg/s*10)          | Read       |
| `0x15`      | R-Axis Acceleration (mm/s²*10)              | Read       |
| `0x16`      | Theta-Axis Acceleration (deg/s²*10)         | Read       |
| `0x20–0x39` | Target Positions 1–10                       | Read       |
| `0x40`      | Goal R Position                             | Write      |
| `0x41`      | Goal Theta Position                         | Write      |

### 2. Bit Positions (Base System Status - 0x01)

| Bit | Binary Value | Decimal | Meaning         |
|-----|--------------|---------|-----------------|
| 0   | 0001         | 1       | Home            |
| 1   | 0010         | 2       | Run Jog Mode    |
| 2   | 0100         | 4       | Run Point Mode  |
| 3   | 1000         | 8       | Go To Target    |
| 4   | 10000        | 16      | Stop            |
> Example: If if you press `Home` button in Base system, it will change data in 2nd bit from 0 to 1 in address Base System Status(0x01).

### 3. Data Format Notes
- All values (position, speed, acceleration) must be multiplied by **10** before sending
  - Example: R = 123.4 mm → Send 1234 to register
- Heartbeat check: Read 0x00 expecting `Ya` (22881), respond with `Hi` (18537)
- Gripper up/down is written to 0x02; status read from 0x03
- Current status read from 0x10 to determine motion state

---

### Data Format

1. **Base System Status (Register 0x01)**
This register is used to command the robot’s high-level actions such as homing, running in jog or point modes, executing movement to target positions, or stopping.

| Bit | Binary                        | Decimal | Meaning         | Description                                                                 |
|-----|-------------------------------|---------|-----------------|-----------------------------------------------------------------------------|
| 0   | 0000 0000 0000 0001           | 1       | Home            | Send the robot to its initial reference position                           |
| 1   | 0000 0000 0000 0010           | 2       | Run Jog Mode    | Enable Jog Mode for manual/incremental control                             |
| 2   | 0000 0000 0000 0100           | 4       | Run Point Mode  | Enable Point Mode for input-based movement                                 |
| 3   | 0000 0000 0000 1000           | 8       | Go To Target    | Command the robot to go to the specified target (goal point)               |
                                            |

> **Example:** Pressing the `Home` button sets bit 0 to 1, which sends a decimal value `1` to register `0x01`.

---

2. **Servo (Pen) Movement Command (Registers 0x04 and 0x05)**
These registers control the servo (pen mechanism) to move up or down. Sending a value of 1 to either register issues the respective command.

| Register | Command | Value | Meaning         | Description                            |
|----------|---------|--------|-----------------|----------------------------------------|
| 0x04     | Up      | 1      | Move Servo Up   | Activates servo upward motion          |
| 0x05     | Down    | 1      | Move Servo Down | Activates servo downward motion        |

> **Rule:** Do **not** set both UP and DOWN to 1 at the same time — this will be ignored.

---

3. **Servo (Pen) Limit Switch Status (Register 0x03)**
This read-only register provides feedback about the servo position by checking the state of the UP and DOWN limit switches.

| Bit | Binary                        | Decimal | Meaning             | Description                                            |
|-----|-------------------------------|---------|----------------------|--------------------------------------------------------|
| 0   | 0000 0000 0000 0001           | 1       | Limit Switch Down   | Indicates the servo has reached its lowest position   |
| 1   | 0000 0000 0000 0010           | 2       | Limit Switch Up     | Indicates the servo has reached its highest position  |

> The base system reads this register and updates the UI accordingly — "TRIGGERED" for ON, "CLEAR" for OFF.

---

4. **R-Theta Moving Status (Register 0x10)**
This register is used to monitor the robot's internal state or what action it is currently performing.

| Bit | Binary                        | Decimal | Meaning         | Description                                            |
|-----|-------------------------------|---------|-----------------|--------------------------------------------------------|
| 0   | 0000 0000 0000 0001           | 1       | Home            | Robot is performing homing                             |
| 1   | 0000 0000 0000 0010           | 2       | Run Jog Mode    | Robot is under Jog Mode                                |
| 2   | 0000 0000 0000 0100           | 4       | Run Point Mode  | Robot is under Point Mode                              |
| 3   | 0000 0000 0000 1000           | 8       | Go To Target    | Robot is executing Go-To-Target                        |
| 4   | 0000 0000 0001 0000           | 16      | Stop            | Robot has been commanded to stop                       |

> This is a feedback register only. It reflects internal status from firmware and helps with safety checks or timing.

---

5. **Position / Speed / Acceleration Format**
The position, speed, and acceleration sent to the base system should contain only one decimal place. Before sending the values to the Base system, multiply the actual value by 10.(Base_system_Value = Actual_Value * 10)
> Example: If the value of the position you want to send is '123.4', multiply it by 10 to get '1234', and send this value to the address z-axis Actual Position (0x11). This will appear in the Base system as '123.4'.
---

6. **Target Position Registers (0x20 – 0x-39)**
These registers store **10 points** of preset **R** (radius) and **Theta** (angle) values that are recorded by the robot.

- Each target position consists of **two consecutive registers**: one for **R** (radius) and the other for **Theta** (angle).
- The values stored are in **16-bit signed format** and are **scaled by 10** (i.e., the actual values are divided by 10 to match the real-world units for **R** and **Theta**).
- These registers are read from the robot using the `read_target_positions()` function, where each pair of registers corresponds to a specific point in the robot’s planned path.
#### **Register Address Mapping**:
- **`0x20 - 0x39`**: Stores the values for **Target Positions 1 to 10**.
  
  Each point is stored as **two consecutive 16-bit signed integers**:
  - **`0x20`**: `R1` (radius of point 1)
  - **`0x21`**: `Theta1` (angle of point 1)
  - **`0x22`**: `R2` (radius of point 2)
  - **`0x23`**: `Theta2` (angle of point 2)
  - ...
  - **`0x38`**: `R10` (radius of point 10)
  - **`0x39`**: `Theta10` (angle of point 10)

#### **Data Format**:
- The values in the registers are **signed 16-bit integers**, which are then converted to the actual **distance** (in mm) and **angle** (in degrees) by dividing by **10**.

  **Example**:
  - If **`register[0x20]`** stores the value **1505**, the actual **R** value will be **1505 / 10 = 150.5 mm**.
  - If **`register[0x21]`** stores the value **302**, the actual **Theta** value will be **302 / 10 = 30.2°**.

$~$
