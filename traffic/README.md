First I tried the steps taught in the lecture:
    One Convolution Layer (ReLU)
    One 2x2 MaxPooling
And Runtime was ~32s per test
But Accuracy was 97%

Next I tried adding the same Convolution and MaxPool layers again after the initial layers
    One Convolution Layer
    One 2x2 MaxPooling
    One Convolution Layer
    One 2x2 MaxPooling
And Runtime reduced to ~9s per test
And Accuracy improved to 99%

Next I tried adding 3 of the Convolution and MaxPool layers to see if trend of improvement would continue or if as expected, the reduction of detail will hinder results
    One Convolution Layer
    One 2x2 MaxPooling
    One Convolution Layer
    One 2x2 MaxPooling
    One Convolution Layer
    One 2x2 MaxPooling
And Runtime reduced to ~5s per test
And as expected Accuracy reduced to 98%

Tried 4 Layer Pairs but Failed

Went Back to 2 Layer Pairs and tried variations of activations:
Runtime stayed about the same for all activation functions
    2x ReLU:
        Accuracy: 99.2%
    2x Sigmoid:
        Accuracy: 83%
    2x TanH:
        Accuracy: 98.91%
    2x Softmax:
        Accuracy: 77%
    1x ReLU 1x TanH:
        Accuracy: 98.84%

Concluded that 2x ReLU is most accurate with decent runtime