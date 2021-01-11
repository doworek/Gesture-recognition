import csv

with open('./annotations/jester-v1-train.csv', 'r') as rtrain, \
   open('./annotations/jester-v1-train-gest.csv', 'w', newline='') as wtrain, \
  open('./annotations/jester-v1-validation.csv', 'r') as rval, \
  open('./annotations/jester-v1-validation-gest.csv', 'w', newline='') as wval, \
  open('./annotations/tmp.csv', 'w', newline='') as tmp:

    # define reader and writer objects
    train_in = csv.reader(rtrain, delimiter=';')
    train_out = csv.writer(wtrain, delimiter=';')
    validation_in = csv.reader(rval, delimiter=';')
    validation_out = csv.writer(wval, delimiter=';')
    temp_id = csv.writer(tmp)

    # write headers
    train_out.writerow(next(train_in))

    # iterate and write rows based on condition
    for row in train_in:
        if (row[1] == 'Swiping Right' or row[1] == 'Swiping Left' or row[1] == 'Swiping Up' or row[1] == 'Swiping Down' or row[1] == 'Thumb Up' or row[1] == 'Thumb Down' or row[1] == 'Doing other things' or row[1] == "No gesture"):
            train_out.writerow(row)

    for val in validation_in:
        if (val[1] == 'Swiping Right' or val[1] == 'Swiping Left' or val[1] == 'Swiping Up' or val[1] == 'Swiping Down' or val[1] == 'Thumb Up' or val[1] == 'Thumb Down' or val[1] == 'Doing other things' or val[1] == "No gesture"):
            validation_out.writerow(val)