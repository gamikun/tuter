from tuter.project import Project, Item
from io import BytesIO
import subprocess

project = Project(
	time_range=(2018, 2020)
)
project.add_item(
	values={2012: 34, 2013: 34, 2014: 35, 2015: 35, 2016: 30, 2017: 29, 2018: 28},
	label='Mexico',
	color=(0, 255, 0, 255),
)
project.add_item(
	values={2012: 73, 2013: 73, 2014: 74, 2015: 76, 2016: 74, 2017: 75, 2018: 71},
	label='USA',
	color=(0, 0, 255, 255),
)
project.add_item(
	values={2012: 84, 2013: 81, 2014: 81, 2015: 83, 2016: 82, 2017: 82, 2018: 81},
	label='Canada',
	color=(255, 0, 0, 255),
)
project.add_item(
	values={2012: 39, 2013: 40, 2014: 36, 2015: 37, 2016: 40, 2017: 41, 2018: 39},
	label='China',
	color=(0, 0, 0, 255),
)
project.add_item(
	values={2012: 79, 2013: 78, 2014: 79, 2015: 81, 2016: 81, 2017: 81, 2018: 80},
	label='Alemania',
	color=(255, 128, 0, 255),
)
project.add_item(
	values={2012: 19, 2013: 20, 2014: 19, 2015: 17, 2016: 17, 2017: 18, 2018: 18},
	label='Venezuela',
	color=(0, 0, 0, 255),
)
project.add_item(
	values={2012: 35, 2013: 34, 2014: 34, 2015: 32, 2016: 36, 2017: 39, 2018: 40},
	label='Argentina',
	color=(0, 128, 255, 255),
)
project.add_item(
	values={2012: 37, 2013: 35, 2014: 38, 2015: 38, 2016: 35, 2017: 37, 2018: 36},
	label='Tailandia',
	color=(128, 0, 0, 255),
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


for step in range(2012, 2019):
	for index in range(0, framerate + 1):
		image = project.generate_image(step=(step, step + 1), time=(1.0 / framerate) * index)
		image.save(ffmpeg.stdin, 'PNG')
	# image.save('image-%d.png' % index)

"""
image = project.generate_image(step=(2018, 2019), time=0)
image.save('image-0.00.png')

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

ffmpeg.communicate()