import os
from os.path import join,exists

# ==============================================================================
# Tar
# ==============================================================================	
class Tar():
	def __init__(self):
		pass

# |----------------------------------------------------------------------------|
# tar_complete_slide_folder
# |----------------------------------------------------------------------------|
	def tar_complete_slide_folder(self,slide_path,slide_name):
		print('slide_path ',slide_path)
		os.chdir(slide_path)
		tarcmd = "tar -cf {}.tar {}".format(slide_name,slide_name)
		print(tarcmd)
		status = os.system(tarcmd)

		return status
# |----------------------End of tar_complete_slide_folder-------------------------------|

# |----------------------------------------------------------------------------|
# tar_slide_folder
# |----------------------------------------------------------------------------|
	def tar_slide_folder(self,src_path,slide_name):
		slide_path = join(src_path,slide_name)
		filelist =os.listdir(slide_path)
		
		print(len(filelist))
		os.chdir(slide_path)
		filelist.remove(slide_name+'.jpeg')
		print(filelist)
		status = self.tar_command(slide_name,filelist,slide_path)

		return status

# |----------------------End of tar_slide_folder-------------------------------|

# |----------------------------------------------------------------------------|
# tar_grid_folder
# |----------------------------------------------------------------------------|
	def tar_grid_folder(self,src_path,slide_name):
		slide_path = join(src_path,slide_name)

		filelist =os.listdir(slide_path)
		#print(filelist)
		gridlist =[]
		otherlist =[]
		stacklist = []
		for grid in filelist:
			if 'grid' in grid:
				print(grid)
				gridlist.append(grid)
				grid_path = join(slide_path,grid)
				grid_list = os.listdir(grid_path)
				if exists(join(grid_path,"blobs")) is True:
					grid_list.remove('blobs')
				if exists(join(grid_path,"stack_images")) is True:
					grid_list.remove('stack_images')
					stacklist.append('stack_images')
					status = self.tar_command('stack_images',stacklist,grid_path)

				print(grid_list)
				status = self.tar_command('grid_intermediate',grid_list,grid_path)
				print('*****************************************')
			else:
				#print(grid)
				otherlist.append(grid)
				

		print('grid -->',gridlist)

		os.chdir(slide_path)
		otherlist.remove(slide_name+'.jpeg')
		print('other-->',otherlist)
		status = self.tar_command('other',otherlist,slide_path)

		return status
# |----------------------End of tar_grid_folder-------------------------------|

# |----------------------------------------------------------------------------|
# tar_command
# |----------------------------------------------------------------------------|
	def tar_command(self,name,data_list,path):
		os.chdir(path)
		status =123
		str1 = " "
		tarcmd = 'tar -cf {}.tar {}'.format(name,str1.join(data_list))
		print('tarcmd',tarcmd)
		status = os.system(tarcmd)
		os.system('rm -rf {}'.format(str1.join(data_list)))

		return status

# |----------------------End of tar_command-------------------------------|


if __name__ == '__main__':

	obj = Tar()
	obj.tar_grid_folder('/home/adminspin/wsi_app/acquired_data/','S1_34752')
