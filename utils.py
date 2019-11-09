import random


def cleanArrayAndConvertToFloat(arr) :
    arr.pop(0)
    arr[-1] = arr[-1].strip()
    arr = list(map(float, arr))
    return arr

def getRandomJoke() :
    jokes = ["What did the green grape say to the purple grape? |  BREATHE STUPID!",
		"What happens to a frog's car when it breaks down? |  It gets toad away.",
		"Why isn't the turkey hungry at Thanks giving?  |   Because it's stuffed.",
		"Why do witches wear name tags? |  So they know which witch is which.",
		"My friend thinks he is so smart, told me today that onion is the only food that makes you cry  |   So I threw a coconut at his face.",
		"What stays in one corner but travels around the world?  |  A stamp.",
		"What do you call a pig that does karate?  |  Pork chop.",
		"Why does Humpty Dumpty love autumn?  |  Because he had a great fall last year.",
		"Did you hear about the kidnapping at school today?  |  It's alright, he's awake now.",
		"Have you heard about the new restaurant Karma?  |  There's no menu, you get what you deserve."]

    return jokes[random.randint(0,9)]