import subprocess
import json

result = subprocess.run(
    ["ansible-playbook", "minh_dep_zai.yml", "--connection=local", "-v", "--tags=all"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)


if result.returncode == 0:
    print("Playbook ran successfully!")
    try:
        ansible_output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing Ansible output as JSON: {e}")
else:
    print("Playbook execution failed!")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    ansible_output = None

if ansible_output:
    for play in ansible_output['plays']:
        for task in play['tasks']:
            for host, host_data in task['hosts'].items():
                host_name = host
                task_name = task['task']['name']
                task_result = host_data.get('task_result', {})
                
                print(f"Host: {host_name}")
                print(f"Task: {task_name}")
                
                # Process task-specific data based on your playbook structure
                if task_name == "Get Web App Info":
                    web_app_info = task_result.get('web_app_info', {})
                    web_app_output = web_app_info.get('stdout', '')
                    print(f"Web App Info:\n{web_app_output}")
                
                if task_name == "Configure PostgreSQL":
                    postgres_output = task_result.get('postgres_output', {})
                    print(f"PostgreSQL Configuration:\n{postgres_output}")
else:
    print("No Ansible output to process.")
