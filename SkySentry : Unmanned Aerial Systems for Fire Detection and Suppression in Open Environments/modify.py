import os

def process_files(folder_path):
    # Get a list of all files in the specified folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Process only text files
        if file_name.lower().endswith('.txt'):
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()

            # Change the first character from '0' to '1'
            if content and content[0] == '0':
                content = '1' + content[1:]

                # Write the modified content back to the file
                with open(file_path, 'w') as file:
                    file.write(content)

            print(f"Processed: {file_name}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")

    if os.path.exists(folder_path):
        process_files(folder_path)
        print("Processing complete.")
    else:
        print("Invalid folder path.")
