import pytest
from wordhunt import wordhunt

def test():
	res = wordhunt("./Test/","Hey")
	assert res != {},"test failed, empty result"
	for reskey in res:
		assert res[reskey][0]['Text'] == '>>Hey<<', "test failed, wrong result"