from vehicle import Vehicle

PX4 = Vehicle("COM4")
"""
PX4.arm()

arr = [x*20 + 1100 for x in range(10)]
for pwm in arr:
    PX4.set_rc_channel_pwm(4, pwm)
    PX4.master.wait_heartbeat()
PX4.set_rc_channel_pwm(4, 1000)

#PX4.avanzar(-0.1,5)
#PX4.girar(0.1,5)
#PX4.avanzar_lateral(0.1,5)

PX4.disarm()
"""
# PX4.start_data_rx()
# Aquí puedes recibir datos
# PX4.stop_data_rx()

