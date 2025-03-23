from protocol import Protocol_RT
import time

# ✅ สร้างอ็อบเจ็กต์ Protocol_RT
protocol = Protocol_RT()

# ✅ ทดสอบการเชื่อมต่อ Modbus
if protocol.usb_connect:
    print("✅ Modbus Connection Successful!")
else:
    print("❌ Modbus Connection Failed!")

# ✅ ทดสอบการอ่านค่าต่าง ๆ
print("🔍 Reading initial values...")
protocol.routine()

print(f"📍 r Position: {protocol.r_position} mm")
print(f"📍 theta Position: {protocol.theta_position} degree")
print(f"🚀 Speed: r = {protocol.v_r} mm/s, theta = {protocol.v_theta} degree/s")

# ✅ ทดสอบการเขียนคำสั่ง Home
print("🏠 Sending Home Command...")
protocol.write_base_system_status("Home")

# ✅ รอ 2 วินาที และตรวจสอบค่าที่เปลี่ยนแปลง
time.sleep(2)
protocol.routine()
print(f"📍 r Position (Updated): {protocol.r_position} mm")
print(f"📍 theta Position (Updated): {protocol.theta_position} degree")
