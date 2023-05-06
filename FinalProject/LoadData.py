import glob
import numpy
import pickle
from scipy import ndimage as ndimage
from sklearn.model_selection import train_test_split

'''
This script loads and processes gesture data from either the DHG or SHREC dataset. 
It first defines two functions, resize_gestures and load_gestures. 
The resize_gestures function takes an input list of gesture arrays and resizes them to a specified final length using the ndimage.zoom function.
The load_gestures function loads the gestures data and their labels from either the DHG or SHREC dataset. 
It takes four input arguments: dataset, root, version_x, and version_y. 
Based on these arguments, it reads the gesture data from the specified dataset and resizes the gestures using the resize_gestures function if the resize_gesture_to_length parameter is provided. 
It then extracts labels for the gestures, either in a 14-class or 28-class format, or both.
After defining these functions, the script loads the gesture data and labels using the load_gestures function with the SHREC dataset as an example. 
It then splits the loaded data into training and test sets using the train_test_split function from the sklearn library. 
Finally, it saves the resulting dataset to a pickle file using the write_data function.
'''

def resize_gestures(input_gestures, final_length=100):
    output_gestures = numpy.array([numpy.array([ndimage.zoom(x_i.T[j], final_length / len(x_i), mode='reflect') for j in range(numpy.size(x_i, 1))]).T for x_i in input_gestures])
    return output_gestures


def load_gestures(dataset, root, version_x, version_y, resize_gesture_to_length):
    if dataset == 'dhg':
      assert 'dataset_dhg' in root
    if dataset == 'shrec':
      assert 'dataset_shrec' in root
    
    if version_x == '3D':
        if dataset == 'dhg':
            pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeleton_world.txt'
        elif dataset == 'shrec':
            pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeletons_world.txt'
    else:
        if dataset == 'dhg':
            pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeleton_image.txt'
        elif dataset == 'shrec':
            pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeletons_image.txt'

    gestures_filenames = sorted(glob.glob(pattern))
    gestures = [numpy.genfromtxt(f) for f in gestures_filenames]
    if resize_gesture_to_length is not None:
        gestures = resize_gestures(gestures, final_length=resize_gesture_to_length)

    labels_14 = [int(filename.split('/')[-5].split('_')[1]) for filename in gestures_filenames]
    labels_28 = [int(filename.split('/')[-4].split('_')[1]) for filename in gestures_filenames]
    labels_28 = [labels_14[idx_gesture] if n_fingers_used == 1 else 14 + labels_14[idx_gesture] for idx_gesture, n_fingers_used in enumerate(labels_28)]

    if version_y == '14' or version_y == 14:
        return gestures, labels_14
    elif version_y == '28' or version_y == 28:
        return gestures, labels_28
    elif version_y == 'both':
        return gestures, labels_14, labels_28

def write_data(data, filepath):
    with open(filepath, 'wb') as output_file:
        pickle.dump(data, output_file)

gestures, labels_14, labels_28 = load_gestures(dataset='shrec', root='dataset_shrec', version_x='3D', version_y='both', resize_gesture_to_length=100)
x_train, x_test, y_train_14, y_test_14, y_train_28, y_test_28 = train_test_split(gestures, labels_14, labels_28, test_size=0.15)

# Save the dataset
data = {'x_train': x_train, 'x_test': x_test, 'y_train_14': y_train_14, 'y_train_28': y_train_28, 'y_test_14': y_test_14, 'y_test_28': y_test_28}
write_data(data, filepath='dhg_data.pckl')

