import requests


def file_validator(file_id):
    # file_id = file_id
    a = requests.get('http://192.168.0.100:7001/uploader/{}/'.format(file_id))
    b = a.json()
    if b['exists'] == 'true':
        print('This file exists in uploader machine')
        return True
    else:
        print('This file does not exists in uploader machine')
        return False


def delete_file(file_id):

    a = requests.delete('http://192.168.0.100:7001/uploader/{}/'.format(file_id))

    return True
    


if __name__ == '__main__':
    file_validator()


