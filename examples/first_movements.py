import pydobot
import keyboard
import time
import numpy as np

# 1) Verbindung zum Dobot herstellen (COM-Port ggf. anpassen)
dobot = pydobot.Dobot()

# 2) Funktion zur manuellen Positionserfassung
def capture_position(name: str) -> np.ndarray:
    input(f"Move the Dobot manually to the {name} and press Enter…")
    x, y, z, r = dobot.get_pose().position
    print(f"{name} captured: X={x:.2f}, Y={y:.2f}, Z={z:.2f}, R={r:.2f}")
    return np.array([x, y, z, r])

print("=== Move Robot to new Home Position manually")
home = capture_position("Home")
dobot._set_home_coordinate(home[0],home[1],home[2], home[3])
dobot._set_ptp_jump_params(50,35)
dobot.speed(30,30)

print("=== Press Ctrl+Enter for Homing ===")
keyboard.wait('ctrl+enter')
dobot.wait_for_cmd(dobot.home())

# 3) Manuelle Erfassung der beiden Eckpunkte
print("=== Manual capture of grid corners ===")
start = capture_position("start point (top-left)")
end   = capture_position("end point   (bottom-right)")

# 4) Raster-Parameter und Berechnung der Punkte
grid_size = 5
x_vals = np.linspace(start[0], end[0], grid_size)
y_vals = np.linspace(start[1], end[1], grid_size)
z_height = start[2]  # Höhe konstant halten

# 5) Raster abfahren
print("=== Starting grid scan ===")
for y in y_vals:
    for x in x_vals:
        print(f"Press Ctrl+Enter to move to → X={x:.2f}, Y={y:.2f}, Z={z_height:.2f}")
        keyboard.wait('ctrl+enter')
        dobot.wait_for_cmd(dobot.move_to(x, y, z_height, mode=0))
        time.sleep(0.2)  # kleine Pause


keyboard.wait('ctrl+enter')
print("✅ Grid scan complete.")
end = capture_position("end")
dobot.speed(30,30)
dobot.wait_for_cmd(dobot.move_to(end[0],end[1],end[2]+50,end[3]))
dobot.close()
