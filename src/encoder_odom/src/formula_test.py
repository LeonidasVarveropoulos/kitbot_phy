import math

# Set initial values
th = 0
x = 10
y = 10

# Set constants
hz_rate = 1.0
body_width = 1.0
encoder_counts_per_rev = 256.0 
wheel_dia = 0.1524
wheel_circum = 1.0

# Calculate distance of each wheel 

pre_l_tick = 0.0
pre_r_tick = 0.0

left_tick = -256
right_tick = -256

distance_left = ((left_tick - pre_l_tick) / encoder_counts_per_rev) * wheel_circum
distance_right = ((right_tick - pre_r_tick) /encoder_counts_per_rev) * wheel_circum

pre_th = th

# If the robot is moving perfectly forward (Inorder to aviod crashing the program by dividing by 0)
if distance_right == distance_left:
    th = pre_th
    x += distance_left * math.cos(pre_th)
    y += distance_left * math.sin(pre_th)
else:
    th = th + (distance_left-distance_right) / body_width
    x = x - ((body_width*(distance_right + distance_left))/(2*(distance_right - distance_left))) * (math.sin(th) - math.sin(pre_th))
    y = y + ((body_width*(distance_right + distance_left))/(2*(distance_right - distance_left))) * (math.cos(th) - math.cos(pre_th))

# Calculate robot velocities in referance of the robot base not the map
vth = (( distance_left- distance_right) / body_width) * hz_rate
vx = ((distance_right + distance_left) /2) * hz_rate
vy = 0

print(x)
print(y)
print(th)

print(" ")

print(vx)
print(vy)
print(vth)