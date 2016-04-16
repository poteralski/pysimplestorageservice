from pysimplestorageservice import AmazonAWSManager
import unittest

from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class MyTestCase(unittest.TestCase):

    def test_something(self):

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
        result = amazon.get(
            filename='',
            prefix='',
            bucket=''
        )

if __name__ == '__main__':
    unittest.main()
