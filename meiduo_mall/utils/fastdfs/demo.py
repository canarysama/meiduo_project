from fdfs_client.client import Fdfs_client


if __name__ == '__main__':

    client = Fdfs_client('client.conf')

    data = client.upload_by_filename('/home/python/Desktop/picture/u=3093055328,1855974557&fm=214&gp=0.jpg')
    print(data)





