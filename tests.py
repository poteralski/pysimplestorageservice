from pysimplestorageservice import AmazonAWSManager
import unittest


class MyTestCase(unittest.TestCase):

    def test_something(self):
        AWS_ACCESS_KEY_ID = ''
        AWS_SECRET_ACCESS_KEY = ''
        amazon = AmazonAWSManager(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        files = amazon.get_file_list(
            bucket='teatrtotu',
            prefix='media/images/events/',
        )
        print files
        dirs = amazon.get_dir_list(
            bucket='teatrtotu',
            prefix='media/',
        )
        print dirs

if __name__ == '__main__':
    unittest.main()
