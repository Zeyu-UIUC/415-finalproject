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


def load_gestures(dataset, root, len):
    # dataset folder path. after dowloading the dataset, please put into corresponding folder (dataset_dhg or dataset_shrec)
    if dataset == 'dhg':
      assert 'dataset_dhg' in root
    if dataset == 'shrec':
      assert 'dataset_shrec' in root
    
    # check wich dataset is using
    if dataset == 'dhg':
        pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeleton_world.txt'
    elif dataset == 'shrec':
        pattern = root + '/gesture_*/finger_*/subject_*/essai_*/skeletons_world.txt'

    gfile = sorted(glob.glob(pattern))
    gestures = [numpy.genfromtxt(f) for f in gfile]
    if len is not None:
        gestures = resize_gestures(gestures, final_length=len)

    l1 = [int(filename.split('/')[-5].split('_')[1]) for filename in gfile]
    l2 = [int(filename.split('/')[-4].split('_')[1]) for filename in gfile]
    # for idx, fingure in enumerate(l2):
    #     if fingure == 1:
    #         l2.append(l1[idx])
    #     else:
    #         l2.append(14 + l1[idx] )
    l2 = [l1[idx] if f == 1 else 14 + l1[idx] for idx, f in enumerate(l2)]
  
    return gestures, l1, l2

gestures, l1, l2 = load_gestures('shrec', 'dataset_shrec', 100)
# split dataset
x_train, x_test, y_train_14, y_test_14, y_train_28, y_test_28 = train_test_split(gestures, l1, l2, test_size=0.15)

# Save the dataset
data = {'x_train': x_train, 'x_test': x_test, 'y_train_14': y_train_14, 'y_train_28': y_train_28, 'y_test_14': y_test_14, 'y_test_28': y_test_28}
# save pre-processed data to dhg_data.pckl, (the other one SHREC2017.pckl is old version, you could ignore it)
with open('dhg_data.pckl', 'wb') as output_file:
    pickle.dump(data, output_file)


