from gettext import find
from numpy import size


file_name = "groups.txt"
true_group_list = []
with open(file_name) as f:
    lines = f.readlines()
    for line in lines:
        str_list = line.split()
        print("List of numbers in string format is:")
        print(str_list)
        num_list=[]
        for i in str_list:
            num_list.append(int(i))    
        print("Output List of numbers is:")
        print(num_list)
        true_group_list.append(num_list)
print(true_group_list)

predicted_group_list = [[1, 2], [3, 4], [12, 13], [14, 15], [16, 17, 19], [18, 20], [23, 24, 25]]

pred_intersection_true = 0
pred_union_true = size(predicted_group_list) + size(true_group_list)

for true_group in true_group_list:
    if(true_group in predicted_group_list):
        pred_intersection_true = pred_intersection_true + 1
        pred_union_true = pred_union_true - 1

print(pred_intersection_true)
print(pred_union_true)

iou = pred_intersection_true/pred_union_true

print(iou)




#for pred_group in predicted_group_list:
#        if(true_group == pred_group):
#            pred_intersection_true = pred_intersection_true + 1
#            break
