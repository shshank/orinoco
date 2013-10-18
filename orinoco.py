import boto.ec2 as b
from datetime import datetime 

class AWS_iface():
	def __init__(self):
		self.regions = [reg for reg in b.regions() if 'gov' not in reg.name]
		self.connections = dict([(reg.name,reg.connect()) for reg in self.regions])
	
	def get_instances_from_region(self, reg_name):
		reservations = self.connections[reg_name].get_all_instances()
		for resv in reservations:		
			if resv.instances[0].tags:
				print str(resv.instances[0].tags)
				
		reg_instances = [(resv.instances[0].id, resv.instances[0].public_dns_name, reg_name)\
		                  for resv in reservations\
		                  if not resv.instances[0].tags or 'APK_Donwloader' in resv.instances[0].tags['Name'] ]
		return reg_instances
	
	def get_all_instances(self):
		all_instances = []
		for reg in self.regions:
			all_instances += self.get_instances_from_region(reg.name)
		return all_instances
	
		
	def make_csv(self, list_of_tuples, file_path):
		with open(file_path, 'w') as fil:
			for item in list_of_tuples:
				line = ','.join(item)
				fil.write(line+'\n')
	

	def generate_csv(self, for_reg = None):
		if for_reg:
			#print get_instances_for_region(for_reg)
			self.make_csv(self.get_instances_from_region(for_reg),for_reg+str(datetime.now()))
		else:
			#print get_instances_for_region(for_reg)
			self.make_csv(self.get_all_instances(),'all_ins'+str(datetime.now()))
	
	def reboot_instances(self,instances, reg_name):
		if instances:
			return self.connections[reg_name].reboot_instances(instances)
		else:
			return 'no instances in '+reg_name
	
	def reboot_all_instances(self,reg_name = None):
		if reg_name:
			list_of_tuples = self.get_instances_from_region(reg_name)
			ins_ids = [item[0] for item in list_of_tuples]
			return self.reboot_instances(ins_ids, reg_name)
		else:
			status = {}
			for reg in self.regions:
				list_of_tuples = self.get_instances_from_region(reg.name)
				print list_of_tuples
				ins_ids = [item[0] for item in list_of_tuples]
				status[reg.name] = self.reboot_instances(ins_ids, reg.name)
				print status[reg.name]
			return status
	
	def terminate_instances(self,instances, reg_name):
		if instances:
			return self.connections[reg_name].terminate_instances(instances)
		else:
			return 'no instances in '+reg_name
	
	def terminate_all_instances(self,reg_name = None):
		if reg_name:
			list_of_tuples = self.get_instances_from_region(reg_name)
			ins_ids = [item[0] for item in list_of_tuples]
			return self.terminate_instances(ins_ids, reg_name)
		else:
			status = {}
			for reg in self.regions:
				list_of_tuples = self.get_instances_from_region(reg.name)
				print list_of_tuples
				ins_ids = [item[0] for item in list_of_tuples]
				status[reg.name] = self.terminate_instances(ins_ids, reg.name)
				print status[reg.name]
			return status

if __name__ == '__main__':
	my_iface = AWS_iface()
	my_iface.generate_csv()
	for reg in my_iface.regions:
		my_iface.generate_csv(reg.name)