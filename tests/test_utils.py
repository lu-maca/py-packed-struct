import logging

logging.basicConfig(level=logging.INFO,)

required_tests = []

def test(f):
    required_tests.append(f)
    return f

def non_blocking_assert(condition: bool, message: str):
    try:
        assert condition, message
    except AssertionError as e:
        logging.error(e)
 
def run():
    for test in required_tests:
        try:
            logging.info(f"Running test: {test.__name__}")
            test()
        except AssertionError as e:
            logging.error(e)
        except Exception as e:
            raise e
        