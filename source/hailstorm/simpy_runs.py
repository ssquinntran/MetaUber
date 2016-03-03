import simpy

"""
https://simpy.readthedocs.org/en/latest/simpy_intro/process_interaction.html
https://simpy.readthedocs.org/en/latest/
https://simpy.readthedocs.org/en/latest/simpy_intro/basic_concepts.html
https://simpy.readthedocs.org/en/latest/examples/index.html
https://simpy.readthedocs.org/en/latest/contents.html
https://simpy.readthedocs.org/en/latest/topical_guides/index.html
https://simpy.readthedocs.org/en/latest/api_reference/index.html
http://ubuntuforums.org/showthread.php?t=1659574
"""
def car(env):
	while True:
		print('Start parking at %d' % env.now)
		parking_duration = 5
		yield env.timeout(parking_duration)
		print('Start driving at %d' % env.now)
		trip_duration = 2
		yield env.timeout(trip_duration)
env = simpy.Environment()
env.process(car(env))
env.run(until=15)