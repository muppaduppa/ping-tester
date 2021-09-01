"""
AUTHOR: Muppaduppa
DATE: 1 Sep 2021
Small script that you can use to verify that devices in an subnet 
is working before and after a "job". Will print result of diff between
before and after.

version 1.0 First release
"""


import ipaddress
import subprocess
import difflib
import os



def create_ip_list(ip_subnet):
    """Creates an ip address list"""
    
    ips= ipaddress.ip_network(ip_subnet)
    ip_list=[str(ip) for ip in ips]
    return ip_list

def ping_device_before(ip_list,ip_subnet_filename,ip_subnet):
    """Ping devices in subnet and prints/write UP result to file"""

    ip_list_up=[]
    with open('ping_tester-{}-before.txt'.format(ip_subnet_filename), 'w') as file:
        print()
        print('Before Check. Pinging all ip in subnet, listing all device that are reachable')
        print('test subnet = {}'.format(ip_subnet))
        print('-' * 80)
        for ip in ip_list:
            p = subprocess.Popen(['ping', '-q', '-c', '2', '-i', '0.3','-W', '4',ip],stdout=subprocess.DEVNULL)
            p.wait()
            if p.returncode == 0:
                file.write('{}\n'.format(ip))
                print('{}'.format(ip))
                ip_list_up.append(ip)
                
        return ip_list_up

def ping_device_after(ip_list_up,ip_subnet_filename,ip_subnet):
    """Ping UP devices from before and prints/write UP result to file"""

    with open('ping_tester-{}-after.txt'.format(ip_subnet_filename), 'w') as file:
        print('\n')
        print('After Check. Pinging devices from before, listing all device that are reachable')
        print('test subnet = {}'.format(ip_subnet))
        print('-' * 80)
        for ip in ip_list_up:
            #p = subprocess.Popen(['ping', '-q', '-c', '2', '-i', '0.1',ip],stdout=subprocess.DEVNULL)
            p = subprocess.Popen(['ping', '-q', '-c', '3', '-i', '0.5','-W', '5',ip],stdout=subprocess.DEVNULL)
            p.wait()
            if p.returncode == 0:
                file.write('{}\n'.format(ip))
                print('{}'.format(ip))
               
          
        

def compare_files(ip_subnet_filename):
    """Compares result from before/after and prints diff"""
    #open before file for reading
    with open('ping_tester-{}-before.txt'.format(ip_subnet_filename)) as file_1:
        file_1_text = file_1.readlines()
    #open after file for reading
    with open('ping_tester-{}-after.txt'.format(ip_subnet_filename)) as file_2:
        file_2_text = file_2.readlines()
    
    
    size1 = os.path.getsize('ping_tester-{}-before.txt'.format(ip_subnet_filename))
    size2 = os.path.getsize('ping_tester-{}-after.txt'.format(ip_subnet_filename))
    if size1 == size2:
        print('\n')
        print('All devices are up and running')
        print('-' * 80)
    else:
        for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile='ping_tester-{}-before.txt'.format(ip_subnet_filename), 
            tofile='ping_tester-{}-after.txt'.format(ip_subnet_filename), lineterm='',n=0):
            for prefix in ('---', '+++', '@@'):
                if line.startswith(prefix):
                    break
            else:
                print('\n')
                print('These devices was reachable before but not anymore. Please investigate')
                print('-' * 80)
                print (line)

        


def show_menu():
    print ('\nMain menu')
    print ('-----------------')
    print ('1) Ping-tester before')
    print ('2) Ping-tester after')
    print ('3) Compare before and after')
    print ('Q) Exit\n')

def menu():
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            ip_list_up = ping_device_before(ip_list,ip_subnet_filename,ip_subnet)
        elif choice == '2':
            ping_device_after(ip_list_up,ip_subnet_filename,ip_subnet)
        elif choice == '3':
            compare_files(ip_subnet_filename)
            
        elif choice == 'q':
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')


if __name__ == '__main__':
    print('\n')
    ip_subnet = str(input('enter subnet with mask i.e 192.168.1.0/24 : '))
    print('\nTest subnet:',ip_subnet)
    ip_list = create_ip_list(ip_subnet)
    ip_subnet_filename = ip_subnet.replace('/','-')
    menu()

