import yaml

with open('../../materials/todo.yml') as input_file:
    read_data = yaml.load(input_file, Loader=yaml.FullLoader)

start = '---\n'

update_system = {'name': 'Update packages', 'apt': {'update_cache': True}}
install_important_packets = {'name': 'Install packages', 'apt': {'name': '{{item}}', 'state': 'present'},
                             'loop': (read_data['server']['install_packages'] + ['redis'])}
pip_install = {'name': 'Install pip redis', 'pip': {'name': 'redis'}}
copy_files = {'name': 'Copy files', 'copy': {'src': '{{item}}', 'dest': '.'},
              'loop': ['../ex01/consumer.py', '../ex01/producer.py', '../ex00/exploit.py']}
start_redis = {'name': 'Start redis', 'service': {'name': 'redis-server', 'state': 'started'}}
exe_check = {'name': 'Exexute check',
             'command': 'nohup python3 ' + read_data['server']['exploit_files'][1] + '-e ' + ','.join(
                 read_data['bad_guys']), 'async': 20, 'poll': 0}
exe_post = {'name': 'Exexute post', 'command': 'python3 producer.py'}

tasks = [update_system, install_important_packets, pip_install, copy_files, start_redis, exe_check, exe_post]

all = [{'name': 'Ex2', 'hosts': 'localhost', 'become': True, 'tasks': tasks}]

with open('deploy.yml', 'w') as output_file:
    output_file.write(start)
    output_file.write(yaml.dump(all, sort_keys=False))
