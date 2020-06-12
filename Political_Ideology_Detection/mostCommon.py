def run(train_data, test_data):
    train_samples = len(train_data)
    total_samples = len(test_data)
    lib_data = 0
    con_data = 0
    for each_sample in train_data:
        if each_sample["label"] == 0:
            lib_data += 1
        else:
            con_data += 1
    if lib_data >= con_data:
        output = 0
    else:
        output = 1

    correct = 0.0
    incorrect = 0.0
    for each_sample in test_data:
        if each_sample["label"] == 0:
            correct += 1
        else:
            incorrect += 1

    accuracy = correct / total_samples
    return accuracy