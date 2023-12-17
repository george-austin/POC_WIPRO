import os

class LabelAmounts:
    class_labels = {
        0: "Bildartefakte",
        1: "Manuell überprüfter Container",
        2: "Schimmel",
        3: "Schmutz",
        4: "Schäden",
        5: "Schädlinge",
        6: "Sonstiges",
        7: "Starke Überbeleuchtung oder Unterbeleuchtung",
        8: "Unerwartetes Layout",
        9: "Wasser"
    }

    def get_amounts_for_each_class(self):
        # Initialize counters
        total_annotations = 0
        class_annotations = {label: 0 for label in self.class_labels.values()}

        # Folder path containing the text files
        folder_path = '../datasets/train/labels'

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)

                # Read annotations from the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate over each line in the file
                    for line in lines:
                        annotation = line.split()
                        if annotation:
                            # Increment total annotations count
                            total_annotations += 1

                            # Get the class label and update class-specific count
                            class_label = self.class_labels.get(int(annotation[0]), "Unknown")
                            class_annotations[class_label] += 1

        # Print the results
        print("Total Annotations:", total_annotations)
        print("\nAnnotations per Class:")
        for label, count in class_annotations.items():
            print(f"{label}: {count}")

    def get_filenames_for_class(self, class_number):
        # Initialize list for filenames
        class_files = []

        folder_path = '../datasets/train/labels'

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)

                # Read annotations from the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate over each line in the file
                    for line in lines:
                        annotation = line.split()
                        if annotation and int(annotation[0]) == class_number:
                            # Add filename to the list if the class matches
                            print(file_path)
                            break


if __name__ == "__main__":
    lab = LabelAmounts()
    lab.get_filenames_for_class(3)