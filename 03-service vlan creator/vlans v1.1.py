import paramiko
import time

##############################
username = 'eventum'
password = 'P@ssw0rd123'
# in_file = 'DC02_VLANS.csv'
in_file = 'TB_VLANS.csv'
ip_address = '10.52.49.24'

connect=False
##############################
out_file = in_file.split('.')[0] + '_configuration.txt'
conf = open (out_file, 'w')

f = open(in_file, 'r')
input = f.readlines()

# Keeps vlan to description mapping
vlans_desc = {}

for line in input:
	vlans=[]
	# Get the first vlan in the range
	v_st = line.split(',')[0]
	vlans.append(v_st)
	# If there is a range of vlans
	if line.split(',')[1]:
		v_end = line.split(',')[1]
		# create a list with all the vlan numbers within the range and put them in the list "vlans"
		while ((int(v_end) - int(v_st)) > 0):
			x = int(v_st) + 1
			vlans.append(str (x))
			v_st = int(v_st) + 1

		## Execute the command to the switch
		n=1
		for v in vlans:
			# If the vlan was mentioned in previous range, generate warning message and skip configuring it
			if str(v) in vlans_desc.keys():
				print ('vlan ' + str(v) + ' with description :"' + str(line.split(',')[2].strip()) + '_sub_' + str(n) + '" is configured in previous range with description : "' + vlans_desc[str(v)] + '"')
				continue
			# Write the command to be ecexuted on the switch for each vlan
			conf.write ('vlan ' + str(v) + '\n' + ' description ' + str(line.split(',')[2].strip()) + '_sub_' + str(n) + '\n')
			vlans_desc[str(v)]= str(line.split(',')[2].strip()) + '_sub_' + str(n)
			n = n+1
	else:
		if str(v_st) in vlans_desc.keys():
			print ('vlan ' + str(v_st) + ' with description : "' + str(line.split(',')[2].strip()) + '" is configured in previous range with description : "' + vlans_desc[str(v_st)] + '"')
			continue
		# Write the command to be ecexuted on the switch for each vlan
		conf.write ('vlan ' + str(v_st) + '\n' + ' description ' + str(line.split(',')[2].strip()) + '\n')
		vlans_desc[str(v_st)]= str(line.split(',')[2].strip())
f.close()
conf.close()

if connect is True:
# Connect to the device and execute the commands
	commands = open (out_file, 'r')
	command_line = commands.readlines()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip_address, username=username, password=password, look_for_keys=False, allow_agent=False)
	remote_conn = client.invoke_shell()
	remote_conn.send('sys \n')
	time.sleep(0.5)
	for comm in command_line:
		remote_conn.send(comm)
		time.sleep(0.1)
		output = remote_conn.recv(65535)
		print output
	remote_conn.send('commit \n')
	remote_conn.close()
	commands.close()
