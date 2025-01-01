from tuter.project import Project, Item
from io import BytesIO
from PIL import Image
import subprocess


project = Project(
	time_range=(2018, 2020),
	size=(1920, 1080),	
)
project.add_item(
	values=[34, 34, 35, 35, 30, 29, 28, 900],
	label='Mexico',
	color=(0, 255, 0, 255),
	image=Image.open('mx.png').convert('RGBA'),
)
project.add_item(
	values=[73, 73, 74, 76, 74, 75, 71, 5],
	label='USA',
	color=(0, 0, 255, 255),
	image=Image.open('us.png').convert('RGBA'),
)
project.add_item(
	values=[84, 81, 81, 83, 82, 82, 81, 2500],
	label='Canada',
	color=(255, 0, 0, 255),
	image=Image.open('ca.png').convert('RGBA'),
)
project.add_item(
	values=[39, 40, 36, 37, 40, 41, 39, 4000],
	label='China',
	color=(0, 0, 0, 255),
	image=Image.open('cn.png').convert('RGBA'),
)
project.add_item(
	values=[79, 78, 79, 81, 81, 81, 80, 20],
	label='Alemania',
	color=(255, 128, 0, 255),
	image=Image.open('de.png').convert('RGBA'),
)
project.add_item(
	values=[19, 20, 19, 17, 17, 18, 18, 1500],
	label='Venezuela',
	color=(0, 0, 0, 255),
	image=Image.open('ve.png').convert('RGBA'),
)
project.add_item(
	values=[35, 34, 34, 32, 36, 39, 40, 500],
	label='Argentina',
	color=(0, 128, 255, 255),
	image=Image.open('ar.png').convert('RGBA'),
)
project.add_item(
	values=[37, 35, 38, 38, 35, 37, 36, 750],
	label='Tailandia',
	color=(128, 0, 0, 255),
	image=Image.open('th.png').convert('RGBA'),
)

framerate = 60
ffmpeg = subprocess.Popen(
	['ffmpeg',
		'-f', 'image2pipe',
		'-framerate', str(framerate),
		'-vcodec', 'png',
		'-i', '-',
		'-f', 'mp4',
		'-b:v', '5000k',
		'-y',
		'algo.mp4'
	],
	stdin=subprocess.PIPE
)

for step in range(2012, 2020):
	for index in range(0, framerate + 1):
		image = project.generate_image(step=(step, step + 1), time=(1.0 / framerate) * index)
		image.save(ffmpeg.stdin, 'PNG')
	# image.save('image-%d.png' % index)

ffmpeg.communicate()

image = project.generate_image(step=(2012, 2013), time=0)
image.save('image-0.00.png')

"""
image = project.generate_image(step=(2018, 2019), time=0.25)
image.save('image-0.25.png')

image = project.generate_image(step=(2018, 2019), time=0.50)
image.save('image-0.50.png')

image = project.generate_image(step=(2018, 2019), time=0.75)
image.save('image-0.75.png')

image = project.generate_image(step=(2018, 2019), time=1.00)
image.save('image-1.00.png')
"""

"""
for index in range(0, framerate):
	image = project.generate_image(step=(2019, 2020), time=(1.0 / framerate) * index)
	image.save(ffmpeg.stdin, 'PNG')
"""

