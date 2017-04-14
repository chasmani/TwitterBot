import random


STATUS_BITS = [
	"Woof!",
	"Woof Woof!",
	"So cute.",
	"Check out this furry fellow.",
	"Could it GET any cuter?",
	"Awwwww!",
	"Dog pic of the day!",
	"Can I take him home?",
	"This is George, George is a dog. George wants to be your friend.",
	"Fluffy madness!",
	"Sometimes I wish I could stroke every dog in the world, just once.",
	"Who's a good boy then?",
	"That's it! In my next life I want to come back as a dog.",
	"I can't take how cute this guy is!",
	"Woofy woof.",
	"Super dog!",
	"BEST - DOG - EVER.",
	"Supercute, supercute, he's supercutey!",
	"Absolutely adorable.",
	"Delightful.",
	"I'm so glad that dogs exist in the world!",
	"Okay I'm actually in lvoe with this furry fellow",
]

HASHTAGS = [
	"#dogs",
	"#DogsOfTwitter",
	"#CuteDogs",
	"#Pets",
]


def build_status():
	'''
	Build a tweet from some lists of status bits
	and hashtags
	'''
	status = ""
	# Build a list out of random status bits and a random hashtag
	status_list = random.sample(STATUS_BITS, 3) + [random.choice(HASHTAGS)]
	# Build up the tweet string, keeping it below 140 characters
	for status_bit in status_list:
		if (len(status) + len(status_bit)) < 100:
			status += status_bit + " "
	# Strip the empty space from the end
	return status.strip()
