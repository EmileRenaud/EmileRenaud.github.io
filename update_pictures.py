import os
import json
import re

def numerical_sort(value):
    """ Extract numbers from the folder name and return as key for sorting. """
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else float('inf')  # Return large value if no number is found

def create_pictures_and_project_json():
    current_directory = os.getcwd()
    
    # Path to the /projects folder
    projects_folder = os.path.join(current_directory, 'projects')
    
    projects_list = []
    project_folders = []

    # First, gather all project folders
    for folder_name in os.listdir(projects_folder):
        folder_path = os.path.join(projects_folder, folder_name)
        if os.path.isdir(folder_path):
            project_folders.append(folder_name)

    # Sort folders numerically based on the number in the folder name
    project_folders = sorted(project_folders, key=numerical_sort, reverse=True)

    # Loop through each project folder
    for index, folder_name in enumerate(project_folders):
        folder_path = os.path.join(projects_folder, folder_name)
        
        images = []
        project_info = {}

        # Look for all image files and add them to the 'pictures.json'
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                images.append(file_name)

        pictures_data = {
            "images": images
        }
        
        # Write the 'pictures.json' in the project folder
        pictures_json_path = os.path.join(folder_path, 'pictures.json')
        with open(pictures_json_path, 'w') as json_file:
            json.dump(pictures_data, json_file, indent=2)
        
        print(f"Created {pictures_json_path}")

        # Now process the 'info.json' if it exists
        info_json_path = os.path.join(folder_path, 'info.json')
        if os.path.exists(info_json_path):
            with open(info_json_path, 'r') as info_file:
                project_info = json.load(info_file)[0]  # Assume the structure you provided

            # Ensure paths are properly formatted (using forward slashes)
            project_info['image'] = f'projects/{folder_name}/{project_info["image"]}'.replace("\\", "/")
            project_info['link'] = f'projects/{folder_name}/{project_info["link"]}'.replace("\\", "/")

            # Add prev and next links
            if index == 0:  # First project
                project_info['prev'] = "/index.html"
            else:
                project_info['prev'] = f'projects/{project_folders[index - 1]}/page.html'

            if index == len(project_folders) - 1:  # Last project
                project_info['next'] = "/index.html"
            else:
                project_info['next'] = f'projects/{project_folders[index + 1]}/page.html'

            # Append the project information to the projects list
            projects_list.append(project_info)
    
    # Create or update the 'projects.json' in the root directory
    projects_json_path = os.path.join(current_directory, 'projects.json')
    with open(projects_json_path, 'w') as projects_file:
        json.dump({"projects": projects_list}, projects_file, indent=2)

    print(f"Created {projects_json_path}")

def update_info_json_with_prev_next():
    current_directory = os.getcwd()
    
    # Load the projects.json file
    projects_json_path = os.path.join(current_directory, 'projects.json')
    with open(projects_json_path, 'r') as projects_file:
        projects_data = json.load(projects_file)

    projects_list = projects_data['projects']

    # Update each project's info.json with prev and next data
    for index, project in enumerate(projects_list):
        # Determine folder name from the link (assuming 'link' format: 'projects/{folder_name}/page.html')
        folder_name = project['link'].split('/')[1]
        project_folder_path = os.path.join('projects', folder_name)

        info_json_path = os.path.join(project_folder_path, 'info.json')
        if os.path.exists(info_json_path):
            with open(info_json_path, 'r') as info_file:
                info_data = json.load(info_file)

            # Update 'prev' and 'next' in the info.json file
            if index == 0:
                info_data[0]['prev'] = "/index.html"
            else:
                info_data[0]['prev'] = "/"+projects_list[index - 1]['link']

            if index == len(projects_list) - 1:
                info_data[0]['next'] = "/index.html"
            else:
                info_data[0]['next'] = "/"+projects_list[index + 1]['link']

            # Write the updated info.json back to the project folder
            with open(info_json_path, 'w') as info_file:
                json.dump(info_data, info_file, indent=2)
            
            print(f"Updated {info_json_path} with prev and next links")

# Run the script
create_pictures_and_project_json()
update_info_json_with_prev_next()
